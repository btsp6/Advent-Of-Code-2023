with open("./cube_conundrum.in", "r") as f:
    data = [line.rstrip() for line in f]

data = [line.partition(":")[2] for line in data]
data = [line.split(";") for line in data]
data = [[{amount.partition(" ")[2]: int(amount.partition(" ")[0]) for amount in group.strip().split(", ")} for group in line] for line in data]

def part1():
    LIMITS = {"red": 12, "green": 13, "blue": 14}

    output = 0
    for idx, line in enumerate(data):
        possible = True
        for amounts in line:
            for color, amount in amounts.items():
                if LIMITS[color] < amount:
                    possible = False
                    break
            if not possible:
                break
        if possible:
            output += idx + 1

    print(output)


def part2():
    output = 0
    for line in data:
        min_amounts = {"red": 0, "green": 0, "blue": 0}
        for amounts in line:
            for color, amount in amounts.items():
                min_amounts[color] = max(min_amounts[color], amount)
        output += min_amounts["red"] * min_amounts["green"] * min_amounts["blue"]


    print(output)


part1()
part2()