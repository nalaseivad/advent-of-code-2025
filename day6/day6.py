import sys, re, traceback, math


def transpose(rows):
    return ["".join(col) for col in zip(*rows)]


def evaluate_numbers(op, numbers):
    fn = sum if op == "+" else math.prod
    return fn([int(x) for x in numbers])


def evaluate_column_1(column):
    return evaluate_numbers(column[0], column[3])


def evaluate_column_2(column):
    return evaluate_numbers(column[0], transpose(column[3]))


#
# 0000000000111111
# 0123456789012345
#
# 123.328..51.64.
# .45.64..387.23.
# ..6.98..215.314
# *...+...*...+..    <- last_line, len = 15
#
# ^  ^^  ^^  ^^..
# |  ||  ||  ||  |
# start_col_0||  |
#    ||  ||  ||  |
#    end_col_0   |
#     start_col_1|
#        ||  ||  |
#        end_col_1
#         start_col_2
#            ||  |
#            end_col_2
#             start_col_3
#                |
#                end_col_3
#
def part_n(lines, evaluate_column_fn):
    lines = list(lines)
    last_line = lines[-1]
    columns = []       # [op, start_index, end_index, numbers]
    for n, c in enumerate(last_line):
        if c in ("+", "*"):
            if n > 0:
                columns[-1][2] = n - 1
            columns.append([c, n, None, None])
    columns[-1][2] = len(last_line) + 1
    for column in columns:
        numbers = []
        for line in lines[:-1]:
            start_index = column[1]
            end_index = column[2]
            numbers.append(line[start_index:end_index])
        column[3] = numbers
    return sum([evaluate_column_fn(column) for column in columns])


def part_1(lines):
    return part_n(lines, evaluate_column_1)


def part_2(lines):
    return part_n(lines, evaluate_column_2)


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
