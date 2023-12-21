import math
from collections import OrderedDict

from modint import chinese_remainder


with open("wasteland.in", "r") as f:
    data = [line.rstrip() for line in f]

instructions = data[0]
instructions = instructions.replace("L", "0").replace("R", "1")
instructions = list(map(int, instructions))
data = data[2:]

data = [line.replace(" ", "").replace("(", "").replace(")", "") for line in data]
paths = {
    line.partition("=")[0]:
    [
        line.partition("=")[2].partition(",")[0],
        line.partition("=")[2].partition(",")[2],
    ] for line in data
}

def inc(steps):
    return (steps + 1) % len(instructions)

def part1():
    steps = 0
    location = "AAA"
    while location != "ZZZ":
        instruction = instructions[steps]
        location = paths[location][instruction]
        steps = inc(steps)
    print(steps)

def finished(locations):
    return all(location[-1] == "Z" for location in locations)

def get_p_path(location):
    """Gets the p-shaped path of (step, location) pairs the given starting location
    loops through before repeating
    Returns unique list of (step, location) pairs as well as the index that the
    path reinserts into after reaching the end of the list"""
    steps = 0
    index = 0
    curr_location = location
    p_path = OrderedDict()
    p_path[(steps, curr_location)] = index
    while True:
        instruction = instructions[steps]
        steps = inc(steps)
        index += 1
        curr_location = paths[curr_location][instruction]
        if (steps, curr_location) not in p_path:
            p_path[(steps, curr_location)] = index
        else:
            return [location for _, location in p_path.keys()], p_path[(steps, curr_location)]

def part2():
    locations = [location for location in paths.keys() if location[-1] == "A"]
    loop_finishes = []
    for location in locations:
        p_path, insertion_idx = get_p_path(location)
        p_loop = p_path[insertion_idx:]
        start_idx = math.ceil(insertion_idx / len(p_loop)) * len(p_loop)
        effective_loop = p_path[start_idx:] + p_path[insertion_idx:start_idx]
        finish_idxs = []
        for idx, location in enumerate(effective_loop):
            if location[-1] == "Z":
                finish_idxs.append(idx)
        assert len(finish_idxs) == 1
        loop_finishes.append((finish_idxs[0], len(p_loop)))

    print(loop_finishes)


part1()
part2()