import unittest

from pychoco.model import Model
from pychoco.objects.graphs.undirected_graph import create_undirected_graph, create_complete_undirected_graph


class TestGraphNodesChanneling(unittest.TestCase):

    def test1(self):
        m = Model()
        lb = create_undirected_graph(m, 5)
        ub = create_complete_undirected_graph(m, 5)
        g = m.graphvar(lb, ub, "g")
        b = m.boolvar()
        m.graph_node_channeling(g, b, 2).post()
        while m.get_solver().solve():
            self.assertEqual(b.get_value(), g.get_value().contains_node(2))
