import numpy as np

image_dimensions = (25, 6)


def load(image_dims, path: str = "input/8.txt"):
    with open(path) as file:
        return np.array([c for c in file.read()]).reshape((-1, image_dims[0] * image_dims[1]))


def number_of_values_in_layer(layer, value):
    return np.count_nonzero(layer == value)


def stack_layers(image_layers):
    final_layer = list()

    for i in range(len(image_layers[0])):
        for j in range(len(image_layers)):
            if image_layers[j][i] != "2":
                final_layer.append(image_layers[j][i])
                break

    return np.array(final_layer)


# Prep
layers = load(image_dimensions)

# First
wanted_layer = None
minimum = None

for l in layers:
    n = number_of_values_in_layer(l, "0")

    if minimum is None or wanted_layer is None or n < minimum:
        minimum = n
        wanted_layer = l

wanted_1 = number_of_values_in_layer(wanted_layer, "1") * number_of_values_in_layer(wanted_layer, "2")
print(f"[1]\t{wanted_1}")

# Second
stacked_layer = stack_layers(layers).reshape(image_dimensions[::-1])
final_image = list()

for row in stacked_layer:
    r = ""

    for element in row:
        r += "##" if element == "1" else "  " if element == "0" else "  "

    final_image.append(r)

print(f"[2]:")
for r in final_image:
    print(r)
