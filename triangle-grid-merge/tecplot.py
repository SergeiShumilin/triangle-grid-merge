"""
Module provides interaction with tecplot format.
"""
from node import Node
from face import Face
from edge import Edge
from grid import Grid


def print_tecplot(grid, filename):
    """
    Create tecplot file with grid.
    :param grid: Grid object.
    """
    with open('grids/{}'.format(filename), 'w') as f:
        f.write('TITLE = "GRID"\n')
        f.write('VARIABLES = "X", "Y"\n')

    print_tecplot_zone(grid, filename, 'ZON1 1')


def print_tecplot_zone(grid, filename, zone_name):
    """
    Add grid as a zone to "grid/grid.dat".
    :param zone_name: name for the zone.
    :param grid: Grid object.
    """
    with open('grids/{}'.format(filename), 'a+') as f:
        f.write('ZONE T = "{}"\n'.format(zone_name))
        f.write('NODES = {}\n'.format((len(grid.Nodes))))
        f.write('ELEMENTS = {}\n'.format((len(grid.Faces))))
        f.write('DATAPACKING = BLOCK\n')
        f.write('ZONETYPE = FETRIANGLE\n')

        # Variables' values.
        for node in grid.Nodes:
            f.write(str(node.x) + ' ')

        f.write('\n')

        for node in grid.Nodes:
            f.write(str(node.y) + ' ')
        f.write('\n')

        # Connectivity list.
        for face in grid.Faces:
            for node in face.nodes:
                f.write(str(node.Id + 1) + ' ')
            f.write('\n')


def read_tecplot(file):
    """
    Read tecplot file and create a grid.

    If tecplot file contains several zones than merge them into
    single grid.

    :param grid: Grid object to import in.
    :param file: tecplot (.dat) file.
    :return: Grid object.
    """
    grid = Grid()

    file_with_grid = open('grids/{}'.format(file), 'r')

    lines = file_with_grid.readlines()

    # Number of times the word ZONE occurs in the file.
    nzones = number_of_zones(lines)

    # Number of nodes.
    nnodes = number_of_nodes(lines[3])

    # number of faces.
    nelements = number_of_elements(lines[4])

    # number of edges.
    nedges = 2 * nelements + 1

    # Create arrays of elements in the grid.
    for i in range(nnodes):
        grid.Nodes.append(Node())

    for i in range(nedges):
        grid.Edges.append(Edge())

    # If ELEMENTS is found then we can count two lines down the file
    # and start read the variables values.
    # X-coord.
    for node_id, x in enumerate(map(float, lines[7].split(' ')[:-1])):
        grid.Nodes[node_id].x = x

    # Y-coord.
    for node_id, y in enumerate(map(float, lines[8].split(' ')[:-1])):
        grid.Nodes[node_id].y = y

    # Current edge in grid.Edges.
    edge = 0

    # cl_line - connectivity list line.
    for face_id, cl_line in enumerate(lines[9: 10 + nelements]):
        # Set id.
        f = Face()

        # Extract nodes' ids.
        ids = cl_line.split(' ')
        ids = list(map(int, ids[:-1]))

        n1 = grid.Nodes[ids[0] - 1]
        n2 = grid.Nodes[ids[1] - 1]
        n3 = grid.Nodes[ids[2] - 1]

        # Link face and nodes.
        grid.link_face_and_node(f, n1)
        grid.link_face_and_node(f, n2)
        grid.link_face_and_node(f, n3)

        # Link faces, nodes and edges.
        if grid.is_edge_present(n1, n2) is None:
            grid.link_face_and_edge(f, grid.Edges[edge])
            grid.link_node_and_edge(n1, grid.Edges[edge])
            grid.link_node_and_edge(n2, grid.Edges[edge])
            edge += 1
        else:
            grid.link_face_and_edge(f, grid.Edges[edge])

        if grid.is_edge_present(n2, n3) is None:
            grid.link_face_and_edge(f, grid.Edges[edge])
            grid.link_node_and_edge(n2, grid.Edges[edge])
            grid.link_node_and_edge(n3, grid.Edges[edge])
            edge += 1
        else:
            grid.link_face_and_edge(f, grid.Edges[edge])

        if grid.is_edge_present(n3, n1) is None:
            grid.link_face_and_edge(f, grid.Edges[edge])
            grid.link_node_and_edge(n3, grid.Edges[edge])
            grid.link_node_and_edge(n1, grid.Edges[edge])
            edge += 1
        else:
            grid.link_face_and_edge(f, grid.Edges[edge])

        grid.Faces.append(f)

    file_with_grid.close()

    # Init new elements' ids.
    grid.init_ids()

    return grid


def number_of_zones(file):
    """
    Count the number of times the word ZONE occurs in the file.
    :param file: file to read.
    :return: number of zones.
    """
    return ' '.join(file).count('ZONE')


def number_of_nodes(line):
    """
    Extract the number of nodes from te line.

    :param line: line with the word NODES
    :return: int number of nodes.
    """
    return int(line[line.find('NODES =') + 7: len(line)])


def number_of_elements(line):
    """
    Extract the number of nodes from te line.

    :param line: line with the word NODES
    :return: int number of nodes.
    """
    return int(line[line.find('ELEMENTS =') + 10: len(line)])
