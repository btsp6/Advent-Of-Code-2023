from collections import defaultdict, OrderedDict

with open("lens_library.in", "r") as f:
    data = f.readline()

instructions = data.split(",")
ascii = [list(map(ord, inst)) for inst in instructions]

max_length = max(len(a) for a in ascii)
power17 = [17]
for i in range(1, max_length):
    power17.append((power17[-1] * 17) % 256)

def get_hash(instruction):
    a = list(map(ord, instruction))
    output = 0
    for idx, c in enumerate(reversed(a)):
        output += power17[idx] * c
    return output % 256

def part1():
    output = 0
    for instruction in instructions:
        output += get_hash(instruction)

    print(output)

def part2():
    boxes = defaultdict(OrderedDict)
    for instruction in instructions:
        op = '=' if '=' in instruction else '-'
        label, _, focus = instruction.partition(op)
        box = boxes[get_hash(label)]
        if op == '=':
            box[label] = int(focus)
        else:
            if label in box:
                del box[label]

    output = 0
    for box_idx, box in boxes.items():
        for idx, (_, focus) in enumerate(box.items()):
            output += (box_idx + 1) * (idx + 1) * focus

    print(output)

part1()
part2()