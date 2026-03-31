import sys, re, traceback, math


def print_pairs(pairs):
    for n, (i, box1, j, box2, distance) in enumerate(pairs):
        if n == 10:
            break
        print(f"{i}, {box1}, {j}, {box2}, {distance}")


def part_1(lines):
    junction_boxes = [tuple(map(int, line.split(","))) for line in lines]
    
    # Generate all pairs of junction boxes and calc the distance between their coordinates
    pairs = []
    for i, box1 in enumerate(junction_boxes):
        for j, box2 in enumerate(junction_boxes):
            if i <= j:
                continue
            pairs.append((i, box1, j, box2, math.dist(box1, box2)))
    
    pairs.sort(key=lambda t: t[-1])   # Sort by distance between junction boxes in ascending order

    # Create a map from box index to the circuit (set of connected boxes) that contains that box
    box_to_circuits = {n: set([n]) for n in range(len(junction_boxes))}

    def connect(i, j):
        circuit1 = box_to_circuits[i]
        circuit2 = box_to_circuits[j]
        merged_circuit = circuit1.union(circuit2)
        for n in merged_circuit:
            box_to_circuits[n] = merged_circuit
        return

    def connect_top_n(n):
        for index, (i, _, j, _, _) in enumerate(pairs):
            if index == n:
                break
            connect(i, j)

    connect_top_n(1000)  # Connect the top 1000 closest pairs of boxes

    # Merge all the circuits into a list of unique circuits.
    # Need to use frozenset here, an immutable set, because it's hashable.  I need a list of hashable values to use to
    # initialize the outer set.
    circuits = list(set(frozenset(circuit) for circuit in box_to_circuits.values()))
    circuits.sort(key=lambda c: len(c), reverse=True)   # Sort by circuit length descending

    return len(circuits[0]) * len(circuits[1]) * len(circuits[2])


def part_2(lines):
    # As in part 1 ...
    junction_boxes = [tuple(map(int, line.split(","))) for line in lines]
    pairs = []
    for i, box1 in enumerate(junction_boxes):
        for j, box2 in enumerate(junction_boxes):
            if i <= j:
                continue
            pairs.append((i, box1, j, box2, math.dist(box1, box2)))
    pairs.sort(key=lambda t: t[-1])

    box_to_circuits = {n: set([n]) for n in range(len(junction_boxes))}

    # Different connect logic.
    # If a new connection creates a circuit contining all the boxes then return true, else false
    def connect(i, j):
        circuit1 = box_to_circuits[i]
        circuit2 = box_to_circuits[j]
        merged_circuit = circuit1.union(circuit2)
        if len(merged_circuit) == len(junction_boxes):
            return True
        for n in merged_circuit:
            box_to_circuits[n] = merged_circuit
        return False

    for i, _, j, _, _ in pairs:
        if connect(i, j):
            # Connecting these two boxes formed the full circuit
            box_i = junction_boxes[i]
            box_j = junction_boxes[j]
            return box_i[0] * box_j[0]

    print("This shouldn't happen")
    return -1


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
