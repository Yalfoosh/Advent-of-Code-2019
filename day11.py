from collections import defaultdict
from copy import deepcopy
import numpy as np
import re
from typing import Callable, Dict, List, Tuple

input_splitter = re.compile(r"\s*,\s*")

parameter_count_dict =\
    {
        1: 3, 2: 3,
        3: 1, 4: 1,
        5: 2, 6: 2,
        7: 3, 8: 3,
        9: 1
    }

default_memory_value = 0


# region Exact same thing as Day 9.
def load(path: str = "input/11.txt"):
    with open(path) as file:
        instruction_list = [int(x) for x in input_splitter.split(file.read().strip())]
        return defaultdict(lambda: default_memory_value, {index: x for index, x in enumerate(instruction_list)})


def int_to_flag_vector(value, max_size=3):
    to_return = list()

    for _ in range(max_size):
        to_return.append(value % 10)
        value //= 10

    return to_return


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


def default_rules(current_state, command):
    if current_state == (0, 0) or current_state[0] == current_state[1]:
        return 0, 1
    else:
        if command[1] == 0:
            return -current_state[1], current_state[0]
        elif command[1] == 1:
            return current_state[1], -current_state[0]


class Canvas:
    def __init__(self, starting_position: List[int] or Tuple[int, int] = (0, 0),
                 starting_memory: Dict[Tuple[int, int], int] = None,
                 starting_state=None, rules: Callable = default_rules):
        if isinstance(starting_position, list):
            starting_position = tuple(starting_position)[:2]
        if starting_position is None or not isinstance(starting_position, tuple) or not len(starting_position) == 2\
                or not (isinstance(starting_position[0], int) and isinstance(starting_position[1], int)):
            starting_position = (0, 0)

        if starting_memory is None or not isinstance(starting_memory, dict):
            starting_memory = dict()

        if starting_state is None:
            starting_state = (0, 1)

        if rules is None or not callable(rules):
            rules = default_rules

        self.__original_position = deepcopy(starting_position)
        self.__current_position = deepcopy(starting_position)
        self.__memory = defaultdict(lambda: 0, starting_memory)

        self.__original_state = deepcopy(starting_state)
        self.__current_state = deepcopy(starting_state)
        self.__rules = rules

        self.__paint_history = defaultdict(lambda: list())

    def paint(self, command: Tuple):
        self.__memory[self.__current_position] = command[0]
        self.__paint_history[self.__current_position].append(command)

        self.__current_state = self.__rules(self.__current_state, command)
        self.__current_position = (self.__current_position[0] + self.__current_state[0],
                                   self.__current_position[1] + self.__current_state[1])

        return self.__memory[self.__current_position]

    def number_of_first_paint_jobs(self):
        return len(self.__paint_history)

    def __find_image_bounds(self):
        prototype = list(self.__paint_history.keys())[0]
        x_min, x_max, y_min, y_max = (prototype[0], prototype[0], prototype[1], prototype[1])

        for location in self.__paint_history:
            x_min = min(x_min, location[0])
            x_max = max(x_max, location[0])
            y_min = min(y_min, location[1])
            y_max = max(y_max, location[1])

        return x_min, x_max, y_min, y_max

    def display_image(self):
        bounds = self.__find_image_bounds()

        # Because bounds are inclusive, the dimensions are 1 larger than the difference of their extremes.
        image_dimensions = bounds[1] - bounds[0] + 1, bounds[3] - bounds[2] + 1
        image_elements = image_dimensions[0] * image_dimensions[1]

        image_array = np.array([0] * image_elements)
        image_array = np.reshape(image_array, image_dimensions[::-1])

        # By default everything is black.
        for i in range(image_dimensions[1]):
            for j in range(image_dimensions[0]):
                image_array[i][j] = 0

        # Because the upper left corner is (0, 0), we have to flip the image around the x-axis. We do this by inverting
        # the row index and writing the last known color on the location we're remapping to the image array.
        for location in self.__paint_history:
            image_array[image_dimensions[1] - location[1] + bounds[2] - 1][location[0] - bounds[0]] =\
                self.__paint_history[location][-1][0]

        image_representation = list()

        for row in image_array:
            temp = ""

            for element in row:
                temp += "##" if element == 1 else "  " if element == 0 else "??"

            image_representation.append(temp)

        for row in image_representation:
            print(row)


# Prep
original_instructions = load()


# First
instructions = deepcopy(original_instructions)
canvas = Canvas()
relative_base = [0]
inputs = [0]
outputs = []

i = 0
while i >= 0:
    i = execute(instructions, i, inputs,
                output=outputs,
                relative_base=relative_base,
                no_print=True)

    if len(outputs) == 2:
        inputs.append(canvas.paint(tuple(outputs)))
        outputs.clear()

print(f"[1]\t{canvas.number_of_first_paint_jobs()}")


# Second
instructions = deepcopy(original_instructions)
canvas = Canvas()
relative_base = [0]
inputs = [1]
outputs = []

i = 0
while i >= 0:
    i = execute(instructions, i, inputs,
                output=outputs,
                relative_base=relative_base,
                no_print=True)

    if len(outputs) == 2:
        inputs.append(canvas.paint(tuple(outputs)))
        outputs.clear()

print(f"[2]")
canvas.display_image()
