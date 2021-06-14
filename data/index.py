import os
import node
import threading


def create_node(*config_line: list):
    (
        id,
        local_ip,
        local_port,
        event_chance,
        event_quantity,
        min_delay,
        max_delay,
    ) = config_line
    nd = node.Node(
        id, local_ip, local_port, event_chance, event_quantity, min_delay, max_delay
    )
    return nd


def parse_config():
    config_file = os.path.join(os.getcwd(), "config")

    with open(config_file, "r") as f:
        config_lines = list(
            filter(
                lambda x: len(x) > 0,
                [l.strip() for l in f.readlines() if "#" not in l],
            )
        )

    nodes = []
    for line in config_lines:
        configs = line.split(" ")
        print("config", configs)
        nodes.append(create_node(*configs))

    return nodes


def start_node(nd: node.Node):
    nd.await_start()
    nd.start()


if __name__ == "__main__":
    nodes = parse_config()
    print(nodes)

    threads = []
    for nd in nodes:
        th = threading.Thread(target=start_node, args=(nd,), daemon=True)
        th.start()
        threads.append(th)

    for t in threads:
        t.join()
