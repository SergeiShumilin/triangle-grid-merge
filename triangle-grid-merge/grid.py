"""Module describes triangular grid."""
from .node import Node
from .edge import Edge
from .face import Face


class Grid:
    __doc__ = "Class describing triangular grid"

    def __init__(self, nodes, edges, faces):
        """
        Grid constructor.
        :param nodes: number of nodes.
        :param edges: number of edges.
        :param faces: number of faces.
        """
        # Initialize nodes' ids.
        self.Nodes = list()
        for i in range(nodes):
            self.Nodes.append(Node(i))

        # Initialize edges' ids.
        self.Edges = list()
        for i in range(edges):
            self.Edges.append(Edge(i))

        # Initialize faces' ids.
        self.Faces = list()
        for i in range(faces):
            self.Faces.append(Face(i))
