import unittest

from pychoco.model import Model
from pychoco.objects.graphs.directed_graph import create_directed_graph, create_complete_directed_graph
from pychoco.objects.graphs.undirected_graph import create_undirected_graph, create_complete_undirected_graph
from pychoco.variables.boolvar import BoolVar


class TestViews(unittest.TestCase):

    def test_bool_not_view(self):
        m = Model()
        b = m.boolvar()
        not_b = m.bool_not_view(b)
        self.assertTrue(not_b.is_view())
        while m.get_solver().solve():
            self.assertFalse(b.get_value() and not_b.get_value())
            self.assertTrue(b.get_value() or not_b.get_value())

    def test_set_bool_view(self):
        m = Model()
        setvar = m.setvar([], range(0, 10))
        b = m.set_bool_view(setvar, 5)
        self.assertTrue(b.is_view())
        while m.get_solver().solve():
            self.assertEqual(b.get_value(), 5 in setvar.get_value())

    def test_set_bools_view(self):
        m = Model()
        setvar = m.setvar([], range(0, 10))
        bools = m.set_bools_view(setvar, 10)
        [self.assertTrue(b.is_view()) for b in bools]
        while m.get_solver().solve():
            for i in range(0, 10):
                self.assertEqual(i in setvar.get_value(), bools[i].get_value())

    def test_int_offset_view(self):
        m = Model()
        intvar = m.intvar(0, 10)
        int_offset = m.int_offset_view(intvar, 2)
        self.assertTrue(int_offset.is_view())
        while m.get_solver().solve():
            self.assertEqual(intvar.get_value(), int_offset.get_value() - 2)

    def test_minus_view(self):
        m = Model()
        intvar = m.intvar(0, 10)
        int_minus = m.int_minus_view(intvar)
        self.assertTrue(int_minus.is_view())
        while m.get_solver().solve():
            self.assertEqual(intvar.get_value(), -int_minus.get_value())

    def test_int_scale_view(self):
        m = Model()
        intvar = m.intvar(0, 10)
        int_scale = m.int_scale_view(intvar, 2)
        self.assertTrue(int_scale.is_view())
        while m.get_solver().solve():
            self.assertEqual(intvar.get_value() * 2, int_scale.get_value())

    def test_int_abs_view(self):
        m = Model()
        intvar = m.intvar(-10, 10)
        int_abs = m.int_abs_view(intvar)
        while m.get_solver().solve():
            self.assertEqual(abs(intvar.get_value()), int_abs.get_value())

    def test_int_affine_view(self):
        m = Model()
        intvar = m.intvar(0, 10)
        affine_view = m.int_affine_view(2, intvar, 1)
        self.assertTrue(affine_view.is_view())
        while m.get_solver().solve():
            self.assertEqual(2 * intvar.get_value() + 1, affine_view.get_value())

    def test_int_eq_view(self):
        m = Model()
        intvar = m.intvar(0, 10)
        b = m.int_eq_view(intvar, 2)
        self.assertTrue(b.is_view())
        self.assertTrue(isinstance(b, BoolVar))
        while m.get_solver().solve():
            self.assertEqual(intvar.get_value() == 2, b.get_value())

    def test_int_ne_view(self):
        m = Model()
        intvar = m.intvar(0, 10)
        b = m.int_ne_view(intvar, 2)
        self.assertTrue(b.is_view())
        self.assertTrue(isinstance(b, BoolVar))
        while m.get_solver().solve():
            self.assertEqual(intvar.get_value() != 2, b.get_value())

    def test_int_le_view(self):
        m = Model()
        intvar = m.intvar(0, 10)
        b = m.int_le_view(intvar, 2)
        self.assertTrue(b.is_view())
        self.assertTrue(isinstance(b, BoolVar))
        while m.get_solver().solve():
            self.assertEqual(intvar.get_value() <= 2, b.get_value())

    def test_int_ge_view(self):
        m = Model()
        intvar = m.intvar(0, 10)
        b = m.int_ge_view(intvar, 2)
        self.assertTrue(b.is_view())
        self.assertTrue(isinstance(b, BoolVar))
        while m.get_solver().solve():
            self.assertEqual(intvar.get_value() >= 2, b.get_value())

    def test_bools_set_view(self):
        m = Model()
        boolvars = m.boolvars(10)
        set_view = m.bools_set_view(boolvars, offset=2)
        self.assertTrue(set_view.is_view())
        while m.get_solver().solve():
            for i in range(0, 10):
                if boolvars[i].get_value():
                    self.assertTrue(i + 2 in set_view.get_value())
                else:
                    self.assertFalse(i + 2 in set_view.get_value())

    def test_ints_set_view(self):
        m = Model()
        intvars = m.intvars(5, 0, 5)
        v = range(0, 5)
        set_view = m.ints_set_view(intvars, v)
        self.assertTrue(set_view.is_view())
        while m.get_solver().solve():
            for i in range(0, 5):
                self.assertEqual(intvars[i].get_value() == v[i], i in set_view.get_value())

    def test_set_union_view(self):
        m = Model()
        a = m.setvar(set([]), set(range(0, 5)))
        b = m.setvar(set([]), set(range(5, 10)))
        c = m.setvar(set([]), set(range(10, 15)))
        union = m.set_union_view([a, b, c])
        self.assertTrue(union.is_view())
        while m.get_solver().solve():
            self.assertSetEqual(
                a.get_value().union(b.get_value().union(c.get_value())),
                union.get_value()
            )

    def test_set_intersection_view(self):
        m = Model()
        a = m.setvar(set([]), set(range(0, 5)))
        b = m.setvar(set([]), set(range(5, 10)))
        c = m.setvar(set([]), set(range(10, 15)))
        intersection = m.set_intersection_view([a, b, c])
        self.assertTrue(intersection.is_view())
        while m.get_solver().solve():
            self.assertSetEqual(
                a.get_value().intersection(b.get_value().intersection(c.get_value())),
                intersection.get_value()
            )

    def test_set_difference_view(self):
        m = Model()
        a = m.setvar([], range(0, 5))
        b = m.setvar([], range(0, 7))
        diff = m.set_difference_view(a, b)
        self.assertTrue(diff.is_view())
        while m.get_solver().solve():
            self.assertSetEqual(
                a.get_value().difference(b.get_value()),
                diff.get_value()
            )

    def test_graph_node_set_view(self):
        m = Model()
        lb = create_undirected_graph(m, 5)
        ub = create_complete_undirected_graph(m, 5)
        g = m.graphvar(lb, ub, "g")
        s = m.graph_node_set_view(g)
        self.assertTrue(s.is_view())
        while m.get_solver().solve():
            self.assertSetEqual(s.get_value(), set(g.get_value().get_nodes()))

    def test_graph_successors_set_view(self):
        m = Model()
        lb = create_directed_graph(m, 4)
        ub = create_complete_directed_graph(m, 4)
        g = m.digraphvar(lb, ub, "g")
        s = m.graph_successors_set_view(g, 2)
        self.assertTrue(s.is_view())
        while m.get_solver().solve():
            self.assertSetEqual(s.get_value(), set(g.get_value().get_successors_of(2)))

    def test_graph_predecessors_set_view(self):
        m = Model()
        lb = create_directed_graph(m, 4)
        ub = create_complete_directed_graph(m, 4)
        g = m.digraphvar(lb, ub, "g")
        s = m.graph_predecessors_set_view(g, 2)
        self.assertTrue(s.is_view())
        while m.get_solver().solve():
            self.assertSetEqual(s.get_value(), set(g.get_value().get_predecessors_of(2)))

    def test_graph_neighbors_set_view(self):
        m = Model()
        lb = create_undirected_graph(m, 5)
        ub = create_complete_undirected_graph(m, 5)
        g = m.graphvar(lb, ub, "g")
        s = m.graph_neighbors_set_view(g, 2)
        self.assertTrue(s.is_view())
        while m.get_solver().solve():
            self.assertSetEqual(s.get_value(), set(g.get_value().get_neighbors_of(2)))

    def test_node_induced_subgraph_view(self):
        m = Model()
        lb = create_undirected_graph(m, 5)
        ub = create_complete_undirected_graph(m, 5)
        g = m.graphvar(lb, ub, "g")
        nodes = [0, 1, 2]
        view = m.node_induced_subgraph_view(g, nodes)
        self.assertTrue(view.is_view())
        self.assertFalse(view.is_directed())
        while m.get_solver().solve():
            for i in g.get_value().get_nodes():
                if i in nodes:
                    self.assertTrue(i in view.get_value().get_nodes())
                    for j in g.get_value().get_neighbors_of(i):
                        if j in nodes:
                            self.assertTrue(j in view.get_value().get_neighbors_of(i))
                        else:
                            self.assertFalse(view.get_value().contains_edge(i, j))
                else:
                    self.assertFalse(i in view.get_value().get_nodes())

    def test_node_induced_subgraph_view_directed(self):
        m = Model()
        lb = create_directed_graph(m, 4)
        ub = create_complete_directed_graph(m, 4)
        g = m.digraphvar(lb, ub, "g")
        nodes = [0, 1]
        view = m.node_induced_subgraph_view(g, nodes)
        self.assertTrue(view.is_directed())
        self.assertTrue(view.is_view())
        while m.get_solver().solve():
            for i in g.get_value().get_nodes():
                if i in nodes:
                    self.assertTrue(i in view.get_value().get_nodes())
                    for j in g.get_value().get_successors_of(i):
                        if j in nodes:
                            self.assertTrue(j in view.get_value().get_successors_of(i))
                        else:
                            self.assertFalse(view.get_value().contains_edge(i, j))
                else:
                    self.assertFalse(i in view.get_value().get_nodes())

    def test_edge_induced_subgraph_view(self):
        m = Model()
        lb = create_undirected_graph(m, 5)
        ub = create_complete_undirected_graph(m, 5)
        g = m.graphvar(lb, ub, "g")
        edges = [[0, 1], [1, 2], [2, 3]]
        view = m.edge_induced_subgraph_view(g, edges)
        self.assertTrue(view.is_view())
        self.assertFalse(view.is_directed())
        while m.get_solver().solve():
            for i in g.get_value().get_nodes():
                cond = i in [0, 1, 2, 3] \
                       and len([j for j in g.get_value().get_neighbors_of(i) if [i, j] in edges or [j, i] in edges]) > 0
                if cond:
                    self.assertTrue(i in view.get_value().get_nodes())
                    for j in g.get_value().get_neighbors_of(i):
                        if [i, j] in edges or [j, i] in edges:
                            self.assertTrue(view.get_value().contains_edge(i, j))
                        else:
                            self.assertFalse(view.get_value().contains_edge(i, j))
                else:
                    self.assertFalse(i in view.get_value().get_nodes())

    def test_edge_induced_subgraph_view_directed(self):
        m = Model()
        lb = create_directed_graph(m, 4)
        ub = create_complete_directed_graph(m, 4)
        g = m.digraphvar(lb, ub, "g")
        edges = [[0, 1], [1, 2]]
        view = m.edge_induced_subgraph_view(g, edges)
        self.assertTrue(view.is_directed())
        self.assertTrue(view.is_view())
        while m.get_solver().solve():
            for i in g.get_value().get_nodes():
                cond = i in [0, 1, 2] \
                       and (len([j for j in g.get_value().get_successors_of(i) if [i, j] in edges]) > 0
                            or len([j for j in g.get_value().get_predecessors_of(i) if [j, i] in edges]) > 0)
                if cond:
                    self.assertTrue(i in view.get_value().get_nodes())
                    for j in g.get_value().get_successors_of(i):
                        if [i, j] in edges:
                            self.assertTrue(view.get_value().contains_edge(i, j))
                        else:
                            self.assertFalse(view.get_value().contains_edge(i, j))
                else:
                    self.assertFalse(i in view.get_value().get_nodes())

    def test_graph_union_view(self):
        m = Model()
        lb = [create_undirected_graph(m, 3) for i in range(0, 3)]
        ub = [create_complete_undirected_graph(m, 3) for i in range(0, 3)]
        graphs = [m.graphvar(lb[i], ub[i], "g") for i in range(0, 3)]
        union = m.graph_union_view(graphs)
        self.assertTrue(union.is_view())
        while m.get_solver().solve():
            for g in graphs:
                for i in g.get_value().get_nodes():
                    self.assertTrue(i in union.get_value().get_nodes())
                    for j in g.get_value().get_neighbors_of(i):
                        self.assertTrue(union.get_value().contains_edge(i, j))

    def test_graph_union_view_directed(self):
        m = Model()
        lb = [create_directed_graph(m, 3) for i in range(0, 2)]
        ub = [create_complete_directed_graph(m, 3) for i in range(0, 2)]
        graphs = [m.digraphvar(lb[i], ub[i], "g") for i in range(0, 2)]
        union = m.graph_union_view(graphs)
        self.assertTrue(union.is_view())
        while m.get_solver().solve():
            for g in graphs:
                for i in g.get_value().get_nodes():
                    self.assertTrue(i in union.get_value().get_nodes())
                    for j in g.get_value().get_successors_of(i):
                        self.assertTrue(union.get_value().contains_edge(i, j))
