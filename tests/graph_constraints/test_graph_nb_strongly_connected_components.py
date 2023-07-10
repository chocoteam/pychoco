import unittest

from networkx import number_strongly_connected_components

from pychoco.model import Model
from pychoco.objects.graphs.directed_graph import create_directed_graph, create_complete_directed_graph


class TestGraphNbStronglyConnectedComponents(unittest.TestCase):

    def test1(self):
        m = Model()
        lb = create_directed_graph(m, 4)
        ub = create_complete_directed_graph(m, 4)
        g = m.digraphvar(lb, ub, "g")
        nb = m.intvar(0, 3)
        m.graph_nb_strongly_connected_components(g, nb).post()
        while m.get_solver().solve():
            val = g.get_value().to_networkx_graph()
            if val.number_of_nodes() > 0:
                self.assertEqual(number_strongly_connected_components(val), nb.get_value())
