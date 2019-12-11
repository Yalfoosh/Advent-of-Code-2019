from copy import deepcopy
from itertools import product
import re

input_splitter = re.compile(r",\s*")

first_replace = (12, 2)

wanted_output = 19690720
noun_range = (0, 100)
verb_range = (0, 100)


def load(path: str = "input/02.txt"):
    with open(path) as file:
        return list(map(int, input_splitter.split(file.read().strip())))


def command(memory, start):
    command_type = memory[start]

    if command_type == 99:
        return 1

    a = memory[memory[start + 1]]
    b = memory[memory[start + 2]]
    address = memory[start + 3]

    if command_type == 1:
        memory[address] = a + b
    elif command_type == 2:
        memory[address] = a * b


def execute_program(inputs):
    for i in range(0, len(inputs), 4):
        if command(inputs, i) is not None:
            break

    return inputs[0]


def second_function(noun, verb):
    return 100 * noun + verb


# Prep
instructions_original = load()

# First
instructions = deepcopy(instructions_original)
instructions[1], instructions[2] = first_replace

wanted_1 = execute_program(instructions)

# Second
wanted_2 = (0, 0)

for i, j in product(range(*noun_range), range(*verb_range)):
    instructions = deepcopy(instructions_original)
    instructions[1], instructions[2] = i, j

    if execute_program(instructions) == wanted_output:
        wanted_2 = (i, j)
        break

wanted_2 = second_function(*wanted_2)


print(f"[1]\t{wanted_1}")
print(f"[2]\t{wanted_2}")
