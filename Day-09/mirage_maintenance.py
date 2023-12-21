import functools

with open("mirage_maintenance.in", "r") as f:
    data = [line.rstrip() for line in f]

data = [list(map(int, line.split(" "))) for line in data]

@functools.cache
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n-1)

def extrapolate_coeffs(values):
    """
    Extrapolate the polynomial with f(i) = value_i for 0 <= i < n
    Represent it by f(x) = a_0 + a_1x + a_2x(x-1) + a_3x(x-1)(x-2) + ...
    f(n) / n! = a_0/n! + a_1/(n-1)! + ...
    """
    coeffs = []
    for idx, value in enumerate(values):
        # f(idx) = value
        # f(idx) = a_0 + a_1(idx) + ... + a_idx(idx)(idx-1)...1
        # a_idx = value/idx! - a_0/idx! - a_1/(idx-1)! - ... - a_(idx-1)/1!
        a_idx = value / factorial(idx)
        for other_idx in range(idx):
            a_idx -= coeffs[other_idx] / factorial(idx - other_idx)
        coeffs.append(a_idx)
    return coeffs

def extrapolate(values):
    coeffs = extrapolate_coeffs(values)
    next_idx = len(values)
    next_value = 0
    for idx, coeff in enumerate(coeffs):
        next_value += coeff / factorial(next_idx - idx)
    # Round to nearest integer to fix floating point errors
    return round(next_value * factorial(next_idx))

def extrapolate_back(values):
    """
    This time, f(-1) = a_0 - a_1*1 + a_2*2*1 - a_3*3*2*1 +...
    """
    coeffs = extrapolate_coeffs(values)
    prev_value = 0
    for idx, coeff in enumerate(coeffs):
        sign = -2*(idx % 2) + 1
        prev_value += sign * coeff * factorial(idx)
    return round(prev_value)


def part1():
    output = 0
    for line in data:
        next_value = extrapolate(line)
        output += next_value

    print(output)

def part2():
    output = 0
    for line in data:
        next_value = extrapolate_back(line)
        output += next_value

    print(output)

part1()
part2()