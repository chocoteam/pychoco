import unittest

from networkx import recursive_simple_cycles

from pychoco.model import Model
from pychoco.objects.graphs.directed_graph import create_directed_graph, create_complete_directed_graph


class TestGraphMinOutDegree(unittest.TestCase):

    def test1(self):
        m = Model()
        lb = create_directed_graph(m, 4)
        ub = create_complete_directed_graph(m, 4)
        g = m.digraphvar(lb, ub, "g")
        m.graph_no_circuit(g).post()
        while m.get_solver().solve():
            val = g.get_value().to_networkx_graph()
            self.assertEqual(len(recursive_simple_cycles(val)), 0)
