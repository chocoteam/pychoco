from abc import ABC, abstractmethod
from typing import List

from pychoco import backend
from pychoco._utils import make_boolvar_array, make_intvar_array, make_int_array, make_setvar_array, get_boolvar_array
from pychoco._utils import make_int_2d_array, make_graphvar_array
from pychoco.objects.graphs.directed_graph import DirectedGraph
from pychoco.objects.graphs.undirected_graph import UndirectedGraph
from pychoco.variables.boolvar import BoolVar
from pychoco.variables.directed_graphvar import DirectedGraphVar
from pychoco.variables.graphvar import GraphVar
from pychoco.variables.intvar import IntVar
from pychoco.variables.setvar import SetVar
from pychoco.variables.undirected_graphvar import UndirectedGraphVar


class ViewFactory(ABC):
    """
    Factory for creating views.
    """

    @property
    @abstractmethod
    def _handle(self):
        pass

    # Boolean views

    def bool_not_view(self, boolvar: BoolVar):
        """
        Creates a boolean view over boolvar holding the logical negation of boolvar.
        :param boolvar: A BoolVar.
        :return: A bool_not_view.
        """
        handle = backend.bool_not_view(boolvar._handle)
        return BoolVar(handle, self)

    def set_bool_view(self, setvar: SetVar, value: int):
        """
        Creates a boolean view b over a set variable setvar such that:
        given value an integer, b = true iff setvar contains value.

        :param setvar: A SetVar.
        :param value: An int.
        :return: A set_bool_view
        """
        handle = backend.set_bool_view(setvar._handle, value)
        return BoolVar(handle, self)

    def set_bools_view(self, setvar: SetVar, size: int, offset: int = 0):
        """
        Creates an array of boolean views b over a set variable setvar such that:
        b[i - offset] = true <=> i in setvar.

        :param setvar: A SetVar.
        :param size: An int, size of the boolean view to return.
        :param offset: An int.
        :return: A list of boolean views.
        """
        handle = backend.set_bools_view(setvar._handle, size, offset)
        boolvars = get_boolvar_array(handle, self)
        return boolvars

    # Integer views

    def int_offset_view(self, intvar: IntVar, offset: int):
        """
        Creates a view based on intvar, equal to intvar + offset.

        :param intvar: An IntVar.
        :param offset: An int.
        :return: An int_offset_view.
        """
        handle = backend.int_offset_view(intvar._handle, offset)
        return IntVar(handle, self)

    def int_minus_view(self, intvar: IntVar):
        """
        Creates a view over intvar equal to -intvar. That is if intvar = [a,b], then int_minus_view(intvar) = [-b,-a].
        :param intvar: An IntVar.
        :return: An int_minus_view.
        """
        handle = backend.int_minus_view(intvar._handle)
        return IntVar(handle, self)

    def int_scale_view(self, intvar: IntVar, scale: int):
        """
        Creates a view over intvar equal to intvar * scale
        Requires scale > -2
        - if scale < -1, throws an exception;
        - if scale = -1, returns a minus view;
        - if scale = 0, returns a fixed variable;
        - if scale = 1, returns intvar;
        - otherwise, returns a scale view.

        :param intvar: An IntVar.
        :param scale: An int.
        :return: An int_scale_view.
        """
        assert scale > -2, "[int_scale_view] scale must be > -2"
        handle = backend.int_scale_view(intvar._handle, scale)
        return IntVar(handle, self)

    def int_abs_view(self, intvar: IntVar):
        """
        Creates a view over intvar such that: | intvar | .
        - if intvar is already instantiated, returns a fixed variable;
        - if the lower bound of intvar is greater or equal to 0, returns intvar;
        - if the upper bound of intvar is less or equal to 0, return a minus view;
        - otherwise, returns an absolute view.

        :param intvar: An IntVar.
        :return: An int_abs_view
        """
        handle = backend.int_abs_view(intvar._handle)
        return IntVar(handle, self)

    def int_affine_view(self, a: int, intvar: IntVar, b: int):
        """
        Creates an affine view over intvar such that: a * intvar + b.

        :param a: An int.
        :param intvar: An IntVar.
        :param b: An int.
        :return: An int_affine_view.
        """
        handle = backend.int_affine_view(a, intvar._handle, b)
        return IntVar(handle, self)

    def int_eq_view(self, intvar: IntVar, value: int):
        """
        Creates a boolean view over intvar such that: intvar == c.

        :param intvar: An IntVar.
        :param value:  An int.
        :return:  An int_eq_view.
        """
        handle = backend.int_eq_view(intvar._handle, value)
        return BoolVar(handle, self)

    def int_ne_view(self, intvar: IntVar, value: int):
        """
        Creates a boolean view over intvar such that: intvar != c.

        :param intvar: An IntVar.
        :param value:  An int.
        :return:  An int_ne_view.
        """
        handle = backend.int_ne_view(intvar._handle, value)
        return BoolVar(handle, self)

    def int_le_view(self, intvar: IntVar, value: int):
        """
        Creates a boolean view over intvar such that: intvar <= c.

        :param intvar: An IntVar.
        :param value:  An int.
        :return:  An int_le_view.
        """
        handle = backend.int_le_view(intvar._handle, value)
        return BoolVar(handle, self)

    def int_ge_view(self, intvar: IntVar, value: int):
        """
        Creates a boolean view over intvar such that: intvar >= c.

        :param intvar: An IntVar.
        :param value:  An int.
        :return:  An int_ge_view.
        """
        handle = backend.int_ge_view(intvar._handle, value)
        return BoolVar(handle, self)

    # Set views

    def bools_set_view(self, boolvars: List[BoolVar], offset: int = 0):
        """
        Create a set view over an array of boolean variables defined such that:
        boolvars[x - offset] = True <=> x in set view.
        This view is equivalent to the set_bools_channeling constraint.

        :param boolvars: A list of BoolVar.
        :param offset: An int.
        :return: A bools_set_view.
        """
        bools_handle = make_boolvar_array(boolvars)
        handle = backend.bools_set_view(bools_handle, offset)
        return SetVar(handle, self)

    def ints_set_view(self, intvars: List[IntVar], values: List[int], offset: int = 0):
        """
        Create a set view over an array of integer variables, such that:
        intvars[x - offset] = value[x - offset] <=> x in set view.

        :param intvars: A list of IntVars.
        :param values: A list of ints.
        :param offset: An int.
        :return: An ints_set_view.
        """
        assert len(intvars) == len(values), "[ints_set_view] 'intvars' and 'values' must have the same length"
        vars_handle = make_intvar_array(intvars)
        values_handle = make_int_array(values)
        handle = backend.ints_set_view(vars_handle, values_handle, offset)
        return SetVar(handle, self)

    def set_union_view(self, setvars: List[SetVar]):
        """
        Creates a set view representing the union of a list of set variables.

        :param setvars: A list of SetVars.
        :return: A set_union_view.
        """
        vars_handle = make_setvar_array(setvars)
        handle = backend.set_union_view(vars_handle)
        return SetVar(handle, self)

    def set_intersection_view(self, setvars: List[SetVar]):
        """
        Creates a set view representing the intersection of a list of set variables.

        :param setvars: A list of SetVars.
        :return: A set_intersection_view.
        """
        vars_handle = make_setvar_array(setvars)
        handle = backend.set_intersection_view(vars_handle)
        return SetVar(handle, self)

    def set_difference_view(self, setvar_1: SetVar, setvar_2: SetVar):
        """
        Creates a set view representing the set difference between setvar_1 and setvar_2:  setvar_1 \\ setvar_2.

        :param setvar_1: A SetVar.
        :param setvar_2: A SetVar.
        :return: A set_difference_view.
        """
        handle = backend.set_difference_view(setvar_1._handle, setvar_2._handle)
        return SetVar(handle, self)

    # Graph views

    def graph_node_set_view(self, graphvar: "GraphVar"):
        """
        Creates a set view over the set of nodes of a graph variable.

        :param graphvar: A GraphVar (Directed or Undirected).
        :return: A graph_node_set_view.
        """
        handle = backend.graph_node_set_view(graphvar._handle)
        return SetVar(handle, self)

    def graph_successors_set_view(self, digraphvar: "DirectedGraphVar", node: int):
        """
        Creates a set view over the set of successors of a node of a directed graph variable.

        :param digraphvar: A DirectedGraphVar.
        :param node: An int.
        :return: A graph_successors_set_view.
        """
        handle = backend.graph_successors_set_view(digraphvar._handle, node)
        return SetVar(handle, self)

    def graph_predecessors_set_view(self, digraphvar: "DirectedGraphVar", node: int):
        """
        Creates a set view over the set of predecessors of a node of a directed graph variable.

        :param digraphvar: A Directed GraphVar.
        :param node: An int.
        :return: A graph_predecessors_set_view.
        """
        handle = backend.graph_predecessors_set_view(digraphvar._handle, node)
        return SetVar(handle, self)

    def graph_neighbors_set_view(self, graphvar: "UndirectedGraphVar", node: int):
        """
        Creates a set view over the set of neighbors of a node of an undirected graph variable.

        :param graphvar: An UndirectedGraphVar.
        :param node: An int.
        :return: A graph_neighbors_set_view.
        """
        handle = backend.graph_neighbors_set_view(graphvar._handle, node)
        return SetVar(handle, self)

    def node_induced_subgraph_view(self, graphvar: "GraphVar", nodes: List[int], exclude: bool = False):
        """
         Creates a graph view G' = (V', E') from another graph G = (V, E) such that:
         - V' = V - nodes (set difference) if exclude = true, else V' = V intersection nodes (set intersection)
         - E' = { (x, y) in E | x  in V' and y in V' }.

        :param graphvar: A GraphVar (Directed or Undirected).
        :param nodes: A list of ints.
        :param exclude: A bool.
        :return: A node_induced_subgraph_view.
        """
        assert len(nodes) > 0
        nodes_handle = make_int_array(nodes)
        handle = backend.node_induced_subgraph_view(graphvar._handle, nodes_handle, exclude)
        return _make_graphview(handle, self, graphvar)

    def edge_induced_subgraph_view(self, graphvar: "GraphVar", edges: List[List[int]], exclude: bool = False):
        """
        Construct an edge-induced subgraph view G = (V', E') from G = (V, E) such that:
        - V' = { x in V | Exists y in V s.t. (x, y) in E' }
        - E' = E - edges (set difference) if exclude = true, else E' = E intersection edges (set intersection).

        :param graphvar: A GraphVar (Directed or Undirected).
        :param edges: A list of edges.
        :param exclude: A bool.
        :return: An edge_induced_subgraph_view.
        """
        assert len(edges) > 0
        for e in edges:
            assert len(e) == 2
        edges_handle = make_int_2d_array(edges)
        handle = backend.edge_induced_subgraph_view(graphvar._handle, edges_handle, exclude)
        return _make_graphview(handle, self, graphvar)

    def graph_union_view(self, graphvars: List["GraphVar"]):
        """
        Construct an graph union view G = (V, E) from a set of graphs {G_1 = (V_1, E_1), ..., G_k = (V_k, E_k)}
        such that :
        - V = V_1 union ... union V_k (set union);
        - E = E_1 union ... union E_k.
        Note: all graphs in graphvar must be of the same type.

        :param graphvars: A list of GraphVars (Directed or Undirected, but all the same type).
        :return: A graph_union_view.
        """
        assert len(graphvars) >= 2
        cls = graphvars[0].__class__
        nb_max_nodes = graphvars[0].get_nb_max_nodes()
        for g in graphvars:
            assert g.get_nb_max_nodes() == nb_max_nodes, \
                "[graph_union_view] All graphs must have the same maximum number of nodes"
            assert isinstance(g, cls), "[graph_union_view] All graph variables must have the same type."
        graphvars_handle = make_graphvar_array(graphvars)
        handle = backend.graph_union_view(graphvars_handle)
        return _make_graphview(handle, self, graphvars[0])


def _make_graphview(handle, model, graphvar):
    if isinstance(graphvar, UndirectedGraphVar):
        lb = UndirectedGraph(model, 0, _handle=backend.get_graphvar_lb(handle))
        ub = UndirectedGraph(model, 0, _handle=backend.get_graphvar_ub(handle))
        return UndirectedGraphVar(handle, model, lb, ub)
    else:
        lb = DirectedGraph(graphvar.model, 0, _handle=backend.get_graphvar_lb(handle))
        ub = DirectedGraph(graphvar.model, 0, _handle=backend.get_graphvar_ub(handle))
        return DirectedGraphVar(handle, model, lb, ub)
