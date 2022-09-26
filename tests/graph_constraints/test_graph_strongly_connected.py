import unittest

from networkx.algorithms.tournament import is_strongly_connected

from pychoco.model import Model
from pychoco.objects.graphs.directed_graph import create_directed_graph, create_complete_directed_graph


class TestGraphNbStronglyConnectedComponents(unittest.TestCase):

    def test1(self):
        m = Model()
        lb = create_directed_graph(m, 3)
        ub = create_complete_directed_graph(m, 3)  # TODO: there may be a bug in Choco strongly connected constraint
        g = m.digraphvar(lb, ub, "g")
        m.graph_strongly_connected(g).post()
        while m.get_solver().solve():
            val = g.get_value().to_networkx_graph()
            if val.number_of_nodes() > 0:
                self.assertTrue(is_strongly_connected(val))
