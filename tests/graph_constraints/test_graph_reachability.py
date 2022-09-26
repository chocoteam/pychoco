import unittest

from networkx.algorithms.tournament import is_reachable

from pychoco.model import Model
from pychoco.objects.graphs.directed_graph import create_directed_graph, create_complete_directed_graph


class TestGraphReachability(unittest.TestCase):

    def test1(self):
        m = Model()
        lb = create_directed_graph(m, 4)
        ub = create_complete_directed_graph(m, 4)
        g = m.digraphvar(lb, ub, "g")
        m.graph_reachability(g, 0).post()
        while m.get_solver().solve():
            val = g.get_value().to_networkx_graph()
            for i in g.get_value().get_nodes():
                is_reachable(val, i, 0)
