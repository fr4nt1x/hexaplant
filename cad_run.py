# %%
from build123d import *
from ocp_vscode import *

from HexPlant import HexPlant

set_port(3939)

set_defaults(reset_camera=Camera.CENTER, helper_scale=5)
show_clear()
import random


nx = 8
ny = 16
n_max = max(nx, ny)
scaling = 100.0
hex_side_length = scaling / (n_max - 1)
radius = hex_side_length / 6.0
print(f"Side Length: {hex_side_length}")
print(f"Radius: {radius}")
print(radius)
hex = HexPlant(nx, ny)
number_lines = 1
lines = []
start_x = int(nx / 2)
start_y = int(ny / 2)
start_hex = hex.convert_point_to_hexagonal(start_x, start_y, scaling)
start_hex_x = start_hex[0]
start_hex_y = start_hex[1]

outline_points_closed = [
    (0, 0),
    (start_x + int((nx / 4)), 0),
    (start_x - 1, start_y),
    (0, start_y + 2),
    (0, 0),
]
outline_solid = [
    hex.convert_point_to_hexagonal(point[0], point[1], scaling)
    for point in outline_points_closed
]

# lines.append(outline_points_closed)
for i in range(0, number_lines + 1):
    x = random.randint(0, start_x)
    y = random.randint(0, start_y)
    start = random.choice([(x, start_y), (start_x, y)])
    lines.append(hex.grow_line(start[0], start[1], 50))

all_lines = []
all_circles = []
with BuildPart() as branches:
    with BuildSketch() as base_sketch:
        with BuildLine() as line:

            Polyline(
                outline_solid,
            )
        make_face()
        # Rectangle(start_hex_x, start_hex_y)

    extrude(amount=radius, both=True)  # Create a base block

    for line in lines:
        line_converted = [
            hex.convert_point_to_hexagonal(point[0], point[1], 100) for point in line
        ]

        with BuildLine() as ex1_ln:
            l = Polyline(line_converted)
        all_lines += ex1_ln.line

        circles = []
        for i, point in enumerate(line_converted):
            if i == 0:
                continue
            previous_i = i - 1

            z_dir = (
                line_converted[i][0] - line_converted[previous_i][0],
                line_converted[i][1] - line_converted[previous_i][1],
            )

            plane = Plane(origin=line_converted[previous_i], z_dir=z_dir)

            with BuildSketch(plane, mode=Mode.PRIVATE) as circleSK:
                Circle(radius + 2 * i)
            circles += circleSK.sketch.faces()
            print("loop")
        all_circles += circles
        print(circles)
        sweep(path=ex1_ln.line, sections=circles, multisection=True)

export_step(branches.part, "branches.stp")

show_object(all_lines, clear=True)
show_object(all_circles)
# for i, line in enumerate(all_lines):
#     show_object(line, name="line" + str(i))

# for i, circle in enumerate(all_circles):
#     show_object(circle, name="circle" + str(i))
show_object(branches.part)

# show_all()


# %%

# %%

# %%

# %%

# %%
