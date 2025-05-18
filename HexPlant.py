import random

from math import sqrt
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
        self.current_edges = self.init_edges()

    def init_edges(self):
        current_edges = []
        for y in range(0, self.ny):
            current_edges.append([])
            for x in range(0, self.nx):
                current_edges[y].append([False, False, False, False, False, False])
        return current_edges

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
                    # Only if edge points inside the grid (exclude boundary)
                    if (
                        (x + i[0] >= 0)
                        and (y + i[1] >= 0)
                        and (x + i[0] < self.nx)
                        and (y + i[1] < self.ny)
                    ):
                        probs[y][x][n] = 1
                        # General direction should be right
                        if n == 0 or n == 1 or n == 2 or n == 5:
                            probs[y][x][n] = 50
                if y == self.ny - 1:
                    probs[y][x] = [0, 0, 0, 0, 0, 0]
                if x == self.nx - 1:
                    probs[y][x] = [0, 0, 0, 0, 0, 0]
        return probs

    def _get_existing_prob(self, current):
        # Increaase probability for existing edges
        probs = [1, 1, 1, 1, 1, 1]
        current_x = current[0]
        current_y = current[1]
        for i in range(0, 6):
            if self.current_edges[current_y][current_x][i]:
                probs[i] = 2
        return probs

    def _probs_without_triangles(self, current):
        """
        Checks every possible edge.
        If an edge would produce an triangle that edge will be eliminated

        TODO optimize such that not all edges get checked
        """
        probs = [1, 1, 1, 1, 1, 1]
        current_x = current[0]
        current_y = current[1]
        is_current_row_odd = current[1] % 2

        for i in range(0, 6):
            # Check edge before
            index_before = (i - 1) % 6
            if self.current_edges[current_y][current_x][index_before]:
                next_dir = self.indices[is_current_row_odd][index_before]
                next_x = current[0] + next_dir[0]
                next_y = current[1] + next_dir[1]
                # Symmetry yields that if previous edge was edge 0, then the triangle completing edge
                # is edge 2 from the pov of the end point of the previous edge
                searched_edge = (index_before + 2) % 6
                if self.current_edges[next_y][next_x][searched_edge]:
                    probs[i] = 0

            # Check edge after
            index_after = (i + 1) % 6
            if self.current_edges[current_y][current_x][index_after]:
                # Same as before, but index_before is now i
                next_dir = self.indices[is_current_row_odd][i]
                next_x = current[0] + next_dir[0]
                next_y = current[1] + next_dir[1]
                # Symmetry yields that if previous edge was edge 0, then the triangle completing edge
                # is edge 2 from the pov of the end point of the previous edge
                searched_edge = (i + 2) % 6
                if self.current_edges[next_y][next_x][searched_edge]:
                    probs[i] = 0
        return probs

    def _get_dynamic_prob(self, previous, current, static_probs):
        last_edge = (current[0] - previous[0], current[1] - previous[1])
        # This means that no sharp angles are tolarated (with respect to the previous edge)
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
        last_edge_index = self.indices[odd_row].index(last_edge)
        probs = probs_for_indices[last_edge_index]
        dyn_props = list(map(mul, probs, static_probs))

        return dyn_props

    def grow_line(self, x, y, n):
        current_x = x
        current_y = y
        line = [(x, y)]
        probs = self.probs[current_y][current_x]
        for i in range(0, n):
            is_current_row_odd = current_y % 2

            if i >= 1:
                probs = self._get_dynamic_prob(
                    line[-2], (current_x, current_y), self.probs[current_y][current_x]
                )

            without_triangles = self._probs_without_triangles((current_x, current_y))

            probs = list(map(mul, probs, without_triangles))

            if sum(probs) < 0.1:
                # print("Breaking because probs are to small")
                break

            next_index = random.choices([0, 1, 2, 3, 4, 5], weights=probs)[0]
            reversed_index = (next_index + 3) % 6
            next = self.indices[is_current_row_odd][next_index]
            self.current_edges[current_y][current_x][next_index] = True
            current_x = current_x + next[0]
            current_y = current_y + next[1]

            self.current_edges[current_y][current_x][reversed_index] = True
            line.append((current_x, current_y))
        return line

    def convert_point_to_hexagonal(self, x, y, scale=1.0):
        """
        scale=1.0 means the longest side is 1.0 units long
        """
        n_max = max(self.nx, self.ny)
        point_x = x / (n_max - 1)
        point_y = (y * sqrt(3) * 0.5) / (n_max - 1)
        if y % 2:
            point_x = (x + 0.5) / (n_max - 1)

        return (point_x * scale, point_y * scale)

    def getGrid(self):
        conv_point = []
        for x in range(0, self.nx):
            for y in range(0, self.ny):
                conv_point.append(self.convert_point_to_hexagonal(x, y))
        return conv_point
