import binascii
import random
from functions import *


def printing_hex(data):
    return '0x' + ''.join(f'{byte:02X}' for byte in data)


class Packet:
    packets_counter = 0
    def __init__(self, dest_address, src_address, ethernet_type, payload):
        self.preamble = create_repeated_bytes(7,PREAMBLE_value)
        self.sof = create_repeated_bytes(1,SOF_value)
        self.dest_address = dest_address
        self.src_address = src_address
        self.ethernet_type = ethernet_type
        self.payload = payload
        self.crc = Packet.calculate_crc32(self.preamble+self.sof+self.dest_address+self.src_address+self.ethernet_type+self.payload)
        Packet.packets_counter+=1


    def __repr__(self):
        return f"Packet(preamble={printing_hex(self.preamble)}, sof={printing_hex(self.sof)}, dest_address={printing_hex(self.dest_address)}, src_address={printing_hex(self.src_address)}, ethernet_type={printing_hex(self.ethernet_type)},payload_size={len(self.payload)},crc={printing_hex(self.crc)})"

    def get_whole_packet_bytes(self):
        return self.preamble + self.sof + self.dest_address + self.src_address + self.ethernet_type + self.ethernet_type + self.payload + self.crc

    def get_payload_size(self):
        return len(self.payload)

    @staticmethod
    def calculate_crc32(packed_data):
        # Calculate CRC32 checksum
        crc32_value = binascii.crc32(packed_data) & 0xFFFFFFFF
        return crc32_value.to_bytes(4, byteorder='big')

    def set_payload(self,payload):
        self.payload = payload

    def get_payload(self,payload):
        self.payload = payload


def generate_packet(payload_data=None):
    # destination address
    dest_address = bytes.fromhex(config_vars['DESTINATION_ADDRESS'][2:])

    # source address
    src_address = bytes.fromhex(config_vars['SOURCE_ADDRESS'][2:])

    # Ether_type
    ethernet_type = bytes.fromhex(config_vars['ETHER_TYPE'][2:])

    if (payload_data is None):
        # Payload data
        if (config_vars['PAYLOAD_TYPE'] == 'RANDOM'):
            max_payload_size = int(config_vars['MAX_PACKET_SIZE']) - Packet_header_size
            payload_size = random.randint(Min_payload_size, max_payload_size)
        else:
            payload_size = int(config_vars['PAYLOAD_TYPE'])

        return Packet(dest_address=dest_address, src_address=src_address, ethernet_type=ethernet_type,payload=bytes([0xFF] * payload_size))
    else:
        payload_data = bytes.fromhex(payload_data[2:])

        #handling the minumum payload size
        if(len(payload_data) < Min_payload_size):
            diff = Min_payload_size - len(payload_data)
            padding = bytes([IFG_value]*diff)
            payload_data = payload_data + padding

        return Packet(dest_address=dest_address, src_address=src_address, ethernet_type=ethernet_type,payload=payload_data)


def create_completed_bursts(bursts_number,packets_number,incomplete=None):

    for i in range(bursts_number):

        print("start a burst")
        dump_senetnce_data("start a burst")

        index = 0
        for j in range(packets_number):

            # generate a packet
            packet = generate_packet()
            print("     " + str(index) + "  " + str(packet))
            dump_senetnce_data("     " + str(index) + "  " + str(packet))

            dump_data_in_file(packet.get_whole_packet_bytes(),output_file)

            #packet.dump_packet_in_file("output.txt")

            packet_size = Packet_header_size + packet.get_payload_size()
            index += packet_size


            if(j == packets_number-1 and i == bursts_number-1 and incomplete != None):
                IFG = create_repeated_bytes(int(config_vars['IFGs_NUMBER']), IFG_value)
                print("     " + f"IFG={printing_hex(IFG)}")
                dump_senetnce_data("     " + f"IFG={printing_hex(IFG)}")
                dump_data_in_file(IFG,output_file)
                continue

            #if last packet in last burst
            if(j == packets_number-1 and i == bursts_number-1):
                continue

            # add IFG
            IFG = create_repeated_bytes(int(config_vars['IFGs_NUMBER']), IFG_value)
            print("     " + f"IFG={printing_hex(IFG)}")
            dump_senetnce_data("     " + f"IFG={printing_hex(IFG)}")

            dump_data_in_file(IFG,output_file)

            IFG_size = int(config_vars['IFGs_NUMBER'])
            index += IFG_size

            if (j == packets_number - 1):  # at last packet in burst don't make any PADDING
                continue

            # add padding
            padding_bytes_number = index % 4
            if (padding_bytes_number == 0):
                pass
            else:
                padding_bytes_number = 4 - padding_bytes_number
                padding_IFG = create_repeated_bytes(padding_bytes_number, IFG_value)
                print("     " + f"padding_IFG={printing_hex(padding_IFG)}")
                dump_senetnce_data("     " + f"padding_IFG={printing_hex(padding_IFG)}")

                dump_data_in_file(padding_IFG,output_file)

                index += padding_bytes_number

        print("end of burst")
        dump_senetnce_data("end of burst")


def create_uncompleted_bursts(bursts_number,packets_number):

        #if there is uncompleted packet will be added, then you must send 1 in the third paramter of this function
        create_completed_bursts(bursts_number-1,packets_number,1)

        # calculate remaining packets
        time_per_packet = int(config_vars['BURST_PERIODICITY_US']) / int(config_vars['BURST_SIZE'])
        total_packets_to_be_created = int((int(config_vars['STREAM_DURATION_MS']) * 1000) / int(time_per_packet))
        remaining_packets = total_packets_to_be_created - Packet.packets_counter

        print("start a burst")
        dump_senetnce_data("start a burst")

        index = 0
        for x in range(remaining_packets):

            # generate a packet
            packet = generate_packet()
            print("     " + str(index) + "  " + str(packet))
            dump_senetnce_data("     " + str(index) + "  " + str(packet))

            dump_data_in_file(packet.get_whole_packet_bytes(),output_file)

            #packet.dump_packet_in_file("output.txt")

            packet_size = Packet_header_size + packet.get_payload_size()
            index += packet_size

            # add IFG
            IFG = create_repeated_bytes(int(config_vars['IFGs_NUMBER']), IFG_value)
            print("     " + f"IFG={printing_hex(IFG)}")
            dump_senetnce_data("     " + f"IFG={printing_hex(IFG)}")

            dump_data_in_file(IFG,output_file)

            IFG_size = int(config_vars['IFGs_NUMBER'])
            index += IFG_size

            # add padding
            padding_bytes_number = index % 4
            if (padding_bytes_number == 0):
                pass
            else:
                padding_bytes_number = 4 - padding_bytes_number
                padding_IFG = create_repeated_bytes(padding_bytes_number, IFG_value)
                print("     " + f"padding_IFG={printing_hex(padding_IFG)}")
                dump_senetnce_data("     " + f"padding_IFG={printing_hex(padding_IFG)}")

                dump_data_in_file(padding_IFG,output_file)

                index += padding_bytes_number

        # replace last packet by IFGS
        uncompleted_packet_IFG = create_repeated_bytes(int(config_vars['MAX_PACKET_SIZE']), IFG_value)
        print("     " + f"remaining_packet_IFG={printing_hex(uncompleted_packet_IFG)}")
        dump_senetnce_data("     " + f"remaining_packet_IFG={printing_hex(uncompleted_packet_IFG)}")

        dump_data_in_file(uncompleted_packet_IFG,output_file)

        print("end of burst")
        dump_senetnce_data("end of burst")




