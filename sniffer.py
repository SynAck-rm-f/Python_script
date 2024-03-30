import socket

from ctypes import *
import os
import socket
import ipaddress
import struct

HOST = '192.168.206.174'


# class IP(Structure):
#     _fields_ = [
#         ("ihl", c_ubyte, 4),  # 4 bit unsigned char
#         ("version", c_ubyte, 4),  # 4 bit unsigned char
#         ("tos", c_ubyte, 8),  # 1 byte char
#         ("len", c_ushort, 16),  # 2 byte unsigned short
#         ("id", c_ushort, 16),  # 2 byte unsigned short
#         ("offset", c_ushort, 16),  # 2 byte unsigned short
#         ("ttl", c_ubyte, 8),  # 1 byte char
#         ("protocol_num", c_ubyte, 8),  # 1 byte char
#         ("sum", c_ushort, 16),  # 2 byte unsigned short
#         ("src", c_uint32, 32),  # 4 byte unsigned int
#         ("dst", c_uint32, 32)  # 4 byte unsigned int
#     ]
#
#     def __new__(cls, socket_buffer=None):
#         return cls.from_buffer_copy(socket_buffer)
#
#     def __init__(self, socket_buffer=None):
#         # human readable IP addresses
#         self.src_address = socket.inet_ntoa(struct.pack("<L", self.src))
#         self.dst_address = socket.inet_ntoa(struct.pack("<L", self.dst))


# class IP:
#     def __init__(self, buff=None):
#         #  B (1-byte unsigned char), H (2-byte unsigned short), < endianness
#         #  byte array that requires a byte-width specification; 4s means a 4-byte string
#         header = struct.unpack('<BBHHHBBH4s4s', buff)
#
#         # structure header diagram
#         self.ver = header[0] >> 4  # self right-shift
#         self.ihl = header[0] & 0xF  # AND 00001111 operator
#
#         self.tos = header[1]
#         self.len = header[2]
#         self.id = header[3]
#         self.offset = header[4]
#         self.ttl = header[5]
#         self.protocol_num = header[6]
#         self.sum = header[7]
#         self.src = header[8]
#         self.dst = header[9]
#         # human readable IP addresses
#         self.src_address = ipaddress.ip_address(self.src)
#         self.dst_address = ipaddress.ip_address(self.dst)
#         # map protocol constants to their names
#         self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}


def main():
    # Create raw socket, bind to public interface
    if os.name == 'nt':
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP

    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    sniffer.bind((HOST, 0))

    # Include the IP header in the capture
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    if os.name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    # Read one packet
    print(sniffer.recvfrom(65565))

    # If we're on Windows, turn off promiscuous mode
    if os.name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)


if __name__ == '__main__':
    main()
