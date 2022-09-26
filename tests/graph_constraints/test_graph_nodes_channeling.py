import unittest

from pychoco.model import Model
from pychoco.objects.graphs.undirected_graph import create_undirected_graph, create_complete_undirected_graph


class TestGraphNodesChanneling(unittest.TestCase):

    def test1(self):
        m = Model()
        lb = create_undirected_graph(m, 5)
        ub = create_complete_undirected_graph(m, 5)
        s = m.setvar([], [0, 1, 2, 3, 4])
        g = m.graphvar(lb, ub, "g")
        m.graph_nodes_channeling(g, s).post()
        while m.get_solver().solve():
            val = g.get_value()
            self.assertSetEqual(set(val.get_nodes()), s.get_value())

    def test2(self):
        m = Model()
        lb = create_undirected_graph(m, 5)
        ub = create_complete_undirected_graph(m, 5)
        bools = m.boolvars(5)
        g = m.graphvar(lb, ub, "g")
        m.graph_nodes_channeling(g, bools).post()
        while m.get_solver().solve():
            val = g.get_value()
            for i in range(0, len(bools)):
                if i in val.get_nodes():
                    self.assertTrue(bools[i].get_value())
                else:
                    self.assertFalse(bools[i].get_value())
