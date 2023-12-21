import bisect
from tqdm import tqdm

with open("fertilizer.in", "r") as f:
    data = f.readlines()

mappings = []
for line in data[1:]:
    if line == "\n":
        mappings.append([])
        continue
    if ":" in line:
        continue
    mapping = mappings[-1]
    after, before, amount = map(int, line.rstrip().split(" "))
    mapping.append((before, before + amount, after - before))

for mapping in mappings:
    mapping.sort()

def get_mapping(map_idx, input):
    mapping = mappings[map_idx]
    idx = bisect.bisect(mapping, input, key=lambda x: x[0]) - 1
    lower_bound, upper_bound, change = mapping[idx]
    if lower_bound <= input < upper_bound:
        return input + change
    return input

def get_range_mapping(map_idx, start, r):
    """Given a single start and range, returns a list of starts and ranges
    that the input maps to"""
    mapping = mappings[map_idx]
    end = start + r
    start_idx = bisect.bisect(mapping, start, key=lambda x: x[0]) - 1
    end_idx = bisect.bisect(mapping, end - 1, key=lambda x: x[0]) - 1

    starts = []
    ranges = []
    for idx in range(start_idx, end_idx + 1):
        lower_bound, upper_bound, change = mapping[idx]
        if start < lower_bound:
            starts.append(start)
            ranges.append(lower_bound - start)
            start = lower_bound
        if end <= upper_bound:
            starts.append(start + change)
            ranges.append(end - start)
            start = end
        else:
            if start < upper_bound:
                starts.append(start + change)
                ranges.append(upper_bound - start)
                start = upper_bound
            if idx == end_idx:
                starts.append(start)
                ranges.append(end - start)
                start = end

    return starts, ranges


def get_ranges_mapping(map_idx, starts, ranges):
    """Given lists of starts and ranges, returns lists of starts and ranges
    that the input maps to"""
    output_starts = []
    output_ranges = []
    for start, r in zip(starts, ranges):
        return_starts, return_ranges = get_range_mapping(map_idx, start, r)
        output_starts.extend(return_starts)
        output_ranges.extend(return_ranges)
    return output_starts, output_ranges

def get_ranges_mappings(starts, ranges):
    for map_idx in range(len(mappings)):
        starts, ranges = get_ranges_mapping(map_idx, starts, ranges)
    return starts, ranges


def get_mappings(input):
    for map_idx in range(len(mappings)):
        input = get_mapping(map_idx, input)
    return input

def part1():
    seeds = map(int, data[0].partition(":")[2].strip().split(" "))
    print(min(get_mappings(seed) for seed in seeds))

def part2():
    starts_and_ranges = list(map(int, data[0].partition(":")[2].strip().split(" ")))
    starts = starts_and_ranges[::2]
    ranges = starts_and_ranges[1::2]
    output_starts, _ = get_ranges_mappings(starts, ranges)
    print(min(output_starts))

part1()
part2()