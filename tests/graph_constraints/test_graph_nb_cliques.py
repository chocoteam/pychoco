import unittest

import networkx as nx

from pychoco.model import Model
from pychoco.objects.graphs.undirected_graph import create_undirected_graph, create_complete_undirected_graph


class TestGraphNbCliques(unittest.TestCase):

    def test1(self):
        m = Model()
        lb = create_undirected_graph(m, 7)
        ub = create_complete_undirected_graph(m, 7)
        g = m.graphvar(lb, ub, "g")
        i = m.intvar(0, 10)
        m.graph_nb_cliques(g, i).post()
        while m.get_solver().solve():
            val = g.get_value().to_networkx_graph()
            # The cycle constraint of Choco allows empty graphs,
            # whereas networkx does not return cycle for empty graphs.
            if val.number_of_nodes() > 0:
                self.assertEqual(sum(1 for _ in nx.find_cliques(val)), i.get_value())
