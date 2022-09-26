import unittest

from networkx import cycle_basis

from pychoco.model import Model
from pychoco.objects.graphs.undirected_graph import create_undirected_graph, create_complete_undirected_graph


class TestGraphCycle(unittest.TestCase):

    def test1(self):
        m = Model()
        lb = create_undirected_graph(m, 5)
        ub = create_complete_undirected_graph(m, 5)
        g = m.graphvar(lb, ub, "g")
        m.graph_cycle(g).post()
        while m.get_solver().solve():
            val = g.get_value().to_networkx_graph()
            # The cycle constraint of Choco allows empty graphs,
            # whereas networkx does not return cycle for empty graphs.
            if val.number_of_nodes() > 0:
                self.assertEqual(len(cycle_basis(val)[0]), val.number_of_nodes())
