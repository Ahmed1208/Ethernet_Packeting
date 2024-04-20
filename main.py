
import sys
from Packet import Packet

# Initialize an empty dictionary to store variables
config_vars = {}


def extract_variables_from_config_file(file_name):
    with open(file_name, 'r') as file:
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

def process_file(file_name):
    # Here you can implement the logic to process the file
    # For demonstration purposes, let's just print the content of the file
    try:
        extract_variables_from_config_file(file_name)
    except FileNotFoundError:
        print("File not found:", file_name)




if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <configuration_file_name>")
        sys.exit(1)

    file_name = sys.argv[1]
    process_file(file_name)

    # Print the dictionary
    print(config_vars)

    custom_packet = Packet(dest_address=config_vars['DESTINATION_ADDRESS'], src_address=config_vars['SOURCE_ADDRESS'],ethernet_type=config_vars['ETHER_TYPE'])
    print(custom_packet)


    # Convert bytearray to hexadecimal representation
    hex_representation = ''.join('{:02x}'.format(byte) for byte in custom_packet.src_address)

    print(hex_representation)

