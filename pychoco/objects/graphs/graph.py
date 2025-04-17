from abc import ABC, abstractmethod

from pychoco import backend
from pychoco._handle_wrapper import _HandleWrapper
from pychoco._utils import get_int_array


class Graph(ABC, _HandleWrapper):
    """
    Abstract class representing a graph.
    """

    @abstractmethod
    def is_directed(self):
        """
        :return: True if this graph is directed, False if it is undirected.
        """
        pass

    def get_nodes(self):
        """
        :return: The nodes of the graph.
        """
        nodes_handle = backend.get_nodes(self._handle)
        nodes = get_int_array(nodes_handle)
        return nodes

    def add_node(self, node: int):
        """
        Add a node to the graph.

        :param node: The node to add (int).
        :return: True if the node was successfully added. False if it was already in the graph.
        """
        assert node >= 0, "[graph] Nodes cannot be negative."
        assert node < self.get_nb_max_nodes(), "[graph] Nodes cannot be greater of equal to get_nb_max_nodes()"
        return bool(backend.add_node(self._handle, node))

    def remove_node(self, node: int):
        """
        Remove a node from the graph.

        :param node: The node to remove (int).
        :return: True if the node was successfully removed. False if it was not in the graph.
        """
        assert node >= 0, "[graph] Nodes cannot be negative."
        assert node < self.get_nb_max_nodes(), "[graph] Nodes cannot be greater of equal to get_nb_max_nodes()"
        return bool(backend.remove_node(self._handle, node))

    def add_edge(self, source: int, destination: int):
        """
        Add an edge to the graph.

        :param source: The source of the edge (int).
        :param destination: The destination of the edge (int).
        :return: True if the edge was successfully added. False if it was already present.
        """
        assert source >= 0 and destination >= 0, "[graph] Nodes cannot be negative."
        assert source < self.get_nb_max_nodes() and destination < self.get_nb_max_nodes(), \
            "[graph] Nodes cannot be greater of equal to get_nb_max_nodes()"
        return bool(backend.add_edge(self._handle, source, destination))

    def remove_edge(self, source: int, destination: int):
        """
        Remove an edge from the graph.

        :param source: The source of the edge (int).
        :param destination: The destination of the edge (int).
        :return: True if the edge was successfully removed. False if it was not in the graph.
        """
        assert source >= 0 and destination >= 0, "[graph] Nodes cannot be negative."
        assert source < self.get_nb_max_nodes() and destination < self.get_nb_max_nodes(), \
            "[graph] Nodes cannot be greater of equal to get_nb_max_nodes()"
        return bool(backend.remove_edge(self._handle, source, destination))

    def get_nb_max_nodes(self):
        """
        :return: The maximum number of nodes allowed in the graph.
        """
        return backend.get_nb_max_nodes(self._handle)

    def get_node_set_type(self):
        """
        :return: The type of set used to represent nodes.
        """
        return backend.get_node_set_type(self._handle)

    def get_edge_set_type(self):
        """
        :return: The type of set used to represent edges.
        """
        return backend.get_edge_set_type(self._handle)

    def contains_node(self, node: int):
        """
        Check if a node is in the graph.

        :param node: The node (int).
        :return: True if the graph contains the node, False otherwise.
        """
        assert node >= 0, "[graph] Nodes cannot be negative."
        assert node < self.get_nb_max_nodes(), "[graph] Nodes cannot be greater of equal to get_nb_max_nodes()"
        return bool(backend.contains_node(self._handle, node))

    def contains_edge(self, source: int, destination: int):
        """
        Check if an edge is in the graph.

        :param source: The source node of the edge (int).
        :param destination: The destination node of the edge (int).
        :return: True if the graph contains the edge, False otherwise.
        """
        assert source >= 0 and destination >= 0, "[graph] Nodes cannot be negative."
        assert source < self.get_nb_max_nodes() and destination < self.get_nb_max_nodes(), \
            "[graph] Nodes cannot be greater of equal to get_nb_max_nodes()"
        return bool(backend.contains_edge(self._handle, source, destination))

    def graphviz_export(self):
        """
        :return: A graphviz representation of the graph.
        """
        return backend.graphviz_export(self._handle)
