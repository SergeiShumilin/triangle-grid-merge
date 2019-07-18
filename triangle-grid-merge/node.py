"""Module describing grid's node"""


class Node:
    __doc__ = "class describing node"

    def __init__(self):
        """
        Construct node.
        :param id: node's id in the grid.
        """
        self.Id = None
        self.x = None
        self.y = None

        self.faces = list()
        self.edges = list()
