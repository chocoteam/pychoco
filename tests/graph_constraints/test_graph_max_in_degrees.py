import unittest

from pychoco.model import Model
from pychoco.objects.graphs.directed_graph import create_directed_graph, create_complete_directed_graph


class TestGraphMaxInDegrees(unittest.TestCase):

    def test1(self):
        m = Model()
        lb = create_directed_graph(m, 4)
        ub = create_complete_directed_graph(m, 4)
        g = m.digraphvar(lb, ub, "g")
        degrees = [0, 1, 2, 3]
        m.graph_max_in_degrees(g, degrees).post()
        while m.get_solver().solve():
            val = g.get_value()
            for i in val.get_nodes():
                self.assertTrue(len(val.get_predecessors_of(i)) <= degrees[i])
