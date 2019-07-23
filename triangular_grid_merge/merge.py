"""Module that provides tools for merging triangular grids"""


def most_simple(grid1, grid2):
    """
    Merge two grids by the most straightforward algorithm:
    for each node in grid1 find a node in grid2 that has the same
    coordinates.

    Computational complexity: n^2

    :param grid1: first Grid object.
    :param grid2: second Grid object.
    :return: merged grid.
    """
    for node1 in grid1.Nodes:
        for node2 in grid2.Nodes:

            if node1.x == node2.x and node1.y == node2.y:
                node1 = node2
                break