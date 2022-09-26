import unittest

from networkx import connected_components

from pychoco.model import Model
from pychoco.objects.graphs.undirected_graph import create_undirected_graph, create_complete_undirected_graph


class TestGraphNbCliques(unittest.TestCase):

    def test1(self):
        m = Model()
        lb = create_undirected_graph(m, 5)
        ub = create_complete_undirected_graph(m, 5)
        g = m.graphvar(lb, ub, "g")
        max_cc = m.intvar(1, 10)
        m.graph_size_max_connected_components(g, max_cc).post()
        while m.get_solver().solve():
            val = g.get_value().to_networkx_graph()
            ccs = [len(cc) for cc in connected_components(val)]
            self.assertEqual(max(ccs), max_cc.get_value())
