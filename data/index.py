import os
import node
import argparse
import sys
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

    return parsed_configs


def node_listen(nd: node.Node):
    nd.listen()


def node_interact(nd: node.Node):
    nd.interact()


def get_process_config(configs: list, id: str):
    for config in configs:
        if config[0] == id:
            return config
    return None


def get_node_locations(configs: list = []):
    locations = {}
    for config in configs:
        id = config[0]
        local_ip = config[1]
        local_port = config[2]
        locations[id] = {
            "host": local_ip,
            "port": local_port,
        }

    return locations


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Something")
        parser.add_argument(
            "-c", dest="config", help="config file path starting at cwd"
        )
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

        node_locations = get_node_locations(configs)
        node_locations.pop(args.process_id)
        actual_node.set_node_locations(node_locations)

        listen_thread = threading.Thread(target=node_listen, args=(actual_node,))

        # interact_thread = threading.Thread(target=node_interact, args=(actual_node,))

        actual_node.await_start()
        listen_thread.start()

        node_interact(actual_node)
        sys.exit(0)
        # listen_thread.join()

        # actual_node.show_results()

    except KeyboardInterrupt:
        pass
