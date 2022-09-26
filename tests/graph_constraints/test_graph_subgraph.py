import unittest

from pychoco.model import Model
from pychoco.objects.graphs.directed_graph import create_directed_graph, create_complete_directed_graph
from pychoco.objects.graphs.undirected_graph import create_undirected_graph, create_complete_undirected_graph


class TestGraphSubGraph(unittest.TestCase):

    def test1(self):
        m = Model()
        lb1 = create_undirected_graph(m, 4)
        lb2 = create_undirected_graph(m, 4)
        ub1 = create_complete_undirected_graph(m, 4)
        ub2 = create_complete_undirected_graph(m, 4)
        g1 = m.graphvar(lb1, ub1, "g")
        g2 = m.graphvar(lb2, ub2, "g")
        m.graph_subgraph(g1, g2).post()
        while m.get_solver().solve():
            val1 = g1.get_value()
            val2 = g2.get_value()
            for i in val1.get_nodes():
                self.assertTrue(i in val2.get_nodes())
                for j in val1.get_neighbors_of(i):
                    self.assertTrue(val2.contains_edge(i, j))

    def test2(self):
        m = Model()
        lb1 = create_directed_graph(m, 3)
        lb2 = create_directed_graph(m, 3)
        ub1 = create_complete_directed_graph(m, 3)
        ub2 = create_complete_directed_graph(m, 3)
        g1 = m.digraphvar(lb1, ub1, "g")
        g2 = m.digraphvar(lb2, ub2, "g")
        m.graph_subgraph(g1, g2).post()
        while m.get_solver().solve():
            val1 = g1.get_value()
            val2 = g2.get_value()
            for i in val1.get_nodes():
                self.assertTrue(i in val2.get_nodes())
                for j in val1.get_successors_of(i):
                    self.assertTrue(val2.contains_edge(i, j))
