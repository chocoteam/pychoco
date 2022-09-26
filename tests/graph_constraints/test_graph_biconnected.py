import unittest

from networkx import is_biconnected

from pychoco.model import Model
from pychoco.objects.graphs.undirected_graph import create_undirected_graph, create_complete_undirected_graph


class TestGraphBiconnected(unittest.TestCase):

    def test1(self):
        m = Model()
        lb = create_undirected_graph(m, 5)
        ub = create_complete_undirected_graph(m, 5)
        g = m.graphvar(lb, ub, "g")
        m.graph_biconnected(g).post()
        while m.get_solver().solve():
            val = g.get_value().to_networkx_graph()
            self.assertTrue(is_biconnected(val))
