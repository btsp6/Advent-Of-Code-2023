from collections import defaultdict

with open("./gear_ratios.in", "r") as f:
    data = f.readlines()

def check_valid(idx, start, end):
    """
    Checks for any symbols bordering the range
    [idx, start] ... [idx, end]
    """
    row_start = max(idx-1, 0)
    row_end = min(idx+1, len(data)-1)
    col_start = max(start-1, 0)
    col_end = min(end+1, len(data[0])-1)
    for row in range(row_start, row_end+1):
        for col in range(col_start, col_end+1):
            if not (symbol := data[row][col]).isnumeric() and symbol not in ".\n":
                return True
    return False

def part1():
    output = 0
    for ii, line in enumerate(data):
        start = None
        end = None
        num = 0
        for jj, char in enumerate(line):
            if char.isnumeric():
                if num == 0:
                    start = jj
                    end = jj
                else:
                    end = jj
                num = num * 10 + int(char)
            else:
                if num != 0:
                    is_valid = check_valid(ii, start, end)
                    if is_valid:
                        output += num
                num = 0
                start = None
                end = None

    print(output)

def add_gear(idx, start, end, num, gears):
    """
    Checks for any * bordering the range
    [idx, start] ... [idx, end]
    """
    row_start = max(idx-1, 0)
    row_end = min(idx+1, len(data)-1)
    col_start = max(start-1, 0)
    col_end = min(end+1, len(data[0])-1)
    for row in range(row_start, row_end+1):
        for col in range(col_start, col_end+1):
            if data[row][col] == "*":
                gears[(row, col)].append(num)
    return False

def part2():
    gears = defaultdict(list)

    output = 0
    for ii, line in enumerate(data):
        start = None
        end = None
        num = 0
        for jj, char in enumerate(line):
            if char.isnumeric():
                if num == 0:
                    start = jj
                    end = jj
                else:
                    end = jj
                num = num * 10 + int(char)
            else:
                if num != 0:
                    add_gear(ii, start, end, num, gears)
                num = 0
                start = None
                end = None

    for nums in gears.values():
        if len(nums) == 2:
            output += nums[0] * nums[1]

    print(output)


part1()
part2()