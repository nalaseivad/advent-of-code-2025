import sys, re, traceback
from collections import deque


def print_grid(grid):
    for row in grid:
        print(",".join(f"{n:2}" for n in row))


def part_1(lines):
    corners = [tuple(map(int, line.split(","))) for line in lines]
    max_area = 0
    for i, (x1, y1) in enumerate(corners):
        for j, (x2, y2) in enumerate(corners):
            if j <= i:
                continue
            dx = abs(x2 - x1) + 1
            dy = abs(y2 - y1) + 1
            area = dx * dy
            if area > max_area:
                max_area = area
    return max_area


def compressed_grid(corners):
    #
    # Coordinate compression: Keep every corner coordinate, and also +1 so we can represent the space "after" a tile. We
    # basically compress all the edges down to minimal length.  Add a 1-tile pad around the outside so flood fill has
    # somewhere obvious to start.
    #
    # Cell [cy][cx] represents all real tiles with x in [xs[cx], xs[cx + 1]) and y in [ys[cy], ys[cy + 1])
    #

    min_x, max_x = min(x for x, _ in corners), max(x for x, _ in corners)
    min_y, max_y = min(y for _, y in corners), max(y for _, y in corners)
    
    # All the unique corner coords + space after + padding
    xs = sorted({min_x - 1, max_x + 2} | {x for x, _ in corners} | {x + 1 for x, _ in corners})
    ys = sorted({min_y - 1, max_y + 2} | {y for _, y in corners} | {y + 1 for _, y in corners})

    # Maps from actual coordinates to compressed coordinates
    x_to_cx = {x: i for i, x in enumerate(xs)}
    y_to_cy = {y: i for i, y in enumerate(ys)}

    grid_width = len(xs) - 1
    grid_height = len(ys) - 1
    boundary = [[False for _ in range(grid_width)] for _ in range(grid_height)]

    # Draw the polygon boundary by walking consecutive corners
    for i in range(len(corners)):
        x1, y1 = corners[i]
        x2, y2 = corners[(i + 1) % len(corners)]  # % ensures we wrap back around to index 0

        if x1 == x2:
            x = x1
            y_lo, y_hi = min(y1, y2), max(y1, y2)
            cx = x_to_cx[x]
            cy_lo, cy_hi = y_to_cy[y_lo], y_to_cy[y_hi + 1]
            for cy in range(cy_lo, cy_hi):
                boundary[cy][cx] = True
        elif y1 == y2:
            y = y1
            x_lo, x_hi = min(x1, x2), max(x1, x2)
            cy = y_to_cy[y]
            cx_lo, cx_hi = x_to_cx[x_lo], x_to_cx[x_hi + 1]
            for cx in range(cx_lo, cx_hi):
                boundary[cy][cx] = True
        else:
            raise ValueError("Adjacent corners must share x or y")

    # Flood fill outside
    outside = [[False for _ in range(grid_width)] for _ in range(grid_height)]
    q = deque()

    def try_enqueue(cx, cy):
        if 0 <= cx < grid_width and 0 <= cy < grid_height and not boundary[cy][cx] and not outside[cy][cx]:
            outside[cy][cx] = True
            q.append((cx, cy))

    # Start from all perimeter cells that are not boundary
    for cx in range(grid_width):
        try_enqueue(cx, 0)
        try_enqueue(cx, grid_height - 1)
    for cy in range(grid_height):
        try_enqueue(0, cy)
        try_enqueue(grid_width - 1, cy)

    while q:
        cx, cy = q.popleft()
        try_enqueue(cx + 1, cy)
        try_enqueue(cx - 1, cy)
        try_enqueue(cx, cy + 1)
        try_enqueue(cx, cy - 1)

    # A cell is usable if it is on the boundary or interior
    usable = [[boundary[cy][cx] or not outside[cy][cx] for cx in range(grid_width)] for cy in range(grid_height)]

    return grid_width, grid_height, x_to_cx, y_to_cy, usable


#
# How many bad tiles are there inside the rect with compressed corner coordinates (cx1, cy1) and (cx2, cy2)?
#
def bad_count(bad_ps, cx1, cy1, cx2, cy2):
    #
    # A: (cx1, cy1), B: (cx2, cy1), C: (cx2, cy2), D: (cx1, cy2)
    #
    # ..........
    # ..........
    # ..........
    # ...A-----B
    # ...|.....|
    # ...D-----C
    #
    # +--------+   +--------+   +-+.......   +-+.......
    # |.1......|   |.2......|   |3|.......   |4|.......
    # |........|   +--------+   |.|.......   +-+.......
    # |..A-----B   ...A-----B   |.|A-----B   ...A-----B
    # |..|.....|   ...|.....|   |.||.....|   ...|.....|
    # +--D-----C   ...D-----C   +-+D-----C   ...D-----C
    #
    return (
               bad_ps[cy2 + 1][cx2 + 1]   # 1 : Bad tile count for rect from origin to C
             - bad_ps[cy1][cx2 + 1]       # 2 : Bad tile count for rect from origin to B
             - bad_ps[cy2 + 1][cx1]       # 3 : Bad tile count for rect from origin to D
             + bad_ps[cy1][cx1]           # 4 : Bad tile count for rect from origin to A
             )


def make_bad_ps(grid_width, grid_height, usable):
    # Prefix sum of unusable cells so rectangle validation is O(1)
    bad_ps = [[0 for _ in range(grid_width + 1)] for _ in range(grid_height + 1)]
    for cy in range(grid_height):
        row_sum = 0
        for cx in range(grid_width):
            row_sum += (0 if usable[cy][cx] else 1)
            bad_ps[cy + 1][cx + 1] = bad_ps[cy][cx + 1] + row_sum
    return bad_ps


def part_2(lines):
    corners = [tuple(map(int, line.split(","))) for line in lines]

    grid_width, grid_height, x_to_cx, y_to_cy, usable = compressed_grid(corners)
    bad_ps = make_bad_ps(grid_width, grid_height, usable)
    
    max_area = 0

    # Try every pair of red corners as opposite corners
    for i, (x1, y1) in enumerate(corners):
        for j, (x2, y2) in enumerate(corners):
            if j <= i:
                continue

            x_lo, x_hi = min(x1, x2), max(x1, x2)
            y_lo, y_hi = min(y1, y2), max(y1, y2)

            # Rectangle includes all tiles x_lo .. x_hi and y_lo .. y_hi
            cx1 = x_to_cx[x_lo]
            cx2 = x_to_cx[x_hi + 1] - 1
            cy1 = y_to_cy[y_lo]
            cy2 = y_to_cy[y_hi + 1] - 1

            if bad_count(bad_ps, cx1, cy1, cx2, cy2) == 0:
                area = (x_hi - x_lo + 1) * (y_hi - y_lo + 1)
                if area > max_area:
                    max_area = area

    return max_area


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
