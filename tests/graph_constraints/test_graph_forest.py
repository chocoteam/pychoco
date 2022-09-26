import unittest

from networkx import is_forest

from pychoco.model import Model
from pychoco.objects.graphs.undirected_graph import create_undirected_graph, create_complete_undirected_graph


class TestGraphDirectedForest(unittest.TestCase):

    def test1(self):
        m = Model()
        lb = create_undirected_graph(m, 4)
        ub = create_complete_undirected_graph(m, 4)
        g = m.graphvar(lb, ub, "g")
        m.graph_forest(g).post()
        while m.get_solver().solve():
            val = g.get_value().to_networkx_graph()
            if val.number_of_nodes() > 0:
                self.assertTrue(is_forest(val))
