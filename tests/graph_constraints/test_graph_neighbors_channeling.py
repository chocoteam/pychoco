import unittest

from pychoco.model import Model
from pychoco.objects.graphs.undirected_graph import create_undirected_graph, create_complete_undirected_graph


class TestGraphNeighborsChanneling(unittest.TestCase):

    def test1(self):
        m = Model()
        lb = create_undirected_graph(m, 5)
        ub = create_complete_undirected_graph(m, 5)
        sets = [m.setvar([], [0, 1, 2, 3, 4]) for i in range(0, 5)]
        g = m.graphvar(lb, ub, "g")
        m.graph_neighbors_channeling(g, sets).post()
        while m.get_solver().solve():
            val = g.get_value()
            for i in val.get_nodes():
                self.assertSetEqual(set(val.get_neighbors_of(i)), sets[i].get_value())

    def test2(self):
        m = Model()
        lb = create_undirected_graph(m, 5)
        ub = create_complete_undirected_graph(m, 5)
        bools = [m.boolvars(5) for i in range(0, 5)]
        g = m.graphvar(lb, ub, "g")
        m.graph_neighbors_channeling(g, bools).post()
        while m.get_solver().solve():
            val = g.get_value()
            for i in val.get_nodes():
                for j in val.get_neighbors_of(i):
                    self.assertTrue(bools[i][j].get_value())
