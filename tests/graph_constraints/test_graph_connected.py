import unittest

from networkx import is_connected

from pychoco.model import Model
from pychoco.objects.graphs.undirected_graph import create_undirected_graph, create_complete_undirected_graph


class TestGraphConnected(unittest.TestCase):

    def test1(self):
        m = Model()
        lb = create_undirected_graph(m, 5)
        ub = create_complete_undirected_graph(m, 5)
        g = m.graphvar(lb, ub, "g")
        m.graph_connected(g).post()
        while m.get_solver().solve():
            val = g.get_value().to_networkx_graph()
            # The connected constraint of Choco allows empty graphs,
            # whereas networkx does not.
            if val.number_of_nodes() > 0:
                self.assertTrue(is_connected(val))
