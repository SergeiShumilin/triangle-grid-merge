"""The module provides functionality to merge a zone into grid
comparing nodes coordinates."""

from math import fabs

# Accuracy to compare nodes' coordinates.
EPS = 10e-5


def n_square(grid, nodes):
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


def dichotomy_1_sided(grid, nodes):
    """
    Compose grid.Nodes from the nodes from zones to avoid repeating.

    If some nodes in grid are shared between several zones, the task is
    to avoid including one particular node twice to the grid.

    The nodes are compared according to their coordinates (x, y).

    Given a node the algorithm uses dichotomy to locate a node with equal x-coordinate and which stays first
    of all nodes with equal x-coordinate when the algorithm continues to compare y-coordinate of neighbor elements
    with equal x-coordinates in one directions (to the right).

    This algorithm is more effective than `dichotomy_2_sided` when the number of nodes with equal x-coordinates
    is big.

    :param grid: Grid object.
    :param nodes: list: nodes of zone to add to the grid.
    """

    for i in range(0, len(nodes)):
        a = 0
        b = len(grid.Nodes) - 1
        node_is_found = False

        while a <= b:
            m = (a + b) // 2

            if fabs(grid.Nodes[m].x - nodes[i].x) < EPS and (m == 0 or fabs(grid.Nodes[m - 1].x - nodes[i].x) > EPS):

                c = m
                while fabs(grid.Nodes[c].x - nodes[i].x) < EPS:

                    if fabs(grid.Nodes[c].y - nodes[i].y) < EPS:
                        nodes[i] = grid.Nodes[c]
                        node_is_found = True
                        break

                    c += 1
                    if c == len(grid.Nodes):
                        break

            if not node_is_found:

                if grid.Nodes[m].x > nodes[i].x or fabs(grid.Nodes[m].x - nodes[i].x) < EPS:
                    b = m - 1

                else:
                    a = m + 1
            else:
                break

        if not node_is_found:
            grid.Nodes.insert(a, nodes[i])


def dichotomy_2_sided(grid, nodes):
    """
    Compose grid.Nodes from the nodes from zones to avoid repeating.

    If some nodes in grid are shared between several zones, the task is
    to avoid including one particular node twice to the grid.

    The nodes are compared according to their coordinates (x, y).

    Given a node the algorithm uses dichotomy to locate a node with equal x-coordinate and
    continues to compare y-coordinate of neighbor elements with equal x-coordinates in two directions.

    This algorithm is more effective than `dichotomy_1_sided` when the number of nodes with equal x-coordinates is low.

    :param grid: Grid object.
    :param nodes: list: nodes of zone to add to the grid.
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
