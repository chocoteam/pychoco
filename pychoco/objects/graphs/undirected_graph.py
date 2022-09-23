from typing import List

from pychoco import backend
from pychoco._utils import get_int_array
from pychoco.objects.graphs.graph import Graph


class UndirectedGraph(Graph):
    """
    Class representing undirected graphs.
    """

    def __init__(self, model: "Model", nb_max_nodes: int, node_set_type: str = "BITSET",
                 edge_set_type: str = "BIPARTITE_SET", all_node: bool = False):
        """
        Constructor for an undirected graph. Nodes are represented by integers ranging from 0 to nb_max_nodes - 1.
        The data structure used for representing nodes and edges can be chosen among:
        ["BITSET", "BIPARTITE_SET", "SMALL_BIPARTITE_SET", "RANGE_SET", "LINKED_LIST"].

        :param model: A Choco model.
        :param nb_max_nodes: The maximum number of nodes allowed in the graph.
        :param node_set_type: The set data structure to use for nodes (default: "BITSET", must be among
            ["BITSET", "BIPARTITE_SET", "SMALL_BIPARTITE_SET", "RANGE_SET", "LINKED_LIST"]).
        :param edge_set_type: The set data structure to use for edges (default: "BIPARTITE_SET", must be among
            ["BITSET", "BIPARTITE_SET", "SMALL_BIPARTITE_SET", "RANGE_SET", "LINKED_LIST"]).
        :param all_node: If True, all nodes are present in the graph and cannot be removed.
        """
        assert node_set_type in ["BITSET", "BIPARTITE_SET", "SMALL_BIPARTITE_SET", "RANGE_SET", "LINKED_LIST"]
        self._model = model
        handle = backend.create_graph(model.handle, nb_max_nodes, node_set_type, edge_set_type, all_node)
        super().__init__(handle)

    def is_directed(self):
        return False

    def get_neighbors_of(self, node: int):
        """
        :param node: A node of the graph.
        :return: The neighbors of the node.
        """
        handle = backend.get_successors_of(self.handle, node)
        return get_int_array(handle)

    def __repr__(self):
        return "Undirected Graph"


def create_undirected_graph(model: "Model", nb_max_nodes: int, nodes: List[int], edges: List[List[int]],
                            node_set_type: str = "BITSET", edge_set_type: str = "BIPARTITE_SET"):
    """
    Creates an undirected graph from a list of nodes and edges.

    :param model: A Choco model.
    :param nb_max_nodes: The maximum number of nodes allowed in the graph.
    :param nodes: A list of nodes, e.g [0, 1, 2, 3].
    :param edges: A list of edges, e.g. [ [0, 1], [1, 3], [3, 2] ].
    :param node_set_type: The set data structure to use for nodes (default: "BITSET", must be among
        ["BITSET", "BIPARTITE_SET", "SMALL_BIPARTITE_SET", "RANGE_SET", "LINKED_LIST"]).
    :param edge_set_type: The set data structure to use for edges (default: "BIPARTITE_SET", must be among
        ["BITSET", "BIPARTITE_SET", "SMALL_BIPARTITE_SET", "RANGE_SET", "LINKED_LIST"]).
    :return: An UndirectedGraph.
    """
    g = UndirectedGraph(model, nb_max_nodes, node_set_type, edge_set_type)
    for i in nodes:
        g.add_node(i)
    for e in edges:
        assert len(e) == 2, "[graph] Edges must be in the form [source, destination]"
        g.add_edge(e[0], e[1])
    return g
