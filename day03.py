import re

input_splitter = re.compile(r",\s*")


def load(path: str = "input/03.txt"):
    to_return = list()

    with open(path) as file:
        for line in file.readlines():
            line = input_splitter.split(line.strip())

            to_return.append(list())

            for entry in line:
                to_return[-1].append((entry[0], int(entry[1:])))

    return to_return


def get_direction_vector(direction):
    horizontal_movement = 1 if direction == "R" else -1 if direction == "L" else 0
    vertical_movement = 1 if direction == "U" else -1 if direction == "D" else 0

    return horizontal_movement, vertical_movement


def manhattan(first, second=(0, 0)):
    return abs(first[0] - second[0]) + abs(first[1] - second[1])


def delay_manhattan(intersection, timings):
    return sum([timings[x][intersection] for x in range(len(timings))])


def place_wire(platform, wire, wire_index):
    collisions = set()
    timings = dict()

    current_point = (0, 0)
    time_alive = 0

    for direction, amount in wire:
        direction = get_direction_vector(direction)

        for _ in range(amount):
            current_point = (current_point[0] + direction[0], current_point[1] + direction[1])
            time_alive += 1

            if current_point not in platform:
                platform[current_point] = wire_index
            elif current_point != (0, 0) and platform[current_point] != wire_index:
                collisions.add(current_point)

            if current_point not in timings:
                timings[current_point] = time_alive

    return collisions, timings


wires = load()

panel = dict()
intersections = set()
timing_list = list()

for i, wire_steps in enumerate(wires):
    collided, timed = place_wire(panel, wire_steps, i)

    intersections.update(collided)
    timing_list.append(timed)

# First
intersection_manhattan = sorted([(x, manhattan(x)) for x in intersections], key=lambda x: x[1])

# Second
intersection_delay = sorted([(x, delay_manhattan(x, timing_list)) for x in intersections], key=lambda x: x[1])

print(f"[1]\t{intersection_manhattan[0][1]}")
print(f"[2]\t{intersection_delay[0][1]}")
