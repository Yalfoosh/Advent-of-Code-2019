from copy import deepcopy
from itertools import permutations
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

first_range = (0, 5)
second_range = (5, 10)


# region Mostly same as Day 5
def load(path: str = "input/7.txt"):
    with open(path) as file:
        return [int(x) for x in input_splitter.split(file.read().strip())]


def int_to_flag_vector(value, max_size=3):
    to_return = list()

    for _ in range(max_size):
        to_return.append(value % 10)
        value //= 10

    return to_return


# Slightly modified IO
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
    else:
        return len(memory)

    return position + len(parameters) + 1
# endregion


def sequential_compute(memory, input_signal: int = 0, initial_values=(0, 1, 2, 3, 4), **kwargs):
    no_print = kwargs.get("no_print", True)

    for phase_setting in initial_values:
        current_memory = deepcopy(memory)

        program_inputs = [phase_setting, input_signal]
        program_outputs = list()

        i = 0
        while i < len(current_memory):
            i = execute(current_memory, i, program_inputs, output=program_outputs, no_print=no_print)

        input_signal = program_outputs[-1]

    return input_signal


def feedback_loop_sequential(memory, input_signal: int = 0, initial_values=(5, 6, 7, 8, 9), **kwargs):
    no_print = kwargs.get("no_print", True)

    amps = [deepcopy(memory) for _ in initial_values]
    pointer = [0] * len(initial_values)
    program_inputs = [[initial_values[i]] for i in range(len(initial_values))]
    program_outputs = list()
    last_amp_out = 0

    while pointer[-1] < len(amps[-1]):
        for i in range(len(initial_values)):
            program_inputs[i].append(input_signal)

            stop_next = False
            while pointer[i] < len(amps[i]):
                if amps[i][pointer[i]] == 4:
                    stop_next = True

                pointer[i] = execute(amps[i], pointer[i], program_inputs[i], output=program_outputs, no_print=no_print)

                if stop_next:
                    input_signal = program_outputs[-1]

                    if i == len(initial_values) - 1:
                        last_amp_out = input_signal

                    break

    return last_amp_out


# Prep
instructions = load()


# First
to_check = permutations(range(*first_range))
wanted_1 = max([sequential_compute(deepcopy(instructions), 0, x) for x in to_check])

print(f"[1]\t{wanted_1}")


# Second
to_check_2 = permutations(range(*second_range))
wanted_2 = max([feedback_loop_sequential(deepcopy(instructions), 0, x) for x in to_check_2])

print(f"[2]\t{wanted_2}")
