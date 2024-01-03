with open("pipe_maze.in", "r") as f:
    data = [line.rstrip() for line in f]

start = None
for row, line in enumerate(data):
    col = line.find("S")
    if col != -1:
        start = (row, col)
        break
assert start is not None

PIPE_ADJACENTS = {
    "|": {(1, 0), (-1, 0)},
    "-": {(0, 1), (0, -1)},
    "L": {(-1, 0), (0, 1)},
    "J": {(-1, 0), (0, -1)},
    "7": {(1, 0), (0, -1)},
    "F": {(1, 0), (0, 1)},
    "S": {(0, 1), (0, -1)},  # by observation
}

def add(coords1, coords2):
    return (coords1[0] + coords2[0], coords1[1] + coords2[1])

def get_pipe(pipe_coords):
    return data[pipe_coords[0]][pipe_coords[1]]

def get_next_coord(prev_coord, curr_coord):
    adjacent_coords = {add(curr_coord, adj) for adj in PIPE_ADJACENTS[get_pipe(curr_coord)]}
    adjacent_coords.remove(prev_coord)
    return next(iter(adjacent_coords))

def get_loop():
    loop = [start]
    # Insert the first pipe into loop. Observing the data, let's choose the one on the right
    start_row, start_col = start
    curr_coord = (start_row, start_col + 1)
    loop.append(curr_coord)
    while curr_coord != start:
        curr_coord = get_next_coord(loop[-2], loop[-1])
        loop.append(curr_coord)
    return loop

def get_enclosed(loop_coords):
    """
    Employ a diagonal-scanning method. Starting at coordinate (0, k), scan (1, k-1), ..., (i, k-i), ...
    and change parity of a counter every time we encounter any main loop pipe that isn't "J" or "F".
    Landing on any non-main loop square, if the counter parity is odd, it is inside; even, it is outside.
    """
    PARITY_PIPES = {"|", "-", "L", "7", "S"}
    enclosed_coords = set()
    width = len(data[0])
    height = len(data)
    for k in range(width + height - 1):
        parity = 0
        curr_coord = (0, k) if k < width else (k - width + 1, width - 1)
        while curr_coord[0] < height and curr_coord[1] >= 0:
            if curr_coord in loop_coords:
                if get_pipe(curr_coord) in PARITY_PIPES:
                    parity += 1
            else:
                if parity % 2 == 1:
                    enclosed_coords.add(curr_coord)
            curr_coord = add(curr_coord, (1, -1))
    return enclosed_coords


def part1():
    loop = get_loop()
    print(int(len(loop) // 2))

def part2():
    loop = get_loop()
    enclosed = get_enclosed(set(loop))
    print(len(enclosed))

part1()
part2()