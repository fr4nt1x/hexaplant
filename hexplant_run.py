import cairo
import random
from math import pi
from HexPlant import HexPlant


def printDot(cx, x, y):
    cx.arc(
        x,
        y,
        0.0005,
        0,
        2 * pi,
    )
    cx.stroke()


def printRedDot(cx, x, y):
    cx.set_source_rgb(1, 0, 0)
    cx.arc(
        x,
        y,
        0.0015,
        0,
        2 * pi,
    )
    cx.stroke()
    cx.set_source_rgb(1, 1, 1)


def reduce_lines(lines):
    edges = []
    for line in lines:
        last_point = line[0]
        for point in line[1:]:
            edge = {point, last_point}
            if edge not in edges:
                edges.append(edge)
            last_point = point

    return edges


if __name__ == "__main__":
    line_width = 0.001
    nx = 8
    ny = 16
    hex = HexPlant(nx, ny)
    number_lines = 16
    lines = []
    start_x = int(nx / 2)
    start_y = int(ny / 2)
    for i in range(0, number_lines + 1):
        x = random.randint(0, start_x)
        y = random.randint(0, start_y)
        start = random.choice([(x, start_y), (start_x, y)])
        lines.append(hex.grow_line(start[0], start[1], 50))

    # edges = reduce_lines(lines)

    with cairo.SVGSurface("./example.svg", 1200, 1200) as surface:
        cx = cairo.Context(surface)
        cx.scale(1000, 1000)
        cx.set_source_rgb(1, 1, 1)
        cx.set_line_width(line_width)

        grid = hex.getGrid()

        for point in grid:
            printDot(cx, point[0], point[1])

        for line in lines:
            print(f"Start: {line[0]}")
            print(f"Line: {line}")
            start = hex.convert_point_to_hexagonal(line[0][0], line[0][1])
            printRedDot(cx, start[0], start[1])
            for point in line:
                conv_point = hex.convert_point_to_hexagonal(point[0], point[1])
                cx.line_to(conv_point[0], conv_point[1])
            cx.stroke()
