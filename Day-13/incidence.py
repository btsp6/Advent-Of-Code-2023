with open("incidence.in", "r") as f:
    data = [line.rstrip() for line in f]

plots = [[]]
for line in data:
    if line == "":
        plots.append([])
        continue
    plots[-1].append(line)

def transpose(plot):
    return ["".join(plot[row][col] for row in range(len(plot))) for col in range(len(plot[0]))]

plots_t = [transpose(plot) for plot in plots]

def get_reflection(array):
    """Finds the index after which the array is a reflection across that point."""
    for reflection in range(0, len(array)-1):
        idx = reflection
        is_reflection = True
        while idx >= 0 and (reflected_idx := 2*reflection+1 - idx) < len(array):
            if array[idx] != array[reflected_idx]:
                is_reflection = False
                break
            idx -= 1
        if is_reflection:
            return reflection + 1
    return None

def off_by_one(str1, str2):
    fixed = False
    for c1, c2 in zip(str1, str2):
        if c1 != c2:
            if not fixed:
                fixed = True
            else:
                return False
    return fixed

def get_fixed_reflection(array):
    """Finds the index after which the array is a reflection across that point, given a fix occurs"""
    for reflection in range(0, len(array)-1):
        idx = reflection
        is_reflection = True
        fixed = False
        while idx >= 0 and (reflected_idx := 2*reflection+1 - idx) < len(array):
            if array[idx] != array[reflected_idx]:
                if not off_by_one(array[idx], array[reflected_idx]):
                    is_reflection = False
                    break
                if fixed:
                    is_reflection = False
                    break
                fixed = True
            idx -= 1
        if is_reflection and fixed:
            return reflection + 1
    return None

def part1():
    output = 0
    for plot, plot_t in zip(plots, plots_t):
        if (horizontal_reflection := get_reflection(plot)) is not None:
            output += 100 * horizontal_reflection
        if (vertical_reflection := get_reflection(plot_t)) is not None:
            output += vertical_reflection

    print(output)

def part2():
    output = 0
    for plot, plot_t in zip(plots, plots_t):
        if (horizontal_reflection := get_fixed_reflection(plot)) is not None:
            output += 100 * horizontal_reflection
        if (vertical_reflection := get_fixed_reflection(plot_t)) is not None:
            output += vertical_reflection

    print(output)

part1()
part2()