import math

import functions
from Packet import *
from functions import *


if __name__ == "__main__":
    global config_file
    global output_file

    if len(sys.argv) != 3:
        print("Usage: python main.py <configuration_file_name> <output_file>")
        sys.exit(1)


    #check if both files exists and writable and readable
    process_file(config_file,output_file)

    # creating a dictionary for all data inside the config.txt (input file)
    extract_variables_from_config_file(config_file)


    # clear packets_sequnce file
    with open(output_packets_sequence_file, 'w'):
        pass

    #check the data inside config file
    check_config_data()


    #calcultae how many bursts
    bursts_number = (int(config_vars['STREAM_DURATION_MS'])*1000) / int(config_vars['BURST_PERIODICITY_US'])
    print(f"number of bursts={bursts_number}")

    completed_bursts = True

    if(bursts_number == int(bursts_number)):
        bursts_number = int(bursts_number)
    else:
        bursts_number = math.ceil(bursts_number)
        completed_bursts = False


    print("/////////////////// starting new streaming connection ////////////////////////////")

    bursts_counter = 0
    index = 0

    if(completed_bursts):
        create_completed_bursts(bursts_number,int(config_vars['BURST_SIZE']))
        bursts_counter = bursts_number
    else:
        create_uncompleted_bursts(bursts_number,int(config_vars['BURST_SIZE']))
        bursts_counter = math.ceil(Packet.packets_counter/int(config_vars['BURST_SIZE']))

    print(f"number_of_bursts_created= {bursts_counter}")
    print(f"number_of_packets_created= {Packet.packets_counter}")

    dump_senetnce_data(f"number_of_bursts_created= {bursts_counter}")
    dump_senetnce_data(f"number_of_packets_created= {Packet.packets_counter}")



