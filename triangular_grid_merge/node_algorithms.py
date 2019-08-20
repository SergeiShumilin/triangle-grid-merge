"""The module provides functionality to merge a zone into grid
comparing nodes coordinates."""

from math import fabs

# Accuracy to compare nodes' coordinates.
EPS = 10e-5


def n_square_algorithm(grid, nodes):
    """
    Compose grid.Nodes from the nodes from zones to avoid repeating.

    If some nodes in grid are shared between several zones, the task is
    to avoid including one particular node twice to the grid.

    The nodes are compared according to their coordinates (x, y).
    The algorithm does simple n^2 search through all nodes.

    :param grid: Grid object.
    :param nodes: list: nodes of zone to add to the grid.
    """
    for i in range(len(nodes)):

        node_is_found = False

        for j in range(len(grid.Nodes)):

            # Compare coordinates.
            cond1 = fabs(grid.Nodes[j].x - nodes[i].x) <= EPS
            cond2 = fabs(grid.Nodes[j].y - nodes[i].y) <= EPS

            if cond1 and cond2:
                nodes[i] = grid.Nodes[j]
                node_is_found = True
                break

        if not node_is_found:
            grid.Nodes.append(nodes[i])


def ranging_algorithm(grid, nodes):
    """
    Compose grid.Nodes from the nodes from zones to avoid repeating.

    If some nodes in grid are shared between several zones, the task is
    to avoid including one particular node twice to the grid.

    The nodes are compared according to their coordinates (x, y).

    The algorithm search for a node using dichotomy method with searching
    through nodes with equal x coordinates.

    :param grid: Grid object.
    :param nodes: list: nodes of zone to add to the grid.
    :return:
    """

    for i in range(0, len(nodes)):
        a = 0
        b = len(grid.Nodes) - 1
        node_is_found = False

        while a <= b:
            m = (a + b) // 2

            if fabs(grid.Nodes[m].x - nodes[i].x) < EPS:

                c = m
                while fabs(grid.Nodes[c].x - nodes[i].x) < EPS and c >= 0:
                    if fabs(grid.Nodes[c].y - nodes[i].y) < EPS:
                        nodes[i] = grid.Nodes[c]
                        node_is_found = True
                        break

                    c -= 1

                if not node_is_found:
                    c = m
                    while fabs(grid.Nodes[c].x - nodes[i].x) < EPS:

                        if fabs(grid.Nodes[c].y - nodes[i].y) < EPS:
                            nodes[i] = grid.Nodes[c]
                            node_is_found = True
                            break

                        c += 1
                        if c == len(grid.Nodes):
                            break

            if node_is_found:
                break

            if grid.Nodes[m].x > nodes[i].x:
                b = m - 1

            else:
                a = m + 1

        if not node_is_found:
            grid.Nodes.insert(a, nodes[i])
