from copy import deepcopy
import re

input_splitter = re.compile(r"\)")


def load(path: str = "input/06.txt"):
    with open(path) as file:
        lines = filter(lambda x: len(x) != 0, [input_splitter.split(z.strip()) for z in file.readlines()])
        return set((x, y) for x, y in lines)


def build_orbit_hierarchy(orbit_pairs, root="COM", stopping_planet=None):
    orbit_pairs = deepcopy(orbit_pairs)
    hierarchy = [{root}]

    while len(hierarchy[-1]) != 0:
        for i in range(len(hierarchy)):
            centers = hierarchy[-1]

            if len(centers) != 0:
                orbiter_pairs = set()
                orbiter_pairs_reverse = set()

                for o_p in orbit_pairs:
                    if o_p[0] in centers:
                        orbiter_pairs.add(o_p)
                    elif o_p[1] in centers:
                        orbiter_pairs_reverse.add(o_p)

                for orbiter_pair in orbiter_pairs | orbiter_pairs_reverse:
                    orbit_pairs.remove(orbiter_pair)

                orbiter_pairs_reverse = set(map(lambda x: x[::-1], orbiter_pairs_reverse))

                hierarchy.append(set(map(lambda x: x[1], orbiter_pairs | orbiter_pairs_reverse)))

                if stopping_planet is not None and stopping_planet in hierarchy[-1]:
                    return hierarchy
            else:
                break

    return hierarchy


def orbit_checksum(orbit_pairs, root="COM"):
    hierarchy = build_orbit_hierarchy(orbit_pairs, root)
    return sum(list(map(lambda i: i * len(hierarchy[i]), range(1, len(hierarchy)))))


def minimum_distance(orbit_pairs, source="YOU", destination="SAN"):
    hierarchy = build_orbit_hierarchy(orbit_pairs, source, destination)

    # YOU, SAN and the SAN's center of mass.
    # This is basically YOU + [0, n] + SAN, which has 1 + (n + 1) + 1 elements.
    return len(hierarchy) - 3


# Prep
orbits = load()

# First
print(f"[1]\t{orbit_checksum(orbits)}")

# Second
print(f"[2]\t{minimum_distance(orbits)}")
