import unittest

from networkx import is_tree

from pychoco.model import Model
from pychoco.objects.graphs.directed_graph import create_directed_graph, create_complete_directed_graph


class TestGraphDirectedTree(unittest.TestCase):

    def test1(self):
        m = Model()
        lb = create_directed_graph(m, 5)
        ub = create_complete_directed_graph(m, 5)
        g = m.digraphvar(lb, ub, "g")
        m.graph_directed_tree(g, 0).post()
        while m.get_solver().solve():
            val = g.get_value().to_networkx_graph()
            if val.number_of_nodes() > 0:
                self.assertTrue(is_tree(val))
