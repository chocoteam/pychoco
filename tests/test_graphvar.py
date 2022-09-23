import unittest

from pychoco.model import Model
from pychoco.objects.graphs.directed_graph import DirectedGraph
from pychoco.objects.graphs.directed_graph import create_directed_graph
from pychoco.objects.graphs.undirected_graph import create_undirected_graph, UndirectedGraph


class TestGraphVar(unittest.TestCase):

    def test_undirected_graph_var(self):
        model = Model("MyModel")
        lb = create_undirected_graph(model, 10, [], [])
        ub = create_undirected_graph(model, 10, [0, 1, 2, 3], [[0, 1], [1, 3], [3, 2]])
        graphvar = model.graphvar(lb, ub, "g")
        llb = graphvar.get_lb()
        uub = graphvar.get_ub()
        self.assertIsInstance(llb, UndirectedGraph)
        self.assertIsInstance(uub, UndirectedGraph)
        self.assertFalse(graphvar.is_directed())
        self.assertEqual(len(llb.get_nodes()), 0)
        self.assertEqual(len(uub.get_nodes()), 4)
        self.assertEqual(graphvar.get_type(), "UndirectedGraphVar")
        g2 = model.graphvar(lb, lb, "g2")
        self.assertTrue(g2.is_instantiated())
        self.assertEqual(g2.get_value().get_nodes(), [])

    def test_node_induced_graph_var(self):
        model = Model("MyModel")
        lb = create_undirected_graph(model, 10, [], [])
        ub = create_undirected_graph(model, 10, [0, 1, 2, 3], [[0, 1], [1, 3], [3, 2]])
        graphvar = model.node_induced_graphvar(lb, ub, "g")
        llb = graphvar.get_lb()
        uub = graphvar.get_ub()
        self.assertIsInstance(llb, UndirectedGraph)
        self.assertIsInstance(uub, UndirectedGraph)
        self.assertFalse(graphvar.is_directed())
        self.assertEqual(len(llb.get_nodes()), 0)
        self.assertEqual(len(uub.get_nodes()), 4)
        self.assertEqual(graphvar.get_type(), "UndirectedGraphVar")
        g2 = model.node_induced_graphvar(lb, lb, "g2")
        self.assertTrue(g2.is_instantiated())
        self.assertEqual(g2.get_value().get_nodes(), [])

    def test_directed_graph_var(self):
        model = Model("MyModel")
        lb = create_directed_graph(model, 10, [], [])
        ub = create_directed_graph(model, 10, [0, 1, 2, 3], [[0, 1], [1, 3], [3, 2]])
        graphvar = model.digraphvar(lb, ub, "g")
        llb = graphvar.get_lb()
        uub = graphvar.get_ub()
        self.assertIsInstance(llb, DirectedGraph)
        self.assertIsInstance(uub, DirectedGraph)
        self.assertTrue(graphvar.is_directed())
        self.assertEqual(len(llb.get_nodes()), 0)
        self.assertEqual(len(uub.get_nodes()), 4)
        self.assertEqual(graphvar.get_type(), "DirectedGraphVar")
        g2 = model.digraphvar(lb, lb, "g2")
        self.assertTrue(g2.is_instantiated())
        self.assertEqual(g2.get_value().get_nodes(), [])

    def test_node_induced_digraph_var(self):
        model = Model("MyModel")
        lb = create_directed_graph(model, 10, [], [])
        ub = create_directed_graph(model, 10, [0, 1, 2, 3], [[0, 1], [1, 3], [3, 2]])
        graphvar = model.node_induced_digraphvar(lb, ub, "g")
        llb = graphvar.get_lb()
        uub = graphvar.get_ub()
        self.assertIsInstance(llb, DirectedGraph)
        self.assertIsInstance(uub, DirectedGraph)
        self.assertTrue(graphvar.is_directed())
        self.assertEqual(len(llb.get_nodes()), 0)
        self.assertEqual(len(uub.get_nodes()), 4)
        self.assertEqual(graphvar.get_type(), "DirectedGraphVar")
        g2 = model.node_induced_digraphvar(lb, lb, "g2")
        self.assertTrue(g2.is_instantiated())
        self.assertEqual(g2.get_value().get_nodes(), [])
