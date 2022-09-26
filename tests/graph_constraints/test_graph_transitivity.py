import unittest

from pychoco.model import Model
from pychoco.objects.graphs.directed_graph import create_directed_graph, create_complete_directed_graph
from pychoco.objects.graphs.undirected_graph import create_undirected_graph, create_complete_undirected_graph


class TestGraphTransitivity(unittest.TestCase):

    def test1(self):
        m = Model()
        lb = create_undirected_graph(m, 5)
        ub = create_complete_undirected_graph(m, 5)
        g = m.graphvar(lb, ub, "g")
        m.graph_transitivity(g).post()
        while m.get_solver().solve():
            val = g.get_value()
            for i in val.get_nodes():
                for j in val.get_neighbors_of(i):
                    for k in val.get_neighbors_of(j):
                        if k != i:
                            self.assertTrue(val.contains_edge(i, k))

    def test2(self):
        m = Model()
        lb = create_directed_graph(m, 4)
        ub = create_complete_directed_graph(m, 4)
        g = m.digraphvar(lb, ub, "g")
        m.graph_transitivity(g).post()
        while m.get_solver().solve():
            val = g.get_value()
            for i in val.get_nodes():
                for j in val.get_successors_of(i):
                    for k in val.get_successors_of(j):
                        if k != i:
                            self.assertTrue(val.contains_edge(i, k))
