import sys, re, traceback


def count_adjacent(grid, r, c, target):
    deltas = [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    ]
    count = 0
    for dr, dc in deltas:
        rr = r + dr
        cc = c + dc
        if 0 <= rr < len(grid) and 0 <= cc < len(grid[0]):
            if grid[rr][cc]["value"] == target:
                count += 1
    return count


def rows_to_grid(rows):
    grid = []
    for row in rows:
        grid.append([{ "value": char, "flags": None } for char in list(row)])
    return grid


def print_grid(grid):
    for row in grid:
        print("".join("x" if cell["flags"] else cell["value"] for cell in row))
    print()


def part_n(grid, fn):
    print_grid(grid)
    total = 0
    for r, row in enumerate(grid):
        for c, _ in enumerate(row):
            if fn(grid, r, c):
                total += 1
    print_grid(grid)
    return total


def flag_if_less_than_4_adjacent(grid, r, c):
    if grid[r][c]["value"] == "@" and count_adjacent(grid, r, c, "@") < 4:
        grid[r][c]["flags"] = True
        return True
    return False


def part_1(rows):
    grid = rows_to_grid(rows)
    return part_n(grid, flag_if_less_than_4_adjacent)


def part_2(rows):
    grid = rows_to_grid(rows)
    overall_total = 0
    while True:
        total = part_n(grid, flag_if_less_than_4_adjacent)
        overall_total += total
        print(f"{total=}, {overall_total=}")
        print()
        if total == 0:
            break
        for r, row in enumerate(grid):
            for c, _ in enumerate(row):
                if grid[r][c]["flags"]:
                    grid[r][c]["value"] = "."
                    grid[r][c]["flags"] = None
    return overall_total


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
    traceback.print_exc()
    exit(1)
