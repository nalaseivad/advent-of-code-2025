import sys, re


def is_valid_1(id):
    s = str(id)
    n = len(s)
    if n < 2:
        return True
    if n % 2 == 0 and s[: n // 2] == s[n // 2:]:
        return False
    return True


def is_periodic(id):
    s = str(id)
    return s in (s + s)[1:-1]


def is_valid_2(id):
    return not is_periodic(id)


def part_1(lines):
    return part_n(lines, is_valid_1)


def part_2(lines):
    return part_n(lines, is_valid_2)


def part_n(lines, is_valid_fn):
    sum = 0
    for line in lines:
        for pair in line.split(","):
            min_id, max_id = (int(n) for n in pair.split("-"))
            for id in range(min_id, max_id + 1):
                if not is_valid_fn(id):
                    sum += id
    return sum


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
