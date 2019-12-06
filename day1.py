def load(path: str = "input/1.txt"):
    to_return = list()

    with open(path) as file:
        for line in file.readlines():
            to_return.append(int(line.strip()))

    return to_return


def first(values):
    return sum([value // 3 - 2 for value in values])


def fuel_reduce(amount):
    to_return = 0

    amount = amount // 3 - 2

    while amount > 0:
        to_return += amount
        amount = amount // 3 - 2

    return to_return


def second(values):
    return sum([fuel_reduce(value) for value in values])


inputs = load()

print(f"[1]\t{first(inputs)}")
print(f"[2]\t{second(inputs)}")
