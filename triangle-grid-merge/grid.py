"""Module describes triangular grid."""
from .node import Node
from .edge import Edge
from .face import Face


class Grid:
    __doc__ = "Class describing triangular grid"

    def __init__(self, xn, yn):
        """
        Grid constructor.
        :param xn: number of points by x-axis.
        :param yn: number of points by y-axis.
        """
        self.Faces = list()
        self.Edges = list()
        self.Nodes = list()

        num_nodes = self.number_of_edges(xn, yn)
        num_edges = self.number_of_edges(xn, yn)
        num_faces = self.number_of_faces(xn, yn)

        self.init_element_arrays(num_nodes, num_edges, num_faces)

    def init_element_arrays(self, nodes, edges, faces):
        """
        Fill the arrays of structural elements and give Id to each.
        :param nodes:
        :param edges:
        :param faces:
        """
        # Initialize nodes' Ids.
        for i in range(nodes):
            self.Nodes.append(Node(i))

        # Initialize edges' Ids.
        for i in range(edges):
            self.Edges.append(Edge(i))

        # Initialize faces' Ids.
        for i in range(faces):
            self.Faces.append(Face(i))

    @staticmethod
    def number_of_edges(xn, yn):
        """
        Count the number of edges.
        :param xn: number of points by x.
        :param yn: number of points by y.
        :return: number of edges
        """
        return (xn - 1) * yn + (yn - 1) * xn + (xn - 1) * (yn - 1)

    @staticmethod
    def number_of_nodes(xn, yn):
        """
        Count the number of nodes.
        :param xn: number of points by x.
        :param yn: number of points by y.
        :return: number of nodes
        """
        return xn * yn

    @staticmethod
    def number_of_faces(xn, yn):
        """
        Count the number of faces.
        :param xn: number of points by x.
        :param yn: number of points by y.
        :return: number of faces
        """
        return 2 * (xn - 1) * (yn - 1)

    def init_coordinates():
        pass
