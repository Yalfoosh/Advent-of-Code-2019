import numpy as np
from typing import Tuple

asteroid_to_bet = 200
x_multiplier = 100

pi = np.angle(-1)
pi2 = pi + pi


def load(path: str = "input/10.txt"):
    with open(path) as file:
        return [[1 if element == "#" else 0 for element in line.strip()] for line in file.readlines()]


def asteroid_vector(coordinate_1, coordinate_2):
    return coordinate_2[0] - coordinate_1[0], coordinate_2[1] - coordinate_1[1]


# noinspection PyTypeChecker
def asteroid_direction(coordinate_1, coordinate_2):
    vector = asteroid_vector(coordinate_1, coordinate_2)
    t_angle = np.angle(complex(*vector))

    while t_angle < 0:
        t_angle += pi2

    return t_angle


def get_asteroid_coordinates(asteroid_map):
    to_return = set()

    for j in range(len(asteroid_map)):
        for i in range(len(asteroid_map[j])):
            if asteroid_map[j][i] == 1:
                to_return.add((i, j))

    return to_return


def get_asteroid_angle_map(asteroid_coordinates):
    to_return = {asteroid_coordinate: dict() for asteroid_coordinate in asteroid_coordinates}

    for asteroid_c in to_return:
        angle_dict = dict()

        for other_asteroid_c in asteroid_coordinates:
            if asteroid_c == other_asteroid_c:
                continue

            angle = asteroid_direction(asteroid_c, other_asteroid_c)

            if angle not in angle_dict:
                angle_dict[angle] = set()

            angle_dict[angle].add(other_asteroid_c)

        to_return[asteroid_c] = angle_dict

    return to_return


def get_most_observant_asteroid(asteroid_map):
    keys = list(asteroid_map.keys())
    best = keys[0]

    for i in range(1, len(keys)):
        if len(asteroid_map[keys[i]]) > len(asteroid_map[best]):
            best = keys[i]

    return best


# noinspection PyTypeChecker
def get_asteroid_vaporization_order(vaporization_source: Tuple[int, int], asteroid_map,
                                    starting_angle: float = np.angle(-1j), clockwise: bool = True):
    vaporization_map = asteroid_map[vaporization_source]

    # Make sure we're dealing with positive radians.
    while starting_angle < 0:
        starting_angle += pi2

    angle_to_asteroids_pairs = [(angle, asteroid_set) for angle, asteroid_set in vaporization_map.items()]
    angle_ordered_asteroids = sorted(angle_to_asteroids_pairs, key=lambda pair: pair[0])

    # Find the first hit.
    i = 0
    while i < len(angle_ordered_asteroids) and angle_ordered_asteroids[i][0] < starting_angle:
        i += 1

    # If this is going clockwise, we went 1 too far from our starting i (the difference between our starting angle and
    # the first angle we chose must be positive, but in this case, since it is natural to look at the default direction
    # as counter-clockwise, it will be negative.
    if clockwise and starting_angle != angle_ordered_asteroids[i][0]:
        if i == 0:
            i = len(angle_ordered_asteroids)

        i -= 1

    angle_ordered_asteroids = list(map(lambda x: x[1], angle_ordered_asteroids[i:] + angle_ordered_asteroids[:i]))

    # Although our collisions are sorted in a correct way, the same-angle asteroids aren't sorted to accommodate for
    # the distance from the vaporization source. In Python3 cmp was removed so we have to experience a bit of pain.
    for i in range(len(angle_ordered_asteroids)):
        angle_ordered_asteroids[i] = sorted([(x, sum([abs(y) for y in asteroid_vector(vaporization_source, x)]))
                                             for x in angle_ordered_asteroids[i]], key=lambda x: x[1])
        angle_ordered_asteroids[i] = [x[0] for x in angle_ordered_asteroids[i]]

    # If we're going counter clockwise, since the whole mapping is flipped around the x-axis, we have to reverse the
    # order of our same-angle collision groups, but keep the first collision the same.
    if not clockwise:
        angle_ordered_asteroids = [angle_ordered_asteroids[0]] + angle_ordered_asteroids[1:][::-1]

    asteroid_vaporization_order = list()

    max_depth = max([len(x) for x in angle_ordered_asteroids])
    current_depth = 0

    while current_depth < max_depth:
        for asteroid_set in angle_ordered_asteroids:
            if current_depth < len(asteroid_set):
                asteroid_vaporization_order.append(asteroid_set[current_depth])

        current_depth += 1

    return asteroid_vaporization_order


def asteroid_function(coordinates: Tuple[int, int]):
    return coordinates[0] * x_multiplier + coordinates[1]


# Prep
asteroids = load()
asteroid_coords = get_asteroid_coordinates(asteroids)
asteroid_mapping = get_asteroid_angle_map(asteroid_coords)


# First
best_coordinate = get_most_observant_asteroid(asteroid_mapping)
print(f"[1]\t{len(asteroid_mapping[best_coordinate])} (most observant asteroid is at {best_coordinate})")


# Second
asteroid_vaporizations = get_asteroid_vaporization_order(best_coordinate, asteroid_mapping)
bet_coordinates = asteroid_vaporizations[asteroid_to_bet - 1]

print(f"[2]\t{asteroid_function(bet_coordinates)} (asteroid that was bet on is at {bet_coordinates})")
