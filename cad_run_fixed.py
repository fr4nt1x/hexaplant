# %%
from build123d import *
from ocp_vscode import *

from HexPlant import HexPlant

set_port(3939)

set_defaults(reset_camera=Camera.CENTER, helper_scale=5)
show_clear()
import random

random.seed(42)
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
number_lines = 2
lines = []
start_x = int(nx / 2)
start_y = int(ny / 2)
start_hex = hex.convert_point_to_hexagonal(start_x, start_y, scaling)
start_hex_x = start_hex[0]
start_hex_y = start_hex[1]

# lines.append(outline_points_closed)
for i in range(0, number_lines + 1):
    x = random.randint(0, start_x)
    y = random.randint(0, start_y)
    start = random.choice([(x, start_y), (start_x, y)])
    lines.append(hex.grow_line(start[0], start[1], 50))

all_lines = []
all_circles = []
all_parts = []
for line in lines:
    line_converted = [
        hex.convert_point_to_hexagonal(point[0], point[1], 100) for point in line
    ]
    with BuildPart() as branch_part:

        with BuildLine() as line_l:
            l = Polyline(line_converted)
        all_lines += line_l.line

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
                Circle(radius)
            circles += circleSK.sketch.faces()
        # Last circle
        plane = Plane(origin=l @ 1, z_dir=l % 1)
        with BuildSketch(plane, mode=Mode.PRIVATE) as circleSK:
            Circle(radius)
        circles += circleSK.sketch.faces()

        all_circles += circles
        print("Sweep")
        sweep(sections=circles, multisection=True, transition=Transition.ROUND)
    all_parts += branch_part.part

# export_step(branches.part, "branches.stp")

show_object(all_parts, clear=True)
show_object(all_lines)
show_object(all_circles)
# for i, line in enumerate(all_lines):
#     show_object(line, name="line" + str(i))

# for i, circle in enumerate(all_circles):
#     show_object(circle, name="circle" + str(i))
# show_all()
