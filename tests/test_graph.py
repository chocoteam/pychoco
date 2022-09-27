import unittest

from pychoco.model import Model
from pychoco.objects.graphs.directed_graph import DirectedGraph
from pychoco.objects.graphs.directed_graph import create_directed_graph
from pychoco.objects.graphs.undirected_graph import UndirectedGraph
from pychoco.objects.graphs.undirected_graph import create_undirected_graph


class TestGraph(unittest.TestCase):

    def test_undirected_graph(self):
        model = Model()
        g = UndirectedGraph(model, 10, "BITSET", "BIPARTITE_SET")
        self.assertFalse(g.is_directed())
        self.assertEqual(g.get_nb_max_nodes(), 10)
        self.assertEqual(len(g.get_nodes()), 0)
        self.assertEqual(g.get_node_set_type(), "BITSET")
        self.assertEqual(g.get_edge_set_type(), "BIPARTITE_SET")
        self.assertTrue(g.add_node(0))
        self.assertTrue(g.add_node(1))
        self.assertTrue(g.add_node(2))
        self.assertTrue(g.contains_node(0) and g.contains_node(1) and g.contains_node(2))
        self.assertEqual(set(g.get_nodes()), set([0, 1, 2]))
        self.assertFalse(g.contains_node(4))
        self.assertFalse(g.contains_edge(0, 1))
        self.assertTrue(g.add_edge(0, 1))
        self.assertTrue(g.contains_edge(0, 1))
        self.assertTrue(g.remove_node(2))
        self.assertFalse(g.remove_node(2))
        self.assertFalse(g.contains_node(2))
        self.assertEqual(g.get_neighbors_of(0), [1])
        self.assertTrue(g.remove_edge(1, 0))
        self.assertEqual(g.get_neighbors_of(0), [])
        g.graphviz_export()

    def test_directed_graph(self):
        model = Model()
        g = DirectedGraph(model, 10, "RANGE_SET", "BIPARTITE_SET")
        self.assertTrue(g.is_directed())
        self.assertEqual(g.get_nb_max_nodes(), 10)
        self.assertEqual(len(g.get_nodes()), 0)
        self.assertEqual(g.get_node_set_type(), "RANGE_SET")
        self.assertEqual(g.get_edge_set_type(), "BIPARTITE_SET")
        self.assertTrue(g.add_node(0))
        self.assertTrue(g.add_node(1))
        self.assertTrue(g.add_node(2))
        self.assertTrue(g.contains_node(0) and g.contains_node(1) and g.contains_node(2))
        self.assertEqual(set(g.get_nodes()), set([0, 1, 2]))
        self.assertFalse(g.contains_node(4))
        self.assertFalse(g.contains_edge(0, 1))
        self.assertTrue(g.add_edge(0, 1))
        self.assertTrue(g.contains_edge(0, 1))
        self.assertTrue(g.remove_node(2))
        self.assertFalse(g.remove_node(2))
        self.assertFalse(g.contains_node(2))
        self.assertEqual(g.get_successors_of(0), [1])
        self.assertEqual(g.get_successors_of(1), [])
        self.assertEqual(g.get_predecessors_of(1), [0])
        self.assertFalse(g.remove_edge(1, 0))
        self.assertTrue(g.remove_edge(0, 1))
        self.assertEqual(g.get_successors_of(0), [])
        g.graphviz_export()

    def test_factory_methods(self):
        m = Model()
        g1 = create_undirected_graph(m, 10, [0, 1, 2, 3], [[0, 1], [1, 3], [3, 2]])
        self.assertFalse(g1.is_directed())
        self.assertSetEqual(set(g1.get_nodes()), set([0, 1, 2, 3]))
        self.assertTrue(g1.contains_edge(0, 1))
        self.assertTrue(g1.contains_edge(1, 3))
        self.assertTrue(g1.contains_edge(3, 2))
        g2 = create_directed_graph(m, 10, [0, 1, 2, 3], [[0, 1], [1, 3], [3, 2]])
        self.assertTrue(g2.is_directed())
        self.assertSetEqual(set(g1.get_nodes()), set([0, 1, 2, 3]))
        self.assertTrue(g1.contains_edge(0, 1))
        self.assertTrue(g1.contains_edge(1, 3))
        self.assertTrue(g1.contains_edge(3, 2))
