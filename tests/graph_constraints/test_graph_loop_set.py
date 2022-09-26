import unittest

from pychoco.model import Model
from pychoco.objects.graphs.undirected_graph import create_undirected_graph, create_complete_undirected_graph


class TestGraphDirectedForest(unittest.TestCase):

    def test1(self):
        m = Model()
        lb = create_undirected_graph(m, 5)
        ub = create_complete_undirected_graph(m, 5)
        g = m.graphvar(lb, ub, "g")
        s = m.setvar([], [0, 1, 2, 3, 4])
        m.graph_loop_set(g, s).post()
        while m.get_solver().solve():
            val = g.get_value()
            for i in val.get_nodes():
                if val.contains_edge(i, i):
                    self.assertTrue(i in s.get_value())
                else:
                    self.assertFalse(i in s.get_value())
