from collections import defaultdict

with open("./scratchcards.in", "r") as f:
    data = [line.rstrip() for line in f]

data = [line.partition(":")[2] for line in data]
wins = [line.partition("|")[0] for line in data]
own = [line.partition("|")[2] for line in data]
wins = [{char for char in line.split(" ") if char != ''} for line in wins]
own = [[char for char in line.split(" ") if char != ''] for line in own]

def part1():
    output = 0
    for idx, line in enumerate(own):
        points = 0
        for num in line:
            if num in wins[idx]:
                if points == 0:
                    points = 1
                else:
                    points *= 2
        output += points

    print(output)

def part2():
    output = 0
    copies = defaultdict(lambda: 1)
    for idx, line in enumerate(own):
        counter = 1
        for num in line:
            if num in wins[idx]:
                copies[idx+counter] += copies[idx]
                counter += 1
    for num_copies in copies.values():
        output += num_copies

    print(output)

part1()
part2()