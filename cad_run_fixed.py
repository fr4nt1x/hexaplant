# %%
from build123d import *
from ocp_vscode import *

from HexPlant import HexPlant

set_port(3939)

set_defaults(reset_camera=Camera.CENTER, helper_scale=5)
show_clear()
import random

random.seed(43)
tol = 0.0001
shorting_factor = 0.1

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
number_lines = 16
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
    # print(line)
    # print(line_converted)

    with BuildPart() as branch_part:
        section_lines = []
        for i, end_point in enumerate(line_converted):
            # print("Point", i, end_point)
            # Always need three points for two sections
            if i == 0:
                continue
            start_point = line_converted[i - 1]

            # print("duple:", start_point, end_point)
            with BuildLine(mode=Mode.PRIVATE) as line_l:
                l1 = Line(start_point, end_point)
            section_lines += line_l.edges()
        # all_lines += section_lines
        obj_to_add = []
        for i in range(0, len(section_lines) - 1):
            section_line = section_lines[i]

            next_section_line = section_lines[i + 1]
            next_line_tangent = next_section_line % 0
            line_tangent = section_line % 1

            tangen_diff: Vector = line_tangent - next_line_tangent
            angle = line_tangent.get_angle(next_line_tangent)

            with BuildLine(mode=Mode.PRIVATE) as path_l:
                if angle <= tol:
                    obj_to_add.append(section_line)
                else:
                    l1 = Line(section_line @ 0, section_line @ (1 - shorting_factor))
                    obj_to_add.append(l1)
                    section_lines[i + 1] = Line(
                        next_section_line @ shorting_factor, next_section_line @ 1
                    )
                    spline = Spline(
                        l1 @ 1,
                        section_lines[i + 1] @ 0,
                        tangents=[l1 % 1, section_lines[i + 1] % 0],
                    )
                    obj_to_add.append(spline)
        add(obj_to_add)
        all_lines += obj_to_add
        circles = []

        # First circle
        plane = Plane(origin=section_lines[0] @ 0, z_dir=section_lines[0] % 0)
        with BuildSketch(plane) as circleSK:
            Circle(radius)
        circles += circleSK.sketch.faces()
        all_circles += circles
        sweep(transition=Transition.ROUND)
    all_parts += branch_part.part

# export_step(branches.part, "branches.stp")

show_object(all_parts, name="branches", clear=True)
show_object(all_lines, name="lines")

show_object(all_circles, name="circles")
# for i, line in enumerate(all_lines):
#     show_object(line, name="line" + str(i))

# for i, circle in enumerate(all_circles):
#     show_object(circle, name="circle" + str(i))
# show_all()
