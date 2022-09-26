import unittest

from pychoco.model import Model
from pychoco.objects.graphs.directed_graph import create_directed_graph, create_complete_directed_graph


class TestGraphNodeSuccessorsChanneling(unittest.TestCase):

    def test1(self):
        m = Model()
        lb = create_directed_graph(m, 4)
        ub = create_complete_directed_graph(m, 4)
        s = m.setvar([], [0, 1, 2, 3])
        g = m.digraphvar(lb, ub, "g")
        m.graph_node_successors_channeling(g, s, 2).post()
        while m.get_solver().solve():
            val = g.get_value()
            self.assertSetEqual(set(val.get_successors_of(2)), s.get_value())

    def test2(self):
        m = Model()
        lb = create_directed_graph(m, 4)
        ub = create_complete_directed_graph(m, 4)
        bools = m.boolvars(4)
        g = m.digraphvar(lb, ub, "g")
        m.graph_node_successors_channeling(g, bools, 3).post()
        while m.get_solver().solve():
            val = g.get_value()
            for j in val.get_successors_of(3):
                self.assertTrue(bools[j].get_value())
