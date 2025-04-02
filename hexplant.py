import cairo
import random
from math import pi, sqrt
from operator import mul


class HexPlant:
    def __init__(self, nx, ny):
        self.nx = nx
        self.ny = ny
        #
        self.indices = [
            # y %2 = 0
            #       0   0   1   1   2   2
            #   ________________________________
            # 0|        4       5       *
            #
            # 1|    3       X       0
            #
            # 2|        2       1       *
            #
            # 3|    *       *       *
            [
                (1, 0),  # 0
                (0, 1),  # 1
                (-1, 1),  # 2
                (-1, 0),  # 3
                (-1, -1),  # 4
                (0, -1),  # 5
            ],
            # y %2 = 1
            #       0   0   1   1   2   2
            #   ________________________________
            # 0|        *       *       *
            #
            # 1|    *       4       5
            #
            # 2|        3       X       0
            #
            # 3|    *       2       1
            [
                (1, 0),  # 0
                (1, 1),  # 1
                (0, 1),  # 2
                (-1, 0),  # 3
                (0, -1),  # 4
                (1, -1),  # 5
            ],
        ]
        #             *       4      5
        #
        #                 3      X      0
        #
        #             *       2      1
        #
        self.probs = self.init_probs()

    def init_probs(self):
        probs = []
        for y in range(0, self.ny):
            probs.append([])
            for x in range(0, self.nx):
                probs[y].append([0, 0, 0, 0, 0, 0])

        for x in range(0, self.nx):
            for y in range(0, self.ny):
                odd_row = y % 2
                for n, i in enumerate(self.indices[odd_row]):
                    if (
                        (x + i[0] >= 0)
                        and (y + i[1] >= 0)
                        and (x + i[0] < self.nx)
                        and (y + i[1] < self.ny)
                    ):
                        probs[y][x][n] = 1
                        # General direction should be bottom right
                        if n == 0 or n == 1 or n == 2:
                            probs[y][x][n] = 50
                if y == self.ny - 1:
                    probs[y][x] = [0, 0, 0, 0, 0, 0]
                if x == self.nx - 1:
                    probs[y][x] = [0, 0, 0, 0, 0, 0]
        return probs

    def _get_dynamic_prob(self, previous, current, static_probs):
        distance = (current[0] - previous[0], current[1] - previous[1])
        probs_for_indices = [
            [1, 1, 0, 0, 0, 1],
            [1, 1, 1, 0, 0, 0],
            [0, 1, 1, 1, 0, 0],
            # dont go back to top would be [0, 0, 1, 1, 0.1, 0]
            [0, 0, 1, 1, 1, 0],
            [0, 0, 0, 1, 1, 1],
            [1, 0, 0, 0, 1, 1],
        ]
        odd_row = previous[1] % 2
        index_in_indices = self.indices[odd_row].index(distance)
        probs = probs_for_indices[index_in_indices]
        dyn_props = list(map(mul, probs, static_probs))
        return dyn_props

    def grow_line(self, x, y, n):
        current_x = x
        current_y = y
        line = [(x, y)]
        probs = self.probs[current_y][current_x]
        for i in range(0, n):
            current_odd_row = current_y % 2
            if i >= 1:
                probs = self._get_dynamic_prob(
                    line[-2], (current_x, current_y), self.probs[current_y][current_x]
                )
            if sum(probs) < 0.1:
                break
            next = random.choices(self.indices[current_odd_row], weights=probs)[0]
            current_x = current_x + next[0]
            current_y = current_y + next[1]
            line.append((current_x, current_y))
        return line

    def convert_point_to_hexagonal(self, x, y, scale=1.0):
        point_x = x / self.nx
        point_y = (y * sqrt(3) * 0.5) / self.ny
        if y % 2:
            point_x = (x + 0.5) / self.nx

        return (point_x * scale, point_y * scale)

    def printGrid(self, cx):
        for x in range(0, self.nx):
            for y in range(0, self.ny):
                conv_point = hex.convert_point_to_hexagonal(x, y)
                self.printDot(cx, conv_point[0], conv_point[1])

    def printDot(self, cx, x, y):
        cx.arc(
            x,
            y,
            0.0005,
            0,
            2 * pi,
        )
        cx.stroke()

    def printRedDot(self, cx, x, y):
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

    edges = reduce_lines(lines)
    with cairo.SVGSurface(
        "/home/bebe/Code/hexplant/example.svg", 1200, 1200
    ) as surface:
        cx = cairo.Context(surface)
        cx.scale(1000, 1000)
        cx.set_source_rgb(1, 1, 1)
        cx.set_line_width(line_width)
        hex.printGrid(cx)
        for edge in edges:
            print(f"Start: {line[0]}")
            print(f"Line: {line}")
            start = hex.convert_point_to_hexagonal(line[0][0], line[0][1])
            hex.printRedDot(cx, start[0], start[1])
            for point in line:
                conv_point = hex.convert_point_to_hexagonal(point[0], point[1])
                cx.line_to(conv_point[0], conv_point[1])
            cx.stroke()
