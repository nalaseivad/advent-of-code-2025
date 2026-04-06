import sys, re, traceback, pulp
from itertools import combinations


#
# Convert the indicator light diagram into a bitmask
#
def parse_target(s):
    result = 0
    for i, c in enumerate(s[1:-1]):
        if c == "#":
            result |= 1 << i
    return result


#
# Convert the list of button wiring schematics into a list of bitmaks - part_1
#
def parse_buttons_1(buttons):
    result = []
    for button in buttons:
        bits = 0
        indexes = [int(s) for s in button[1:-1].split(",")]
        for index in indexes:
            bits |= 1 << index
        result.append((bits, button))
    return result


#
# Convert the list of button wiring schematics into a list of bitmaks - part_2
#
def parse_buttons_2(buttons):
    result = []
    for button in buttons:
        indexes = [int(s) for s in button[1:-1].split(",")]
        result.append(indexes)
    return result


#
# Convert the joltage requirements into a list of light levels
#
def parse_joltage(s):
    return [int(j) for j in s[1:-1].split(",")]


def xor_all(values):
    result = 0
    for x in values:
        result ^= x[0]
    return result


def find_buttons(target, buttons):
    for n in range(len(buttons)):
        for subset in combinations(buttons, n):
            test = xor_all(subset)
            if test == target:
                return (n, subset)
    return 1


#
# Pressing a button (e.g. '(1, 3)') will toggle lights 1 and 3, i.e. will go from [....] to [.#.#] or from [####] to
# [#.#.].  Pressing the button 1, 3, 5, ... times has the same effect.  Also pressing 0, 2, 4, ... times has the same
# effect.  So we only need to consider pressing each button once or not at all.
#
def part_1(lines):
    total = 0
    for line in lines:
        parts = line.split(" ")
        target_spec = parts[0]
        target = parse_target(target_spec)
        button_specs = parts[1:-1]
        buttons = parse_buttons_1(button_specs)
        min_buttons = find_buttons(target, buttons)
        total += min_buttons[0]
    return total


def print_button_counts(x):
    button_counts = [n.value() for n in x]
    print(f"{button_counts=}")


def solve_lp(buttons, target_light_levels):
    print(f"{buttons=}")
    print(f"{target_light_levels=}")

    m = len(buttons)  # Number of buttons
    n = len(target_light_levels)  # Number of lights

    prob = pulp.LpProblem("Factory", pulp.LpMinimize)

    # x[i]: how many times each button is pressed
    x = [pulp.LpVariable(f"x_{i}", lowBound=0, cat="Integer") for i in range(m)]

    # Objective: minimize total presses
    prob += pulp.lpSum(x)

    # Constraints: one per light
    for j in range(n):
        prob += pulp.lpSum(x[i] for i in range(m) if j in buttons[i]) == target_light_levels[j]

    # Suppress output during solve
    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    print_button_counts(x)
    total_button_presses = sum(int(x[i].value()) for i in range(m))

    print(f"{total_button_presses=}")
    print()
    return total_button_presses


#
# Now we are targeting a specific total number of voltage increments for each light.  Let's assume that x_i is the
# number of times we press button i and the target for light j is target_j.  Then ...
#
# sum(x_i) where switch i includes light j = target_j
# x_i is an integer >= 0 for all i
#
# And we want to minimize sum(x_i)
#
# This is a linear programming problem.  Let's use the PuLP library for this, in a venv.
#
# One time setup ...
#
# $ python3 -m venv .
# $ source ./bin/activate
# $ python3 -m pip install pulp
# $ deactivate
#
# Then to run ...
#
# $ source ./bin/activate
# $ python3 day10.py 2 <inupt-file>
# $ deactivate
#
def part_2(lines):
    total = 0
    for line in lines:
        parts = line.split(" ")
        button_specs = parts[1:-1]
        buttons = parse_buttons_2(button_specs)
        joltage_spec = parts[-1]
        target_light_levels = parse_joltage(joltage_spec)
        total += solve_lp(buttons, target_light_levels)
    return total


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
