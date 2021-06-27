import struct
import socket

mcast = ("224.1.1.1", 8888)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)

s.setsockopt(
    socket.IPPROTO_IP,
    socket.IP_ADD_MEMBERSHIP,
    struct.pack("4sl", socket.inet_aton(mcast[0]), socket.INADDR_ANY),
)

# tested on ipsec connection on wireshark
s.sendto(b"start_bitches", mcast)

s.close()
