import os
import node
import threading
import argparse
import sys


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


def parse_config(config_path: str):
    if config_path.startswith("/"):
        print("Oh no, a hacker!!!")
        sys.exit(1)

    config_file = os.path.join(os.getcwd(), config_path)

    with open(config_file, "r") as f:
        config_lines = list(
            filter(
                lambda x: len(x) > 0,
                [l.strip() for l in f.readlines() if "#" not in l],
            )
        )

    parsed_configs = []
    for line in config_lines:
        config_line = line.split(" ")
        parsed_configs.append(config_line)
        # nodes.append(create_node(*configs))

    return parsed_configs


def start_node(nd: node.Node):
    nd.await_start()
    nd.start()


def get_process_config(configs: list, id: str):
    for config in configs:
        if config[0] == id:
            return config
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Something")
    parser.add_argument("-c", dest="config", help="config file path starting at cwd")
    parser.add_argument("--id", dest="process_id", help="the id of the process")
    args = parser.parse_args()

    has_required_config = (args.config == None or len(args.config) < 1) or (
        args.process_id == None
        or len(args.process_id) < 1
        or int(args.process_id, 10) < 1  # process IDs must be greater than 0
    )

    if has_required_config:
        parser.print_help()
        sys.exit(0)

    configs = parse_config(args.config)
    node_config = get_process_config(configs, args.process_id)
    actual_node = create_node(*node_config)
    start_node(actual_node)
