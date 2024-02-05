with open("lavaduct_lagoon.in", "r") as f:
    data = [line.rstrip() for line in f]

data = [line.split(" ") for line in data]
colors = [line[2][2:-1] for line in data]

DIRS = {
    "R": 1,
    "U": 1j,
    "L": -1,
    "D": -1j,
}
DIR_MAP = {
    "0": "R",
    "1": "D",
    "2": "L",
    "3": "U",
}

def get_area(coords, perimeter):
    x_coords = [coord.real for coord in coords]
    y_coords = [coord.imag for coord in coords]
    area = 0
    for i in range(len(coords)-1):
        area += x_coords[i] * y_coords[i+1] / 2
        area -= y_coords[i] * x_coords[i+1] / 2
    return int(abs(area)) + perimeter/2 + 1

def make_area(directions):
    coords = []
    curr_coord = 0
    coords.append(curr_coord)
    perimeter = 0
    for direction, steps in directions:
        curr_coord = curr_coord + DIRS[direction] * steps
        coords.append(curr_coord)
        perimeter += steps
    area = get_area(coords, perimeter)
    return int(area)

def part1():
    directions = [(line[0], int(line[1])) for line in data]
    print(make_area(directions))

def part2():
    directions = [(DIR_MAP[line[-1]], int(line[:-1], 16)) for line in colors]
    print(make_area(directions))

part1()
part2()