import unittest

from pychoco.model import Model
from pychoco.objects.graphs.undirected_graph import create_undirected_graph, create_complete_undirected_graph


class TestGraphNeighborsChanneling(unittest.TestCase):

    def test1(self):
        m = Model()
        lb = create_undirected_graph(m, 5)
        ub = create_complete_undirected_graph(m, 5)
        s = m.setvar([], [0, 1, 2, 3, 4])
        g = m.graphvar(lb, ub, "g")
        m.graph_node_neighbors_channeling(g, s, 2).post()
        while m.get_solver().solve():
            val = g.get_value()
            self.assertSetEqual(set(val.get_neighbors_of(2)), s.get_value())

    def test2(self):
        m = Model()
        lb = create_undirected_graph(m, 5)
        ub = create_complete_undirected_graph(m, 5)
        bools = m.boolvars(5)
        g = m.graphvar(lb, ub, "g")
        m.graph_node_neighbors_channeling(g, bools, 3).post()
        while m.get_solver().solve():
            val = g.get_value()
            for j in val.get_neighbors_of(3):
                self.assertTrue(bools[j].get_value())
