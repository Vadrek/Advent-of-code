from os.path import join, dirname

convert = {3: "=", 4: "-", "=": -2, "-": -1}

def to_snafu(n):
    s = ""
    unit = 0
    while n:
        unit = n % 5
        if unit > 2:
            n += 5 - unit
            unit = convert[unit]
        s = str(unit) + s
        n //= 5
    return s

def to_decimal(s):
    expo = 0
    num = 0
    for c in s[::-1]:
        c = convert.get(c, c)
        num += int(c) * 5**expo
        expo += 1
    return num

def solve(data):
    total = 0
    for s in data:
        total += to_decimal(s)
    return to_snafu(total)


with open(join(dirname(__file__), 'data.txt')) as f:
    data = f.read().splitlines()
# print('solve(data)', solve(data))

for i in range(20):
    print(i, to_snafu(i), to_decimal(to_snafu(i)))