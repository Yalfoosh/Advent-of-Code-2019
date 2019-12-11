from collections import defaultdict
from copy import deepcopy
import re


input_splitter = re.compile(r",\s*")

parameter_count_dict =\
    {
        1: 3, 2: 3,
        3: 1, 4: 1,
        5: 2, 6: 2,
        7: 3, 8: 3,
        9: 1
    }

default_memory_value = 0


# region Mostly same as Day 7
def load(path: str = "input/09.txt"):
    with open(path) as file:
        instruction_list = [int(x) for x in input_splitter.split(file.read().strip())]
        return defaultdict(lambda: default_memory_value, {index: x for index, x in enumerate(instruction_list)})


def int_to_flag_vector(value, max_size=3):
    to_return = list()

    for _ in range(max_size):
        to_return.append(value % 10)
        value //= 10

    return to_return


# Slightly modified IO
def execute(memory, position: int, program_input, **kwargs):
    relative_base = kwargs.get("relative_base", [0])

    command_code = memory[position]
    flags = [0, 0, 0]

    if command_code > 99:
        flags = int_to_flag_vector(command_code // 100)
        command_code = command_code % 100

    if command_code == 99:
        return -1

    parameters = [memory[pos] for pos in range(position + 1, position + 1 + parameter_count_dict[command_code])]

    for pi in range(len(parameters)):
        if pi == 2 and command_code in [1, 2, 7, 8]:
            if flags[pi] == 0:
                continue
            elif flags[pi] == 2:
                parameters[pi] = relative_base[0] + parameters[pi]
                continue

        if pi == 0 and command_code == 3:
            if flags[pi] == 0:
                continue
            elif flags[pi] == 2:
                parameters[pi] = relative_base[0] + parameters[pi]
                continue

        if flags[pi] == 0 and command_code != 3:
            parameters[pi] = memory[parameters[pi]]
        elif flags[pi] == 2:
            parameters[pi] = memory[parameters[pi] + relative_base[0]]

    if command_code == 1:
        memory[parameters[2]] = parameters[0] + parameters[1]
    elif command_code == 2:
        memory[parameters[2]] = parameters[0] * parameters[1]
    elif command_code == 3:
        if isinstance(program_input, int):
            memory[parameters[0]] = program_input
        else:
            memory[parameters[0]] = program_input[0]
            del program_input[0]
    elif command_code == 4:
        output_list = kwargs.get("output", None)

        if output_list is not None:
            output_list.append(parameters[0])

        if not kwargs.get("no_print", False):
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
    elif command_code == 9:
        relative_base[0] += parameters[0]
    else:
        return -1

    return position + len(parameters) + 1
# endregion


# Prep
original_instructions = load()
inputs = [1, 2]
relative_bases = [[0], [0]]

# First and second
for i in range(2):
    instructions = deepcopy(original_instructions)

    j = 0
    while j >= 0:
        j = execute(instructions, j, inputs[i], relative_base=relative_bases[i], prefix=i + 1)
