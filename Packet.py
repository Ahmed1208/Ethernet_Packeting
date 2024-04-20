

class Packet:
    def __init__(self, dest_address=None, src_address=None, ethernet_type=None):
        self.preamble = bytearray([0x55] * 7)
        self.sof = 0xFD
        self.dest_address = bytearray([0] * 6) if dest_address is None else dest_address
        self.src_address = bytearray([0] * 6) if src_address is None else src_address
        self.ethernet_type = bytearray([0] * 2) if ethernet_type is None else ethernet_type

    def __repr__(self):
        return f"Packet(preamble={self.preamble}, sof={self.sof}, dest_address={self.dest_address}, src_address={self.src_address}, ethernet_type={self.ethernet_type})"


