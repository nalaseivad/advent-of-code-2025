import sys, re


def calc_max_joltage(batteries, num_batteries):
    digits = []
    for n in range(num_batteries - 1):
        digit = max(batteries[:n - (num_batteries - 1)])
        digits.append(digit)
        batteries = batteries[batteries.index(digit) + 1:]
    digit = max(batteries)
    digits.append(digit)
    max_joltage = int("".join(digits))
    return max_joltage


def part_n(banks, num_batteries):
    total = 0
    for bank in banks:
        batteries = list(bank)
        max_joltage = calc_max_joltage(batteries, num_batteries)
        total += max_joltage
    return total


def part_1(banks):
    return part_n(banks, 2)


def part_2(banks):
    return part_n(banks, 12)


# ===


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
