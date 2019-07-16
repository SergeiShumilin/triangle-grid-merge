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

    add_tecplot_zone(grid, 'ZON1 1')


def add_tecplot_zone(grid, zone_name):
    """
    Add grid as a zone to "grid/grid.dat".
    :param zone_name: name for the zone.
    :param grid: Grid object.
    """
    with open('grids/grid.dat', 'a+') as f:
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
