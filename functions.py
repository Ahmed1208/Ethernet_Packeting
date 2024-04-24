import sys

# Initialize an empty dictionary to store variables inside config_file
config_vars = {}

IFG_value = 0x07
PREAMBLE_value = 0x55
SOF_value = 0xFD
Min_payload_size = 46      #as required in Ethernet frame defaults
Packet_header_size = 26    #size of the packet without payload data size

try:
    config_file = sys.argv[1]
except:
    print("Usage: python main.py <configuration_file_name> <output_file>")
    sys.exit(1)

try:
    output_file = sys.argv[2]
except:
    print("Usage: python main.py <configuration_file_name> <output_file>")
    sys.exit(1)

output_packets_sequence_file = "packets_sequnce.txt"

def extract_variables_from_config_file(config_file):
    with open(config_file, 'r') as file:
        for line in file:
            # Strip any leading/trailing whitespace
            line = line.strip()
            # If the line is not empty
            if line:
                # Split the line into variable name and value
                variable, value = line.split('=')
                # Split the value till the first space
                value = value.split(maxsplit=1)[0]
                # Store the value in the dictionary
                config_vars[variable.strip()] = value.strip()

def process_file(config_file_,output_file_):

    try:
        with open(config_file_):
            pass
    except FileNotFoundError:
            print(f"Error: File '{config_file_}' not found.")
            sys.exit(1)
    except PermissionError:
            print(f"PermissionError: File '{config_file_}' can't read.")
            sys.exit(1)

    try:
        with open(output_file_):
            pass
    except FileNotFoundError:
            print(f"Error: File '{output_file_}' not found.")
            sys.exit(1)
    except PermissionError:
            print(f"PermissionError: File '{output_file_}' can't read.")
            sys.exit(1)

    try:
       with open(config_file_, 'r') as f:
            pass
    except PermissionError:
        print(f"PermissionError: File '{config_file_}' can't read.")
        sys.exit(1)

    try:
        with open(output_file_, 'w') as f:
            pass
    except PermissionError:
        print(f"PermissionError: File '{output_file_}' can't write.")
        sys.exit(1)

    try:
        with open(output_file_, 'a') as f:
            pass
    except PermissionError:
        print(f"PermissionError: File '{output_file_}' can't modify.")
        sys.exit(1)

    #clear output file
    with open(output_file_,'w'):
       pass



def create_repeated_bytes(byte_size,data):
    #return struct.pack(f"{byte_size}B", *([data] * byte_size))
    return bytes([data] * byte_size)

def dump_data_in_file(data,output_file):

    with open(output_file, "a") as file:
        hex_string = ' '.join("{:02x}".format(byte) for byte in data)
        file.write(hex_string + "\n\n")

def dump_senetnce_data(string_data):
    with open(output_packets_sequence_file, "a") as file:
        file.write(string_data+"\n")

def check_config_data():

    #check if STREAM_DURATION_MS exists
    if( 'STREAM_DURATION_MS' in config_vars):
        try:
            temp = int(config_vars['STREAM_DURATION_MS'])
            if(temp<=0):
                raise
        except:
            print(f"STREAM_DURATION_MS must be positive integer value")
            sys.exit(1)
    else:
        print(f"STREAM_DURATION_MS doesn't exists")
        sys.exit(1)

    #check BURST_SIZE
    if( 'BURST_SIZE' in config_vars):
        try:
            temp = int(config_vars['BURST_SIZE'])
            if(temp != int(temp) or temp<=0):
                raise
        except:
            print(f"BURST_SIZE must be positive integer")
            sys.exit(1)
    else:
        print(f"BURST_SIZE doesn't exists")
        sys.exit(1)

    #check BURST_PERIODICITY_US
    if( 'BURST_PERIODICITY_US' in config_vars):
        try:
            temp = int(config_vars['BURST_PERIODICITY_US'])
            if(temp<=0):
                raise
        except:
            print(f"BURST_PERIODICITY_US must be positive value and less than STREAM_DURATION_MS")
            sys.exit(1)
    else:
        print(f"BURST_PERIODICITY_US doesn't exists")
        sys.exit(1)

    #check IFGs_NUMBER
    if( 'IFGs_NUMBER' in config_vars):
        try:
            temp = int(config_vars['IFGs_NUMBER'])
            if(temp<=0 or temp!=int(temp)):
                raise
        except:
            print(f"IFGs_NUMBER must be positive value")
            sys.exit(1)
    else:
        print(f"IFGs_NUMBER doesn't exists")
        sys.exit(1)

    #check SOURCE_ADDRESS
    if( 'SOURCE_ADDRESS' in config_vars):
        try:
            int_value = int(config_vars['SOURCE_ADDRESS'], 16)
            temp = bytes.fromhex(config_vars['SOURCE_ADDRESS'][2:])
            if(len(temp) != 6):
                raise
        except:
            print(f"SOURCE_ADDRESS must be 12 hex digits(6 bytes) starting with 0x, ex : 0x112233445566")
            sys.exit(1)
    else:
        print(f"SOURCE_ADDRESS doesn't exists")
        sys.exit(1)

    #check DESTINATION_ADDRESS
    if( 'DESTINATION_ADDRESS' in config_vars):
        try:
            int_value = int(config_vars['DESTINATION_ADDRESS'], 16)
            temp = bytes.fromhex(config_vars['DESTINATION_ADDRESS'][2:])
            if(len(temp) != 6 or config_vars['DESTINATION_ADDRESS'] == config_vars['SOURCE_ADDRESS']):
                raise
        except:
            print(f"DESTINATION_ADDRESS must be 12 hex digits(6 bytes) starting with 0x and different than source address, ex : 0x112233445566")
            sys.exit(1)
    else:
        print(f"DESTINATION_ADDRESS doesn't exists")
        sys.exit(1)


   #check ETHER_TYPE
    if( 'ETHER_TYPE' in config_vars):
        try:
            int_value = int(config_vars['ETHER_TYPE'], 16)
            temp = bytes.fromhex(config_vars['ETHER_TYPE'][2:])
            if(len(temp) != 2):
                raise
        except:
            print(f"ETHER_TYPE must be 4 hex digits(2 bytes) starting with 0x, ex : 0x0800")
            sys.exit(1)
    else:
        print(f"ETHER_TYPE doesn't exists")
        sys.exit(1)


   #check PAYLOAD_TYPE
    if( 'PAYLOAD_TYPE' in config_vars):
        try:
            if(config_vars['PAYLOAD_TYPE']== 'RANDOM'):
                pass
            else:
                int_value = int(config_vars['PAYLOAD_TYPE'])
                if(int_value<=0 or int_value!=int(int_value) or int_value+Packet_header_size<=int(config_vars['MAX_PACKET_SIZE']) or int_value > 1500):
                    raise
        except:
            print(f"PAYLOAD_TYPE must be RANDOM or fixed value, if fixed value then it must be <= MAX_PACKET_SIZE-26, less than 1500")
            sys.exit(1)
    else:
        print(f"PAYLOAD_TYPE doesn't exists")
        sys.exit(1)

    # check MAX_PACKET_SIZE
    if ('MAX_PACKET_SIZE' in config_vars):
        try:
            int_value = int(config_vars['MAX_PACKET_SIZE'])
            if (int_value <= 71 or int_value != int(int_value) or int_value > 1526 ):
                raise
        except:
            print(f"MAX_PACKET_SIZE must be positive integer and at least 72 bytes according to Ethernet 802.3")
            sys.exit(1)
    else:
        print(f"MAX_PACKET_SIZE doesn't exists")
        sys.exit(1)