import sys, re


def parse_rotation(line):
    match = re.compile(r"^(R|L)(\d+)$").match(line)
    if not match:
        raise Exception(f"Bad move: {line}")
    direction, number = match.groups()
    number = int(number)
    delta = number if direction == "R" else -number
    return delta


def part_n(rotations, fn):
    current_position = 50
    count = 0
    for rotation in rotations:
        delta = parse_rotation(rotation)
        new_position = (current_position + delta) % 100
        count = fn(current_position, delta, count)
        current_position = new_position
    return count


def count_ends_on_zero(current_position, delta, count):
    new_position = (current_position + delta) % 100
    if new_position == 0:
        count += 1
    return count


def count_passes_zero(current_position, delta, count):
    if delta < 0:
        div, mod = divmod(delta, -100)
        count += div
        if current_position > 0 and current_position + mod <= 0:
            count += 1
    else:
        div, mod = divmod(delta, 100)
        count += div
        if current_position + mod >= 100:
            count += 1
    return count


def part_1(rotations):
    return part_n(rotations, count_ends_on_zero)


def part_2(rotations):
    return part_n(rotations, count_passes_zero)


#===


def process_input(file_path, fn):
    with open(file_path, "r") as lines:
        result = fn((line.rstrip() for line in lines))
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
    print(f"Error: {e}")
    exit(1)
