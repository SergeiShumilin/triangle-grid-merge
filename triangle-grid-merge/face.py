"""Module describing grid's face."""


class Face:
    __doc__ = "Module describing grid's face."

    def __init__(self):
        """
        Construct a face.
        :param id: face's id.
        """
        self.Id = None

        # Nodes and edges set clockwise.
        self.nodes = list()
        self.edges = list()
