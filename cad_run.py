# %%
from build123d import *
from ocp_vscode import *

from HexPlant import HexPlant

set_port(3939)

set_defaults(reset_camera=Camera.CENTER, helper_scale=5)
show_clear()
import random

nx = 16
ny = 16
hex = HexPlant(nx, ny)
number_lines = 8
lines = []
for i in range(0, number_lines + 1):
    x = random.randint(0, int(nx / 4))
    y = random.randint(0, int(ny / 4))
    start = random.choice([(x, int(ny / 4)), (int(nx / 4), y)])
    lines.append(hex.grow_line(start[0], start[1], 50))
line = lines[0]
# line = [(10, 0), (10, 10), (0, 10)]
line_converted = [
    hex.convert_point_to_hexagonal(point[0], point[1], 100) for point in line
]
# line_converted = [(10, 0), (10, 10), (0, 10)]

all_lines = []
all_circles = []
with BuildPart() as branches:
    for line in lines:
        line_converted = [
            hex.convert_point_to_hexagonal(point[0], point[1], 100) for point in line
        ]
        # print(line_converted)
        with BuildLine() as ex1_ln:
            l = Polyline(line_converted)
        all_lines += ex1_ln.line

        z_dir = (
            line_converted[1][0] - line_converted[0][0],
            line_converted[1][1] - line_converted[0][1],
        )

        plane = Plane(origin=line_converted[0], z_dir=l % 0)

        with BuildSketch(plane) as rectangleSK:
            Circle(1)
        all_circles += branches.pending_faces
        sweep(transition=Transition.ROUND)

show_object(all_lines)
show_object(all_circles)
# for i, line in enumerate(all_lines):
#     show_object(line, name="line" + str(i))

# for i, circle in enumerate(all_circles):
#     show_object(circle, name="circle" + str(i))
show_object(branches.part)
# show_all()


# %%
