import unittest

from pychoco.model import Model
from pychoco.objects.graphs.directed_graph import create_directed_graph, create_complete_directed_graph


class TestGraphSuccessorsChanneling(unittest.TestCase):

    def test1(self):
        m = Model()
        lb = create_directed_graph(m, 4)
        ub = create_complete_directed_graph(m, 4)
        sets = [m.setvar([], [0, 1, 2, 3, 4]) for i in range(0, 4)]
        g = m.digraphvar(lb, ub, "g")
        m.graph_successors_channeling(g, sets).post()
        while m.get_solver().solve():
            val = g.get_value()
            for i in val.get_nodes():
                self.assertSetEqual(set(val.get_successors_of(i)), sets[i].get_value())

    def test2(self):
        m = Model()
        lb = create_directed_graph(m, 4)
        ub = create_complete_directed_graph(m, 4)
        bools = [m.boolvars(4) for i in range(0, 4)]
        g = m.digraphvar(lb, ub, "g")
        m.graph_successors_channeling(g, bools).post()
        while m.get_solver().solve():
            val = g.get_value()
            for i in val.get_nodes():
                for j in val.get_successors_of(i):
                    self.assertTrue(bools[i][j].get_value())
