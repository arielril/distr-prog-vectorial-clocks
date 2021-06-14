import socket


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)

# tested on ipsec connection on wireshark
s.sendto(b"start_bitches", ("224.1.1.1", 8888))

s.close()
