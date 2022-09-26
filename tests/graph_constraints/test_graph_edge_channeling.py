import unittest

from pychoco.model import Model
from pychoco.objects.graphs.directed_graph import create_directed_graph, create_complete_directed_graph
from pychoco.objects.graphs.undirected_graph import create_undirected_graph, create_complete_undirected_graph


class TestGraphEdgeChanneling(unittest.TestCase):

    def test1(self):
        m = Model()
        lb = create_undirected_graph(m, 5)
        ub = create_complete_undirected_graph(m, 5)
        g = m.graphvar(lb, ub, "g")
        b = m.boolvar()
        m.graph_edge_channeling(g, b, 0, 2).post()
        while m.get_solver().solve():
            self.assertEqual(b.get_value(), g.get_value().contains_edge(0, 2))

    def test2(self):
        m = Model()
        lb = create_directed_graph(m, 4)
        ub = create_complete_directed_graph(m, 4)
        g = m.digraphvar(lb, ub, "g")
        b = m.boolvar()
        m.graph_edge_channeling(g, b, 0, 2).post()
        while m.get_solver().solve():
            self.assertEqual(b.get_value(), g.get_value().contains_edge(0, 2))
