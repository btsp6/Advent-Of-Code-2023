from collections import deque

with open("lava.in", "r") as f:
    data = [line.rstrip() for line in f]

def get_symbol(location):
    return data[int(location.real)][int(location.imag)]

def in_bounds(location):
    if int(location.real) < 0 or int(location.real) >= len(data):
        return False
    if int(location.imag) < 0 or int(location.imag) >= len(data[0]):
        return False
    return True

def passthrough(symbol, direction):
    if symbol == ".":
        return True
    if symbol == "|" and direction.imag == 0:
        return True
    if symbol == "-" and direction.real == 0:
        return True
    return False

def reflect(symbol, direction):
    if symbol in ".":
        raise ValueError(f"Symbol {symbol} cannot reflect.")
    if symbol in "|-":
        if passthrough(symbol, direction):
            raise ValueError(f"Symbol {symbol} cannot reflect direction {direction}")
        if symbol == "|":
            return [1, -1]
        if symbol == "-":
            return [1j, -1j]
    # Normal reflection with \, /
    if symbol == "\\":
        return [direction.imag + direction.real * 1j]
    if symbol == "/":
        return [-direction.imag - direction.real * 1j]

def reflect_dirs(symbol, direction):
    if symbol in ".|-":
        raise ValueError(f"Symbol {symbol} not supported.")
    return frozenset({direction, -reflect(symbol, direction)[0]})

def print_visited(visited):
    board = ""
    for row in range(len(data)):
        line = ""
        for col in range(len(data[0])):
            if row + col * 1j in visited:
                line += "#"
            else:
                line += "."
        line += "\n"
        board += line
    print(board)

def get_visited(location, direction):
    visited = {}
    rays = deque()
    """Stores rays that still need to be traversed, with origin point a+bj and direction
    1 = down, 1j = right, -1 = up, -1j = left"""
    rays.append((location - direction, direction))
    while len(rays) > 0:
        origin, direction = rays.popleft()
        # print_visited(visited)
        # print(origin, direction)
        # breakpoint()
        location = origin + direction
        while in_bounds(location) and passthrough(symbol := get_symbol(location), direction):
            visited[location] = None
            location += direction
        if not in_bounds(location):
            continue
        if symbol in "|-":
            if location in visited:
                continue
            visited[location] = None
        elif symbol in "\\/":
            if location in visited:
                if visited[location] is None or visited[location] == reflect_dirs(symbol, direction):
                    continue
                visited[location] = None
            else:
                visited[location] = reflect_dirs(symbol, direction)
        reflections = reflect(symbol, direction)
        for reflection in reflections:
            rays.append((location, reflection))

    return visited

def part1():
    visited = get_visited(0, 1j)
    print_visited(visited)
    print(len(visited))

def part2():
    max_visited = 0
    for idx in range(len(data)):
        # Left side going right
        visited = get_visited(idx, 1j)
        if len(visited) > max_visited:
            max_visited = len(visited)
        # Right side going left
        visited = get_visited(idx + (len(data[0])-1) * 1j, -1j)
        if len(visited) > max_visited:
            max_visited = len(visited)
    for idx in range(len(data[0])):
        # Top side going down
        visited = get_visited(idx * 1j, 1)
        if len(visited) > max_visited:
            max_visited = len(visited)
        # Bottom side going up
        visited = get_visited(idx * 1j + (len(data)-1), -1)
        if len(visited) > max_visited:
            max_visited = len(visited)

    print(max_visited)

part1()
part2()