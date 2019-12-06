from copy import deepcopy
import re


input_splitter = re.compile(r",\s*")

parameter_count_dict =\
    {
        1: 3, 2: 3,
        3: 1, 4: 1,
        5: 2, 6: 2,
        7: 3, 8: 3,
        99: 1
    }


def load(path: str = "input/5.txt"):
    with open(path) as file:
        return [int(x) for x in input_splitter.split(file.read().strip())]


def int_to_flag_vector(value, max_size=3):
    to_return = list()

    for _ in range(max_size):
        to_return.append(value % 10)
        value //= 10

    return to_return


def execute(memory, position: int, program_input, **kwargs):
    command_code = memory[position]
    flags = [0, 0, 0]

    if command_code > 99:
        flags = int_to_flag_vector(command_code // 100)
        command_code = command_code % 100

    if command_code == 99:
        return len(memory)

    parameters = memory[position + 1: position + 1 + parameter_count_dict[command_code]]

    for pi in range(min(2, len(parameters))):
        if flags[pi] == 0 and command_code != 3:
            parameters[pi] = memory[parameters[pi]]

    if command_code == 1:
        memory[parameters[2]] = parameters[0] + parameters[1]
    elif command_code == 2:
        memory[parameters[2]] = parameters[0] * parameters[1]
    elif command_code == 3:
        memory[parameters[0]] = program_input
    elif command_code == 4:
        prefix = kwargs.get("prefix", None)
        prefix = "" if prefix is None else "[{}]\t".format(str(prefix))

        print(f"{prefix}{parameters[0]}")
    elif command_code == 5:
        if parameters[0] != 0:
            return parameters[1]
    elif command_code == 6:
        if parameters[0] == 0:
            return parameters[1]
    elif command_code == 7:
        memory[parameters[2]] = 1 if (parameters[0] < parameters[1]) else 0
    elif command_code == 8:
        memory[parameters[2]] = 1 if (parameters[0] == parameters[1]) else 0
    else:
        return len(memory)

    return i + len(parameters) + 1


# Prep
original_instructions = load()

# First

first_input = 1
instructions = deepcopy(original_instructions)

i = 0
while i < len(instructions):
    i = execute(instructions, i, first_input, prefix=1)

# Second
second_input = 5
instructions = deepcopy(original_instructions)

i = 0
while i < len(instructions):
    i = execute(instructions, i, second_input, prefix=2)
