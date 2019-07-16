"""
Module provides interaction with tecplot format.
"""


def print_tecplot(grid):
    """
    Create tecplot file with grid.
    :param grid: Grid object.
    """
    with open('grids/grid.dat', 'w+') as f:
        f.write('TITLE = "GRID"\n')
        f.write('VARIABLES = "X", "Y"\n')
        f.write('ZONE T = "GRID 1"\n')
        f.write('NODES = ' + str(len(grid.Nodes)) + '\n')
        f.write('ELEMENTS = ' + str(len(grid.Faces)) + '\n')
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
