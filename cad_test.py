# %%
from build123d import *
from ocp_vscode import *

from hexplant import HexPlant

set_port(3939)

set_defaults(reset_camera=Camera.CENTER, helper_scale=5)
import random

nx = 16
ny = 16
hex = HexPlant(nx, ny)
number_lines = 10
lines = []
for i in range(0, number_lines + 1):
    x = random.randint(0, nx / 4)
    y = random.randint(0, ny / 4)
    start = random.choice([(x, int(ny / 4)), (int(nx / 4), y)])
    lines.append(hex.grow_line(start[0], start[1], 50))
line = lines[0]
# line = [(10, 0), (10, 10), (0, 10)]
line_converted = [
    hex.convert_point_to_hexagonal(point[0], point[1], 100) for point in line
]
# line_converted = [(10, 0), (10, 10), (0, 10)]
print(line_converted)
# for line in lines:
#     line_converted = [
#         hex.convert_point_to_hexagonal(point[0], point[1]) for point in line
#     ]

with BuildPart() as ex1:
    with BuildLine() as ex1_ln:
        l = Polyline(line_converted)
    z_dir = (
        line_converted[1][0] - line_converted[0][0],
        line_converted[1][1] - line_converted[0][1],
    )
    plane = Plane(origin=line_converted[0], z_dir=z_dir)
    with BuildSketch(plane) as rectangleSK:
        Circle(2)
    sweep(transition=Transition.ROUND)
show_all()

# %%

a, b = 40, 20

with BuildPart() as ex14:
    with BuildLine() as ex14_ln:
        l1 = JernArc(start=(0, 0), tangent=(0, 1), radius=a, arc_size=180)
        l2 = JernArc(start=l1 @ 1, tangent=l1 % 1, radius=a, arc_size=-90)
        l3 = Line(l2 @ 1, l2 @ 1 + (-a, a))
    with BuildSketch(Plane.XZ) as ex14_sk:
        Rectangle(b, b)
    sweep()

show_all()
# %%
