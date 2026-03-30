import sys, re, traceback, math


def print_beams(beams, row, split_count):
    print("".join(cell if b is False else "|" for b, cell in zip(beams, row)), f" {split_count=}")


def part_1(lines):
    grid = [list(line) for line in lines]
    width = len(grid[0])
    beams = [False] * width
    split_count = 0
    for row in grid:
        next_beams = [False] * width
        for c, cell in enumerate(row):
            if cell == "S":
                next_beams[c] = True
            elif beams[c]:
                if cell == "^":
                    split_count += 1
                    if c - 1 >= 0:
                        next_beams[c - 1] = True
                    if c + 1 < width:
                        next_beams[c + 1] = True
                else:
                    next_beams[c] = True
        beams = next_beams
        print_beams(beams, row, split_count)
    return split_count


def part_2(lines):
    grid = [list(line) for line in lines]
    height = len(grid)
    width = len(grid[0])
    cache = {}
    def timelines(r, c):
        if c < 0 or c >= width:
            return 0
        if r == height:
            return 1
        if (r, c) in cache:
            return cache[(r, c)]
        if grid[r][c] == ".":
            result = timelines(r + 1, c)
        else:  # ^
            result = timelines(r + 1, c - 1) + timelines(r + 1, c + 1)
        cache[(r, c)] = result
        return result

    c = grid[0].index("S")
    return timelines(0, c)


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
