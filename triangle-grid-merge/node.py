"""Module describing grid's node"""


class Node:

    __doc__ = "class discribing node"

    def __init__(self, id):
        """
        Construct node.
        :param id: node's id in the grid.
        """
        self.Id = id
        self.x = None
        self.y = None

        self.faces = list()
        self.edges = list()
