with open("./trebuchet.in", "r") as f:
    data = f.readlines()
    for i in range(len(data)):
        data[i] = data[i].replace("\n", "")

def part1():
    output = 0
    for line in data:
        number = ""
        for char in line:
            if char.isnumeric():
                number += char
                break
        for char in reversed(line):
            if char.isnumeric():
                number += char
                break
        output += int(number)

    print(output)

def part2():
    NUMERIC = {
        "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9,
    }
    for i in range(1, 10):
        NUMERIC[str(i)] = i

    breakpoint()

    output = 0
    for line in data:
        number = 0
        prefix_found = False
        postfix_found = False
        for i in range(1, len(line)+1):
            prefix = line[:i]
            postfix = line[-i:]
            if not prefix_found:
                for num, value in NUMERIC.items():
                    if num in prefix:
                        number += value * 10
                        prefix_found = True
                        break
            if not postfix_found:
                for num, value in NUMERIC.items():
                    if not postfix_found and num in postfix:
                        number += value
                        postfix_found = True
                        break
            if prefix_found and postfix_found:
                break
        output += number

    print(output)



part1()
part2()