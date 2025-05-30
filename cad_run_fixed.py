# %%

from build123d import *
from ocp_vscode import *

from HexPlant import HexPlant

set_port(3939)

set_defaults(reset_camera=Camera.CENTER, helper_scale=5)
show_clear()
import random
import sys
from itertools import product

seed = random.randrange(sys.maxsize)
random.seed(283662149582336880)

print("Seed was:", seed)

# random.seed(43)
tol = 0.0001
shorting_factor = 0.1

nx = 16
ny = 32
n_max = max(nx, ny)
scaling = 100.0

hex_side_length = scaling / (n_max - 1)
radius = hex_side_length / 4.0

max_radius = 0.3 * radius
random_grid = 0.1
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

outline_points_closed = [
    (0, 0),
    (start_x + int((nx / 4)), 0),
    (start_x - 1, start_y),
    (int(nx / 2) - 3, ny - 1),
    (0, ny - 1),
    (0, 0),
]

outline_solid = [
    hex.convert_point_to_hexagonal(point[0], point[1], scaling)
    for point in outline_points_closed
]


# lines.append(outline_points_closed)
possible_starts = list(product(range(1, start_x), range(1, start_y)))


for i in range(0, number_lines + 1):

    start = random.choice(possible_starts)
    lines.append(hex.grow_line(start[0], start[1], 50))

all_lines = []
all_lines_private = []
all_circles = []
all_paths = []
all_planes = []
all_parts = []


## Outline
with BuildPart() as outline_p:
    with BuildSketch() as outline_sk:
        with BuildLine() as outline_l:
            FilletPolyline(outline_solid, radius=2)
        make_face()
        offset(amount=max_radius + hex_side_length*random_grid )
        # Rectangle(start_hex_x, start_hex_y)

    extrude(amount=radius - 0.2, both=True)  # Create a base block

outline_p.part.label = "outline"
all_parts.append(outline_p.part)


## Lines
for line_index, line in enumerate(lines):
    scaling = 100
    line_converted = [
        hex.convert_point_to_hexagonal(point[0], point[1], scaling, random_grid)
        for point in line
    ]

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
        all_lines_private += section_lines
        obj_to_add = []
        for i in range(0, len(section_lines) - 1):
            section_line = section_lines[i]

            next_section_line = section_lines[i + 1]
            next_line_tangent = next_section_line % 0
            line_tangent = section_line % 1

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
        obj_to_add.append(section_lines[-1])
        add(obj_to_add)
        path = Wire.combine(branch_part.pending_edges)[0]
        all_paths.append(path)
        all_lines += obj_to_add

        circles = []

        segment_count = 12
        rotation = 0  #
        start_radius = radius + random.uniform(-max_radius, max_radius)
        for i in range(segment_count + 1):
            plane = Plane(
                origin=path @ (i / segment_count),
                z_dir=path % (i / segment_count),
                x_dir=(
                    0,
                    0,
                    1,
                ),  # Needed as the path seems to have random orientation otherwise
            )

            all_planes.append(plane)
            with BuildSketch(plane) as circleSK:
                RegularPolygon(
                    start_radius - i * 0.025 * start_radius, 6, rotation=rotation
                )
                rotation += 17
                rotation = rotation % 360

            circles += circleSK.sketch.faces()
        all_circles += circles

        sweep(sections=(circles), multisection=True)

    branch_part.part.label = f"branch_{line_index}"
    all_parts.append(branch_part.part)

box_assembly = Compound(label=f"compound_{seed}", children=[x for x in all_parts])

print(box_assembly.show_topology())
export_step(box_assembly, f"branches.stp")

show_object(box_assembly, name="branches", clear=True)
show_object(all_paths, name="all_paths")
# show_object(all_planes, name="all_planes")
# show_object(all_lines, name="lines")
# show_object(all_lines_private, name="lines private")

show_object(all_circles, name="circles")
