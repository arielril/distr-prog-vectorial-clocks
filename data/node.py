import socket
import binascii
import struct
import random
import time


class Node:
    local_events = []
    # sent messages
    message_events = []
    received_messages = []
    clock = 0

    multicast_group = ("224.1.1.1", 8888)
    start_message = "start_bitches"

    node_locations = {}

    def __init__(
        self,
        id,
        local_ip,
        local_port,
        event_chance,
        event_quantity,
        min_delay,
        max_delay,
    ):
        self.id = id
        self.local_ip = local_ip
        self.local_port = local_port
        self.event_chance = float(event_chance)
        self.event_quantity = int(event_quantity, 10)
        self.min_delay = int(min_delay, 10)
        self.max_delay = int(max_delay, 10)

    def set_node_locations(self, locations: dict):
        self.node_locations = locations

    def interact(self):
        while (len(self.local_events) + len(self.message_events)) < self.event_quantity:
            is_message_event = random.uniform(0, 1) > self.event_chance

            time.sleep(self.get_sleep_time())

            if is_message_event:
                self.send_message()
            else:
                self.send_local_event(self.clock)

    def send_message(self):
        print(f"sending message to someone ({len(self.message_events)})")
        dst_node_id = random.choice(list(self.node_locations.keys()))
        chosen_node = self.node_locations[dst_node_id]

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)

        msg = f"{self.id};{dst_node_id};{self.clock};message"
        s.sendto(msg.encode(), (chosen_node["host"], int(chosen_node["port"], 10)))

    def add_message_event(self, clock, dst_node_id):
        self.message_events.append(
            {
                "clock": clock,
                "dst_node": dst_node_id,
            }
        )

    def send_local_event(self, clock):
        print(f"sending local event ({len(self.local_events)})")
        self.local_events.append(
            {
                "clock": clock,
            }
        )

    def listen(self):
        print("listening =P")

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
        try:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except AttributeError as e:
            print("[node.listen] error on reuse addr", e)

        s.bind(self.multicast_group)

        s.setsockopt(
            socket.IPPROTO_IP,
            socket.IP_ADD_MEMBERSHIP,
            struct.pack(
                "4sl", socket.inet_aton(self.multicast_group[0]), socket.INADDR_ANY
            ),
        )

        while True:
            data = s.recv(4096)
            """
                data = '<orig>;<dst>;<clock>;<msg>'
            """
            data = data.decode()

            if len(data) < 1:
                print("[node.listen] received empty message")
                continue

            orig, dst, clock, msg = data.split(";")
            if orig == dst:
                # received message from me :(
                continue

            print(
                f"[node.listen] received message: ({orig=}, {dst=}, {clock=}, {msg=})"
            )

    def get_sleep_time(self):
        return random.randrange(self.min_delay, self.max_delay, 1) / 1000

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
