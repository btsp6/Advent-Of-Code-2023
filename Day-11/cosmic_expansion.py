with open("cosmic_expansion.in", "r") as f:
    data = [line.rstrip() for line in f]

galaxies = []
for row in range(len(data)):
    for col in range(len(data[0])):
        if data[row][col] == "#":
            galaxies.append((row, col))

def distance(coord1, coord2):
    return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])

def get_expansions():
    expand_cols = []
    for col in range(len(data[0])):
        if all(data[row][col] == "." for row in range(len(data))):
            expand_cols.append(col)
    expand_rows = []
    for row in range(len(data)):
        if data[row] == "." * len(data[0]):
            expand_rows.append(row)

    col_expansions = 0
    num_col_expansions = []
    for col in range(len(data[0])):
        if col in expand_cols:
            col_expansions += 1
        num_col_expansions.append(col_expansions)
    row_expansions = 0
    num_row_expansions = []
    for row in range(len(data)):
        if row in expand_rows:
            row_expansions += 1
        num_row_expansions.append(row_expansions)
    return num_col_expansions, num_row_expansions

def part1():
    num_col_expansions, num_row_expansions = get_expansions()
    output = 0
    for idx in range(len(galaxies)):
        galaxy = galaxies[idx]
        for other_idx in range(idx):
            other_galaxy = galaxies[other_idx]
            dist = distance(galaxy, other_galaxy)\
                + abs(num_row_expansions[galaxy[0]] - num_row_expansions[other_galaxy[0]])\
                + abs(num_col_expansions[galaxy[1]] - num_col_expansions[other_galaxy[1]])
            output += dist

    print(output)

def part2():
    num_col_expansions, num_row_expansions = get_expansions()
    output = 0
    for idx in range(len(galaxies)):
        galaxy = galaxies[idx]
        for other_idx in range(idx):
            other_galaxy = galaxies[other_idx]
            dist = distance(galaxy, other_galaxy)\
                + 999999 * abs(num_row_expansions[galaxy[0]] - num_row_expansions[other_galaxy[0]])\
                + 999999 * abs(num_col_expansions[galaxy[1]] - num_col_expansions[other_galaxy[1]])
            output += int(dist)

    print(output)


part1()
part2()