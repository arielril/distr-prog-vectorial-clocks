import socket
import binascii
import struct


class Node:
    local_events = []
    sent_messages = []
    received_messages = []

    multicast_group = ("224.1.1.1", 8888)
    start_message = "start_bitches"

    def __init__(self):
        print("constructed :)")

    def start(self):
        print("started =P")

    def await_start(self):
        print("awaiting start...")
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
        try:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except AttributeError as e:
            print("error on reuse addr", e)

        s.bind(self.multicast_group)

        # host = socket.gethostbyname(socket.gethostname())
        # s.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(host))
        s.setsockopt(
            socket.IPPROTO_IP,
            socket.IP_ADD_MEMBERSHIP,
            struct.pack(
                "4sl", socket.inet_aton(self.multicast_group[0]), socket.INADDR_ANY
            ),
        )

        while True:
            try:
                data, addr = s.recvfrom(4096)

                if data.decode() == self.start_message:
                    # the caller runs the start :)
                    print("received the start command")
                    return
                else:
                    print(f"received something from ({addr}): {data}")

            except socket.error:
                print(f"failed to read from socket: {binascii.unhexlify(data)}")
