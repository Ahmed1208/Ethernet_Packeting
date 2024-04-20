

class Packet:
    def __init__(self, dest_address=None, src_address=None, ethernet_type=None):
        self.preamble = bytearray([0x55] * 7)
        self.sof = bytearray([0xFD])

        if dest_address is not None:
            # Convert hexadecimal string to integer
            hex_number = int(dest_address, 16)
            # Convert integer to bytearray
            self.dest_address = bytearray.fromhex(hex(hex_number)[2:])
        else:
            self.dest_address = bytearray([0] * 6)

        if src_address is not None:
            # Convert hexadecimal string to integer
            hex_number = int(src_address, 16)
            # Convert integer to bytearray
            self.src_address = bytearray.fromhex(hex(hex_number)[2:])
        else:
            self.src_address = bytearray([0] * 6)

        if ethernet_type is not None:
            # Convert hexadecimal string to integer
            hex_number = int(src_address, 16)
            # Convert integer to bytearray
            self.ethernet_type = bytearray.fromhex(hex(hex_number)[2:])
        else:
            self.ethernet_type = bytearray([0] * 2)


    def __repr__(self):
        return f"Packet(preamble={self.preamble}, sof={self.sof}, dest_address={self.dest_address}, src_address={self.src_address}, ethernet_type={self.ethernet_type})"


