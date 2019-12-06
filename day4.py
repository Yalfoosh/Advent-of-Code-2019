from copy import deepcopy
import re

input_splitter = re.compile(r"\s*-\s*")


def load(path: str = "input/4.txt"):
    with open(path) as file:
        return input_splitter.split(file.read().strip())


def number_string_to_int_vector(number_string):
    return [int(x) for x in number_string]


def find_lower_bound(vector):
    to_return = deepcopy(vector)

    for i in range(1, len(vector)):
        to_return[i] = max(to_return[i], to_return[i - 1])

    return to_return


def vector_leq(lhs, rhs):
    for i in range(len(lhs)):
        if lhs[i] > rhs[i]:
            return False
        elif lhs[i] < rhs[i]:
            return True

    return True


def vector_inc(vector):
    current_index = len(vector) - 1

    if vector[current_index] == 9:
        current_index -= 1

        while vector[current_index] == 9 and current_index > 0:
            current_index -= 1

        vector[current_index] += 1

        for i in range(current_index + 1, len(vector)):
            vector[i] = vector[current_index]
    else:
        vector[current_index] += 1


def first_check(vector):
    valid = False

    for i in range(1, len(vector)):
        if vector[i] == vector[i - 1]:
            valid = True
        elif vector[i] < vector[i - 1]:
            return False

    return valid


def second_check(vector):
    min_count = len(vector)

    i = 1
    while i < len(vector):
        if vector[i] == vector[i - 1]:
            current_count = 2

            i += 1

            while i < len(vector) and vector[i] == vector[i - 1]:
                current_count += 1
                i += 1

            min_count = min(min_count, current_count)
        elif vector[i] < vector[i - 1]:
            return False
        else:
            i += 1

    return min_count == 2


def count_rule_abiding(a, b, is_valid):
    current = find_lower_bound(a)
    n = 0

    while vector_leq(current, b):
        if is_valid(current):
            n += 1

        vector_inc(current)

    return n


# Prep
number_range = tuple(number_string_to_int_vector(x) for x in load())

# First and second
print(f"[1]\t{count_rule_abiding(*number_range, first_check)}")
print(f"[2]\t{count_rule_abiding(*number_range, second_check)}")
