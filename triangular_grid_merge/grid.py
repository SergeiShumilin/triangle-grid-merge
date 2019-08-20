"""Module describes triangular grid."""
from .node import Node
from .edge import Edge
from .face import Face
from .zone import Zone
from math import fabs


class Grid:
    __doc__ = "Class describing triangular grid"

    def __init__(self):
        """
        Grid constructor.
        """
        self.Faces = list()
        self.Edges = list()
        self.Nodes = list()
        self.Zones = list()

    def init(self, xn, yn, x, y):
        """
        The initialization of the grid is done in the next steps:

            1. Calculate the number of nodes, faces and edges basing on
            the number of points by axis.

            2. Initialize the elements' ids.

            3. Initialize Zone 1 - make all nodes and faces belong to zone 1
            of the grid.

            4. Initialize the coordinates of nodes basing on the given
            coordinates of rectangular to put the grid inside it.

                         +--------o (x2, y2)
                         |        |
                         |        |
                         |        |
                (x1, y1) o--------+

            5. Triangulate the grid.

        :param xn: number of points by x-axis.
        :param yn: number of points by y-axis.
        :param x: tuple (x1, x2) x-coordinates for the area to put the grid in.
        :param y: tuple (y1, y2) y-coordinates for the area to put the grid in.
        """
        assert xn > 1, "The number of points should be more than one."
        assert yn > 1, "The number of points should be more than one."
        assert x[0] < x[1], 'The second point should be x1 < x2'
        assert y[0] < y[1], 'The second point should be y1 < y2'

        num_nodes = self.number_of_nodes(xn, yn)
        num_edges = self.number_of_edges(xn, yn)
        num_faces = self.number_of_faces(xn, yn)

        self.init_element_arrays(num_nodes, num_edges, num_faces)

        self.init_zone()

        self.init_coordinates(xn, yn, x, y)

        self.init_ids()

        self.triangulation(xn, yn)

    def init_ids(self):
        """
        Initialize ids of the elements.
        """
        for i, node in enumerate(self.Nodes):
            node.Id = i

        for i, edge in enumerate(self.Edges):
            edge.Id = i

        for i, face in enumerate(self.Faces):
            face.Id = i

    def init_element_arrays(self, nodes, edges, faces):
        """
        Fill the arrays of structural elements and give Id to each.
        :param nodes: array of nodes.
        :param edges: array of edges.
        :param faces: array of faces.
        """
        # Initialize nodes' Ids.
        for i in range(nodes):
            self.Nodes.append(Node())

        # Initialize nodes' Ids.
        for i in range(edges):
            self.Edges.append(Edge())

        # Initialize faces' Ids.
        for i in range(faces):
            self.Faces.append(Face())

    def init_coordinates(self, xn, yn, x, y):
        """
        Initialize coordinates of the nodes inside the rectangular
        set by x = (x1, x2), y = (y1, y2).

        Coordinates are represented in memory so that elements in massives
        lie in row-wise manner.

        :param xn: number of points by x-axis.
        :param yn: number of points by y-axis.
        :param x: tuple (x1, x2): x-coord. of the rect.
        :param y: tuple (y1, y2): y-coord. of the rect.
        """
        size_x = fabs(x[0] - x[1]) / (xn - 1)
        size_y = fabs(y[0] - y[1]) / (yn - 1)

        # Init coordinates.
        for j in range(yn):
            for i in range(xn):
                self.Nodes[j * xn + i].x = x[0] + i * size_x
                self.Nodes[j * xn + i].y = y[0] + j * size_y

    def init_zone(self):
        """
        Init zone 1 of grid.

        Makes all elements of the grid belong to zone 1.
        """
        z = Zone()
        z.Nodes = self.Nodes
        z.Faces = self.Faces
        self.Zones.append(z)

    def triangulation(self, xn, yn):
        """
        Make triangulation of the grid.

                   nul    eu     nur
              OX    *-------------*
                    |fu          /|
                    |          /  |
                    |        /    |
                  el|    ec/      |er
                    |    /        |
                    |  /          |
                    |/          fd|
                    *-------------*
                   ndl   ed     ndr
        """
        sx = xn - 1
        sy = yn - 1

        ehn = sx * yn
        evn = sy * xn

        for i in range(sy):
            for j in range(0, sx):

                # Take two faces.
                fu = self.Faces[2 * (j + i * sx)]
                fd = self.Faces[2 * (j + i * sx) + 1]

                # Take three nodes for fu.
                nul = self.Nodes[i * xn + j]
                nur = self.Nodes[i * xn + j + 1]
                ndl = self.Nodes[(i + 1) * xn + j]
                ndr = self.Nodes[(i + 1) * xn + j + 1]

                # Edges.
                eu = self.Edges[i * sx + j]
                ed = self.Edges[(i + 1) * sx + j]
                el = self.Edges[ehn + i * xn + j]
                er = self.Edges[ehn + i * xn + j + 1]
                ec = self.Edges[ehn + evn + i * sx + j]

                # Link nodes and face 1.
                self.link_face_and_node(fu, nul)
                self.link_face_and_node(fu, ndl)
                self.link_face_and_node(fu, nur)

                # Link nodes and face 2.
                self.link_face_and_node(fd, ndr)
                self.link_face_and_node(fd, nur)
                self.link_face_and_node(fd, ndl)

                # Link node and edges.
                self.link_node_and_edge(nul, eu)
                self.link_node_and_edge(nur, eu)
                self.link_node_and_edge(nul, el)
                self.link_node_and_edge(ndl, el)
                self.link_node_and_edge(nur, ec)
                self.link_node_and_edge(ndl, ec)

                # For the bottom row of squares we add nodes in to the
                # bottom edge.
                if i == sy - 1:
                    self.link_node_and_edge(ndl, ed)
                    self.link_node_and_edge(ndr, ed)

                # For the right column of squares we add nodes in to the
                # right edge.
                if j == sx - 1:
                    self.link_node_and_edge(nur, er)
                    self.link_node_and_edge(ndr, er)

    @staticmethod
    def link_face_and_node(f, n):
        """
        Link node and face.
        :param n: node.
        :param f: face.
        """
        if len(f.nodes) == 3:
            raise Exception('The face is linked to the maximum number of nodes.')
        n.faces.append(f)
        f.nodes.append(n)

    @staticmethod
    def link_node_and_edge(n, e):
        """
        Link node and edge.
        :param n: node.
        :param e: edge.
        """
        if len(e.nodes) == 3:
            raise Exception('The edge is linked to the maximum number of nodes.')
        n.edges.append(e)
        e.nodes.append(n)

    @staticmethod
    def link_face_and_edge(f, e):
        """
        Link face and edge.
        :param f: face.
        :param e: edge.
        """
        if len(e.faces) == 2:
            raise Exception('The edge is linked to the maximum number of faces.')
        f.edges.append(e)
        e.faces.append(f)

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

    def is_edge_present(self, n1: Node, n2: Node):
        """
        Whether the `grid.Edges` contains the edge with nodes n1 and n2.
        :param n1: node 1.
        :param n2: node 2.
        :return: id of the edge if present and None if not.
        """
        for edge in n1.edges:
            if edge in n2.edges:
                return edge

        return None
