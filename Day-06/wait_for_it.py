import math

with open("wait_for_it.in", "r") as f:
    data = [line.rstrip() for line in f]

def num_solutions(time, distance):
    """
    distance traveled = (time - wait) * wait
    solution:   (time - wait) * wait > distance + 0.5  (0.5 to prevent floating point errors)
                wait^2 - time * wait + distance + 0.5 < 0
                wait > (time - sqrt(time^2 - 4*(distance + 0.5)))/2
            and wait < (time + sqrt(time^2 - 4*(distance + 0.5)))/2
    """
    discriminant = time*time - 4 * distance - 2
    lower_bound = (time - math.sqrt(discriminant))/2
    upper_bound = (time + math.sqrt(discriminant))/2
    return math.floor(upper_bound) - math.ceil(lower_bound) + 1

def part1():
    times = [int(nums) for nums in data[0].partition(":")[2].split(" ") if nums != '']
    distances = [int(nums) for nums in data[1].partition(":")[2].split(" ") if nums != '']
    output = 1
    for time, distance in zip(times, distances):
        output *= num_solutions(time, distance)
    print(output)

def part2():
    time = int(data[0].partition(":")[2].replace(" ", ""))
    distance = int(data[1].partition(":")[2].replace(" ", ""))
    output = num_solutions(time, distance)
    print(output)

part1()
part2()