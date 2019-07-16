"""Module describes triangular grid."""
from .node import Node
from .edge import Edge
from .face import Face
from math import fabs


class Grid:
    __doc__ = "Class describing triangular grid"

    def __init__(self, xn, yn, x, y):
        """
        Grid constructor.
        :param xn: number of points by x-axis.
        :param yn: number of points by y-axis.
        """
        assert xn > 1, "The number of points should be more than one."
        assert yn > 1, "The number of points should be more than one."
        assert x[0] < x[1], 'The second point should be x1 < x2'
        assert y[0] < y[1], 'The second point should be y1 < y2'

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
        :param nodes: array of nodes.
        :param edges: array of edges.
        :param faces: array of faces.
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

    def init_coordinates(self, xn, yn, x, y):
        """
        Initialize coordinates of the nodes inside the rectangular
        set by x = (x1, x2), y = (y1, y2).

        Coordinates are represented in memory so that elements in massives
        lie in row-wise manner.

        :param xn:
        :param yn:
        :param x: tuple (x1, x2): x-coord. of the rect.
        :param y: tuple (y1, y2): y-coord. of the rect.
        """
        size_x = fabs(x[0] - x[1]) / (xn - 1)
        size_y = fabs(y[0] - y[1]) / (yn - 1)

        # Init coordinates.
        for j in range(yn):
            for i in range(xn):
                self.Nodes[j * xn + i].x = i * size_x
                self.Nodes[j * xn + i].y = j * size_y
