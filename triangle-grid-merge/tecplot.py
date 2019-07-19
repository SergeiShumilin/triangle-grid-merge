"""
Module provides interaction with tecplot format.
"""
from node import Node
from face import Face
from edge import Edge
from grid import Grid
from zone import Zone
from math import fabs

# Accuracy to compare nodes' coordinates.
EPS = 10e-7


def print_tecplot(grid, filename):
    """
    Create tecplot file (.dat) with grid.

    :param filename: file to write in.
    :param grid: Grid object.
    """
    print_tecplot_header(filename)

    print_tecplot_zone(grid, filename, 'ZON1 1')


def print_tecplot_zone(grid, filename, zone_name):
    """
    Add grid as a zone to "grid/grid.dat".

    :param grid: Grid or Zone object.
    :param filename: file to write in.
    :param zone_name: name for the zone.
    """
    print_zone_header(filename, zone_name, grid.Nodes, grid.Faces)

    print_variables(filename, grid.Nodes)

    print_connectivity_list(filename, grid.Faces)


def read_tecplot(filename):
    """
    Read tecplot file (.dat) and create a grid.

    If tecplot file contains several zones than merge them into
    single grid.

    :param filename: file to read from.
    :param grid: Grid object to import in.
    :return: Grid object.
    """
    grid = Grid()

    file_with_grid = open('grids/{}'.format(filename), 'r')

    lines = file_with_grid.readlines()

    # Number of times the word ZONE occurs in the file.
    nzones = number_of_zones(lines)

    # Number of nodes.
    nnodes = number_of_nodes(lines[3])

    # Number of faces.
    nfaces = number_of_faces(lines[4])

    # Number of edges.
    nedges = 2 * nfaces + 1

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

    # cl_line - connectivity list line.
    connections(grid, lines[9: 9 + nfaces], grid.Nodes, grid.Faces)

    file_with_grid.close()

    # Init new elements' ids.
    grid.init_ids()

    return grid


def read_multizone_tecplot(filename):
    """
    Read tecplot file with two zones and create a grid.

    Merging of two zones is accomplished in the next steps:

    1. Read x, y coordinates of the nodes.

    2. Create node lists for each zone.

    3. Compose grid's node list avoiding repeating nodes.

    4. Link faces, nodes and create edges for each zone.

        Since links in the second zone node list when performing step 2
        share links to nodes with links from node list of zone 1, faces
        link to the correct objects because they point to the ids of the
        nodes.

    5. Both faces lists become grid's Faces.

    :param filename: file to read from.
    :return: Grid object.
    """
    grid = Grid()

    file_with_grid = open('grids/{}'.format(filename), 'r')

    lines = file_with_grid.readlines()

    # Number of times the word ZONE occurs in the file.
    nzones = number_of_zones(lines)

    # Number of faces of zone 1.
    nfaces_z1 = number_of_faces(lines[4])

    # Number of faces in zone 2  expressed by number of elements in zone 1.
    nfaces_z2 = number_of_faces(lines[11 + nfaces_z1])

    # Read all nodes of zone 1.
    # x coords.
    xs_z1 = map(float, lines[7].split(' ')[:-1])
    # y coords.
    ys_z1 = map(float, lines[8].split(' ')[:-1])

    # Nodes of zone 1.
    nodes_z1 = list()

    # Initialize node array for zone 1.
    for x, y in zip(xs_z1, ys_z1):
        n = Node()
        n.x = x
        n.y = y
        nodes_z1.append(n)

    del xs_z1
    del ys_z1

    # Read all nodes of zone 2.
    # x coords.
    xs_z2 = map(float, lines[14 + nfaces_z1].split(' ')[:-1])
    # y coords.
    ys_z2 = map(float, lines[15 + nfaces_z1].split(' ')[:-1])

    nodes_z2 = list()

    # Initialize node array for zone 1.
    for x, y in zip(xs_z2, ys_z2):
        n = Node()
        n.x = x
        n.y = y
        nodes_z2.append(n)

    del xs_z2
    del ys_z2

    compose_node_list_algorithm_1(grid, nodes_z1, nodes_z2)

    # Now create two faces arrays.
    faces_z1 = list()
    connections(grid, lines[9: 9 + nfaces_z1], nodes_z1, faces_z1)

    faces_z2 = list()
    connections(grid, lines[16 + nfaces_z1: 16 + nfaces_z1 + nfaces_z2], nodes_z2, faces_z2)

    grid.Faces = faces_z1 + faces_z2

    file_with_grid.close()

    # Init new elements' ids.
    grid.init_ids()

    return grid


def compose_node_list_algorithm_1(grid, nodes_z1, nodes_z2):
    """
    Compose grid.Nodes from the nodes from two zones to avoid repeating.

    The nodes are compared according to their coordinates (x, y).
    The algorithm does simple n^2 search through all nodes.

    :param grid: Grid object.
    :param nodes_z1: list: nodes of zone 1.
    :param nodes_z2: list: nodes of zone 2.
    """
    # Copy all nodes from zone 1 to the grid.
    grid.Nodes = [node for node in nodes_z1]

    for i in range(len(nodes_z2)):

        node_is_found = False

        for j in range(len(nodes_z1)):

            # Compare coordinates.
            cond1 = fabs(nodes_z1[j].x - nodes_z2[i].x) <= EPS
            cond2 = fabs(nodes_z1[j].y - nodes_z2[i].y) <= EPS

            if cond1 and cond2:
                nodes_z2[i] = nodes_z1[j]
                node_is_found = True
                break

        if not node_is_found:
            grid.Nodes.append(nodes_z2[i])


def connections(grid, lines, nodes, faces):
    """
    Read the connectivity list and link faces and node
    according to the list.

    1 2 3  -> Face 1
    2 3 4  -> Face 2

    Also, edges are created and linked basing on their presence in grid.Edge.

    :param grid: Grid object.
    :param lines: list : lines of file with connectivity list.
    :param nodes: list : nodes to connect.
    :param faces: list : to connect (must be empty).
    """
    # cl_line - connectivity list line.
    for face_id, cl_line in enumerate(lines):
        f = Face()

        # Extract nodes' ids.
        ids = cl_line.split(' ')
        ids = list(map(int, ids[:-1]))

        n1 = nodes[ids[0] - 1]
        n2 = nodes[ids[1] - 1]
        n3 = nodes[ids[2] - 1]

        # Link face and nodes.
        Grid.link_face_and_node(f, n1)
        Grid.link_face_and_node(f, n2)
        Grid.link_face_and_node(f, n3)

        # Link faces, nodes and edges.
        e = grid.is_edge_present(n1, n2)
        if e is None:
            e = Edge()
            grid.link_face_and_edge(f, e)
            grid.link_node_and_edge(n1, e)
            grid.link_node_and_edge(n2, e)
            grid.Edges.append(e)
        else:
            grid.link_face_and_edge(f, e)

        e = grid.is_edge_present(n2, n3)
        if e is None:
            e = Edge()
            grid.link_face_and_edge(f, e)
            grid.link_node_and_edge(n2, e)
            grid.link_node_and_edge(n3, e)
            grid.Edges.append(e)
        else:
            grid.link_face_and_edge(f, e)

        e = grid.is_edge_present(n3, n1)
        if e is None:
            e = Edge()
            grid.link_face_and_edge(f, e)
            grid.link_node_and_edge(n3, e)
            grid.link_node_and_edge(n1, e)
            grid.Edges.append(e)
        else:
            grid.link_face_and_edge(f, e)

        faces.append(f)


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


def number_of_faces(line):
    """
    Extract the number of nodes from te line.

    :param line: line with the word NODES
    :return: int number of nodes.
    """
    return int(line[line.find('ELEMENTS =') + 10: len(line)])


def print_tecplot_header(filename):
    """
    Write tecplot header containing the information
    about Title and number of variables.

    :param filename: file to write in.
    """
    with open('grids/{}'.format(filename), 'w') as f:
        f.write('TITLE = "GRID"\n')
        f.write('VARIABLES = "X", "Y"\n')


def print_zone_header(filename, zone_name, nodes, faces):
    """
    Write information about zone into the file.

    :param filename: file to write in.
    :param zone_name: name of the zone.
    :param nodes: nodes.
    :param faces: faces.
    """
    with open('grids/{}'.format(filename), 'a+') as f:
        f.write('ZONE T = "{}"\n'.format(zone_name))
        f.write('NODES = {}\n'.format((len(nodes))))
        f.write('ELEMENTS = {}\n'.format((len(faces))))
        f.write('DATAPACKING = BLOCK\n')
        f.write('ZONETYPE = FETRIANGLE\n')


def print_variables(filename, nodes):
    """
    Write variables values in tecplot file.

    :param filename: file to write in.
    :param nodes: nodes containing values.
    """
    with open('grids/{}'.format(filename), 'a+') as f:
        # Variables' values.
        for node in nodes:
            f.write(str(node.x) + ' ')

        f.write('\n')

        for node in nodes:
            f.write(str(node.y) + ' ')
        f.write('\n')


def print_connectivity_list(filename, faces):
    """
    Write tecplot connectivity list.

    :param filename: file to write in.
    :param faces: faces with nodes.
    """
    with open('grids/{}'.format(filename), 'a+') as f:
        # Connectivity list.
        for face in faces:
            for node in face.nodes:
                f.write(str(node.Id + 1) + ' ')
            f.write('\n')
