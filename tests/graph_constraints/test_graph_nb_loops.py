import unittest

from pychoco.model import Model
from pychoco.objects.graphs.undirected_graph import create_undirected_graph, create_complete_undirected_graph


class TestGraphNbCliques(unittest.TestCase):

    def test1(self):
        m = Model()
        lb = create_undirected_graph(m, 5)
        ub = create_complete_undirected_graph(m, 5)
        g = m.graphvar(lb, ub, "g")
        nb_loops = m.intvar(0, 10)
        m.graph_nb_loops(g, nb_loops).post()
        while m.get_solver().solve():
            val = g.get_value()
            nb = 0
            for i in val.get_nodes():
                if val.contains_edge(i, i):
                    nb += 1
            self.assertEqual(nb, nb_loops.get_value())
