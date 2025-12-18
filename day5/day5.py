import sys, re, traceback


def merge_ranges(ranges, new_range):
    new_min_value, new_max_value = new_range
    merged_ranges = []
    for min_value, max_value in ranges:
        if max_value < new_min_value or new_max_value < min_value:
            # No overlap, keep the existing range
            merged_ranges.append((min_value, max_value))
        else:
            # Overlapping ranges, merge them
            new_min_value = min(new_min_value, min_value)
            new_max_value = max(new_max_value, max_value)
    # Add the merged new range
    merged_ranges.append((new_min_value, new_max_value))
    return merged_ranges


def init(lines):
    ranges = []
    ingredients = []
    section = 0
    for line in lines:
        if line == "":
            section = 1
            continue
        if section == 0:
            min, max = [int(x) for x in line.split("-")]
            ranges.append((min, max))
        else:
            ingredients.append(int(line))
    return ranges, ingredients


def part_1(lines):
    ranges, ingredients = init(lines)
    count = 0
    for ingredient in ingredients:
        for min, max in ranges:
            if min <= ingredient <= max:
                count += 1
                break   
    return count


def part_2(lines):
    ranges, _ = init(lines)
    merged_ranges = []
    for min, max in ranges:
        merged_ranges = merge_ranges(merged_ranges, (min, max))
    total_ids = 0
    for min, max in merged_ranges:
        #print(f"{min}-{max}")
        total_ids += max - min + 1
    return total_ids


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
