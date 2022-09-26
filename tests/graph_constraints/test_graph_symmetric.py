import unittest

from pychoco.model import Model
from pychoco.objects.graphs.directed_graph import create_directed_graph, create_complete_directed_graph


class TestGraphSymmetric(unittest.TestCase):

    def test1(self):
        m = Model()
        lb = create_directed_graph(m, 4, [], [])
        ub = create_complete_directed_graph(m, 4)
        g = m.digraphvar(lb, ub, "g")
        m.graph_symmetric(g).post()
        while m.get_solver().solve():
            val = g.get_value()
            for i in val.get_nodes():
                for j in val.get_successors_of(i):
                    self.assertTrue(val.contains_edge(j, i))
