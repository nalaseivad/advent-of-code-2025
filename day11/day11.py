import sys, re, traceback
from functools import lru_cache
from collections import defaultdict


def create_devices_graph(lines):
    devices = defaultdict(list)
    for line in lines:
        device_name, s = [s.strip() for s in line.split(":")]
        connected_devices = s.split(" ")
        devices[device_name].extend(connected_devices)
    return devices


#
#  Depth first search
#
def find_paths(graph, current, target, path):
    path = path + [current]   # Creates a new list
    if current == target:
        return [path]
    paths = []
    for neighbor in graph[current]:
        new_paths = find_paths(graph, neighbor, target, path)
        paths.extend(new_paths)
    return paths


def part_1(lines):
    devices_graph = create_devices_graph(lines)
    paths = find_paths(devices_graph, "you", "out", [])
    return len(paths)


def part_2(lines):
    devices_graph = create_devices_graph(lines)
    required = frozenset({'dac', 'fft'})
    
    @lru_cache(maxsize=None)
    def count_paths(current, required_seen):
        if current == "out":
            return 1 if required_seen == required else 0
        
        if current not in devices_graph:
            return 0
        
        total = 0
        for neighbor in devices_graph[current]:
            # Add neighbor to our set of seen required device names if it's required
            new_required_seen = required_seen | ({neighbor} if neighbor in required else set())
            total += count_paths(neighbor, new_required_seen)
        return total
    
    return count_paths('svr', frozenset())

# ===


def process_input(file_path, fn):
    with open(file_path, "r") as lines:
        result = fn((line.rstrip("\n") for line in lines))
    return result


def part_to_handler(part):
    return (part_1, part_2)[part - 1]


def get_part(arg):
    match = re.compile(r"^(1|2)$").match(arg)
    if not match:
        raise Exception(f"Bad part: {arg}")
    part = int(match.group(1))
    return part


def get_file_path(arg):
    file_path = arg
    return file_path


def validate_command_line(args):
    if len(args) != 3:
        raise Exception(f"Usage: python3 {args[0]} <part> <file_path>")


try:
    validate_command_line(sys.argv)
    part = get_part(sys.argv[1])
    file_path = get_file_path(sys.argv[2])
    handler = part_to_handler(part)
    result = process_input(file_path, handler)
    print(f"{result=}")
    exit(0)

except Exception as e:
    traceback.print_exc()
    exit(1)
