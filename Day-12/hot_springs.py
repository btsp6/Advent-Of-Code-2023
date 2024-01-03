import functools

with open("hot_springs.in", "r") as f:
    data = [line.rstrip() for line in f]

springs = [line.partition(" ")[0] for line in data]
records = [tuple(map(int, line.partition(" ")[2].split(","))) for line in data]

@functools.cache
def calculate_solutions(springs, records):
    if sum(records) + len(records) - 1 > len(springs):
        return 0
    if len(springs) == 0:
        if len(records) != 0:
            return 0
    if len(records) == 0:
        if "#" in springs:
            return 0
        return 1

    num_solutions = 0

    spring_length = records[0]
    visible_spring = springs.find("#")
    if visible_spring == -1:
        visible_spring = len(springs)
    # Check setting springs in range [idx, idx + spring_length - 1] from start up to first visible spring
    idx = 0
    check_idx = 0
    while idx + spring_length - 1 < len(springs) and idx <= visible_spring:
        if springs[check_idx] == ".":
            idx = check_idx + 1
        check_idx += 1
        if check_idx < idx + spring_length:
            continue
        # At this point, [idx, idx + spring_length - 1] are all valid spring positions
        # and check_idx = idx + spring_length
        if check_idx >= len(springs):
            # Reached the end of the spring list
            num_solutions += calculate_solutions("", records[1:])
            break
        # Haven't reached the end yet
        if springs[check_idx] == "#":
            idx += 1
            continue
        if check_idx + 1 >= len(springs):
            # Can't fit any more springs
            num_solutions += calculate_solutions("", records[1:])
            idx += 1
            continue
        num_solutions += calculate_solutions(springs[check_idx + 1:], records[1:])
        idx += 1

    return num_solutions

def part1():
    output = 0
    for spring_list, record_list in zip(springs, records):
        output += calculate_solutions(spring_list, record_list)

    print(output)

def part2():
    modified_springs = ["?".join([spring]*5) for spring in springs]
    modified_records = [record*5 for record in records]
    output = 0
    for spring_list, record_list in zip(modified_springs, modified_records):
        output += calculate_solutions(spring_list, record_list)

    print(output)

part1()
part2()