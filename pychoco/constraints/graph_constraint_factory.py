from abc import ABC, abstractmethod
from typing import Union, List

from pychoco import backend
from pychoco._utils import make_intvar_array, make_boolvar_2d_array
from pychoco._utils import make_setvar_array, make_boolvar_array, make_int_array
from pychoco.constraints.constraint import Constraint
from pychoco.variables.boolvar import BoolVar
from pychoco.variables.directed_graphvar import DirectedGraphVar
from pychoco.variables.graphvar import GraphVar
from pychoco.variables.intvar import IntVar
from pychoco.variables.setvar import SetVar
from pychoco.variables.undirected_graphvar import UndirectedGraphVar


class GraphConstraintFactory(ABC):
    """
    Constraints over graph variables.
    """

    @property
    @abstractmethod
    def _handle(self):
        pass

    @staticmethod
    def _assert_undirected(graphvar, name_constraint):
        assert isinstance(graphvar, UndirectedGraphVar), "[{}] Only applies to UndirectedGraphVar".format(
            name_constraint)

    @staticmethod
    def _assert_directed(graphvar, name_constraint):
        assert isinstance(graphvar, DirectedGraphVar), "[{}] Only applies to DirectedGraphVar".format(name_constraint)

    def graph_nb_nodes(self, graphvar: GraphVar, nb_nodes: IntVar):
        """
        Create a constraint to force the number of nodes in graphvar to be equal to nb_nodes.

        :param graphvar: A GraphVar (Directed or Undirected).
        :param nb_nodes: An IntVar.
        :return: A graph_nb_nodes constraint.
        """
        handle = backend.graph_nb_nodes(self._handle, graphvar._handle, nb_nodes._handle)
        return Constraint(handle, self)

    def graph_nb_edges(self, graphvar: GraphVar, nb_edges: IntVar):
        """
        Create a constraint to force the number of edges in graphvar to be equal to nb_edges.

        :param graphvar: A GraphVar (Directed or Undirected).
        :param nb_edges: An IntVar.
        :return: A graph_nb_edges constraint.
        """
        handle = backend.graph_nb_edges(self._handle, graphvar._handle, nb_edges._handle)
        return Constraint(handle, self)

    def graph_loop_set(self, graphvar: GraphVar, loop_set: SetVar):
        """
        Create a constraint which ensures that 'loop_set' denotes the set
        of vertices in g which have a loop, i.e. an edge of the form f(i, i)
        i.e. vertex i in graphvar => edge (i, i) in graphvar.

        :param graphvar: A GraphVar (Directed or Undirected).
        :param loop_set: A SetVar.
        :return: A graph_loop_set constraint.
        """
        handle = backend.graph_loop_set(self._handle, graphvar._handle, loop_set._handle)
        return Constraint(handle, self)

    def graph_nb_loops(self, graphvar: GraphVar, nb_loops: IntVar):
        """
        Create a constraint which ensures graphvar has nb_loops loops | (i, i) in graphvar | = nb_loops

        :param graphvar: A GraphVar (Directed or Undirected).
        :param nb_loops: An IntVar.
        :return: A graph_nb_loops constraint.
        """
        handle = backend.graph_nb_loops(self._handle, graphvar._handle, nb_loops._handle)
        return Constraint(handle, self)

    def graph_symmetric(self, digraphvar: DirectedGraphVar):
        """
        Creates a constraint which ensures that digraphvar is symmetric.
        This means (i, j) in digraphvar <=> (j, i) in digraphvar.
        Note that it may be preferable to use an undirected graph variable instead !

        :param digraphvar: A DirectedGraphVar.
        :return: A graph_symmetric constraint.
        """
        self._assert_directed(digraphvar, "graph_symmetric")
        handle = backend.graph_symmetric(self._handle, digraphvar._handle)
        return Constraint(handle, self)

    def graph_anti_symmetric(self, digraphvar: DirectedGraphVar):
        """
        Creates a constraint which ensures that digraphvar is antisymmetric.
        This means (i, j) in digraphvar => (j, i) not in digraphvar.

        :param digraphvar: A DirectedGraphVar.
        :return: A graph_anti_symmetric constraint.
        """
        self._assert_directed(digraphvar, "graph_anti_symmetric")
        handle = backend.graph_anti_symmetric(self._handle, digraphvar._handle)
        return Constraint(handle, self)

    def graph_transitivity(self, graphvar: GraphVar):
        """
        Create a transitivity constraint: (i, j) in graphvar and (j, k) in graphvar => (i, k) in graphvar.
        Does not consider loops, enables to make cliques.

        :param graphvar: A GraphVar (Directed or Undirected).
        :return: A graph_transitivity constraint.
        """
        handle = backend.graph_transitivity(self._handle, graphvar._handle)
        return Constraint(handle, self)

    def graph_subgraph(self, graphvar_1: Union[UndirectedGraphVar, DirectedGraphVar],
                       graphvar_2: Union[UndirectedGraphVar, DirectedGraphVar]):
        """
        Create an inclusion constraint between graphvar_1 and graphvar_2 such that
        graphvar_1 is a subgraph of graphvar_2.
        Note that node are labelled with their indexes : the vertex 0 in graphvar_1 corresponds to the
        vertex 0 in graphvar_2.
        Important: graphvar_1 and graphvar_2 must be either both directed, or both undirected.

        :param graphvar_1: A GraphVar (Directed or Undirected).
        :param graphvar_2: A GraphVar (Directed or Undirected).
        :return: A graph_subgraph constraint.
        """
        if isinstance(graphvar_1, UndirectedGraphVar):
            assert isinstance(graphvar_2,
                              UndirectedGraphVar), "[graph_subgraph] Both graph variables must have the same type"
        elif isinstance(graphvar_1, DirectedGraphVar):
            assert isinstance(graphvar_2,
                              DirectedGraphVar), "[graph_subgraph] Both graph variables must have the same type"
        else:
            raise Exception("[graph_subgraph] Only applies to graph variables")
        handle = backend.graph_subgraph(self._handle, graphvar_1._handle, graphvar_2._handle)
        return Constraint(handle, self)

    def graph_nodes_channeling(self, graphvar: GraphVar, setvar_or_boolvars: Union[SetVar, List[BoolVar]]):
        """
        Channeling constraint :
        - if `setvar_or_boolvars` is a SetVar: int i in setvar_or_boolvars <=> vertex i in graphvar
        - if `setvar_or_boolvars` is a list of BoolVars: setvar_or_boolvars[i] = 1 <=> vertex i in graphvar

        :param graphvar: A GraphVar (Directed or Undirected).
        :param setvar_or_boolvars: A SetVar or a list of BoolVars.
        :return: A graph_nodes_channeling constraint.
        """
        if isinstance(setvar_or_boolvars, SetVar):
            handle = backend.graph_nodes_channeling_set(self._handle, graphvar._handle, setvar_or_boolvars._handle)
        else:
            bools_handle = make_boolvar_array(setvar_or_boolvars)
            handle = backend.graph_nodes_channeling_bools(self._handle, graphvar._handle, bools_handle)
        return Constraint(handle, self)

    def graph_node_channeling(self, graphvar: GraphVar, is_in: BoolVar, node: int):
        """
        Channeling constraint : is_in = 1 <=> vertex 'node' in graphvar

        :param graphvar: A GraphVar (Directed or Undirected).
        :param is_in: A BoolVar.
        :param node: An int.
        :return: A graph_node_channeling constraint.
        """
        handle = backend.graph_node_channeling(self._handle, graphvar._handle, is_in._handle, node)
        return Constraint(handle, self)

    def graph_edge_channeling(self, graphvar: GraphVar, is_in: BoolVar, source: int, destination: int):
        """
        Channeling constraint : is_in = 1 <=> edge (source, destination) in graphvar.

        :param graphvar: A GraphVar (Directed or Undirected).
        :param is_in: A BoolVar.
        :param source: An int.
        :param destination: An int.
        :return: A graph_edge_channeling constraint.
        """
        handle = backend.graph_edge_channeling(self._handle, graphvar._handle, is_in._handle, source, destination)
        return Constraint(handle, self)

    def graph_neighbors_channeling(self, graphvar: UndirectedGraphVar,
                                   setvars_or_boolvars: Union[List[SetVar], List[List[BoolVar]]]):
        """
        Channeling constraint:
        - if `setvars_or_boolvars` is a list of SetVars: int j in setvars_or_boolvars[i] <=> edge (i, j) in graphvar.
        - if `setvars_or_boolvars` is a matrix of BoolVars: setvars_or_boolvars[i][j] = 1 <=> edge (i,j) in graphvar.

        :param graphvar: An UndirectedGraphVar.
        :param setvars_or_boolvars: A list of SetVars, or a matrix of BoolVars.
        :return: A graph_neighbors_channeling constraint.
        """
        self._assert_undirected(graphvar, "graph_neighbors_channeling")
        assert len(setvars_or_boolvars) > 0
        if isinstance(setvars_or_boolvars[0], SetVar):
            assert len(setvars_or_boolvars) == graphvar.get_nb_max_nodes(), \
                "[graph_neighbors_channeling] The number of set variables must be equal to" \
                " the maximum number of nodes in the graphvar"
            sets_handle = make_setvar_array(setvars_or_boolvars)
            handle = backend.graph_neighbors_channeling_sets(self._handle, graphvar._handle, sets_handle)
        else:
            assert len(setvars_or_boolvars[0]) > 0 and isinstance(setvars_or_boolvars[0][0], BoolVar)
            assert len(setvars_or_boolvars) == graphvar.get_nb_max_nodes(), \
                "[graph_neighbors_channeling] The number of rows in the boolvar matrix must be equal to" \
                " the maximum number of nodes in the graphvar"
            for b in setvars_or_boolvars:
                assert len(b) == graphvar.get_nb_max_nodes(), \
                    "[graph_neighbors_channeling] The number of columns in the boolvar matrix must be equal to" \
                    " the maximum number of nodes in the graphvar"
            bools_handle = make_boolvar_2d_array(setvars_or_boolvars)
            handle = backend.graph_neighbors_channeling_bools(self._handle, graphvar._handle, bools_handle)
        return Constraint(handle, self)

    def graph_node_neighbors_channeling(self, graphvar: UndirectedGraphVar,
                                        setvar_or_boolvars: Union[SetVar, List[BoolVar]], node: int):
        """
        Channeling constraint:
        - if `setvar_or_boolvars` is a SetVar: int j in setvar_or_boolvars <=> edge (node, j) in graphvar.
        - if `setvar_or_boolvars` is a list of BoolVars: setvar_or_boolvars[j] = 1 <=> edge (node, j) in graphvar.

        :param graphvar: An UndirectedGraphVar.
        :param setvar_or_boolvars: A SetVar of a list of BoolVars.
        :param node: An int.
        :return: A graph_node_neighbors_channeling constraint.
        """
        self._assert_undirected(graphvar, "graph_node_neighbors_channeling")
        if isinstance(setvar_or_boolvars, SetVar):
            handle = backend.graph_neighbors_channeling_node_set(self._handle, graphvar._handle,
                                                                 setvar_or_boolvars._handle, node)
        else:
            assert len(setvar_or_boolvars) == graphvar.get_nb_max_nodes(), \
                "[graph_neighbors_channeling] The number of boolvars must be equal to" \
                " the maximum number of nodes in the graphvar"
            bools_handle = make_boolvar_array(setvar_or_boolvars)
            handle = backend.graph_neighbors_channeling_node_bools(self._handle, graphvar._handle, bools_handle, node)
        return Constraint(handle, self)

    def graph_successors_channeling(self, digraphvar: DirectedGraphVar,
                                    setvars_or_boolvars: Union[List[SetVar], List[List[BoolVar]]]):
        """
        Channeling constraint:
        - if `setvars_or_boolvars` is a list of SetVars: int j in setvars_or_boolvars[i] <=> edge (i, j) in digraphvar.
        - if `setvars_or_boolvars` is a matrix of BoolVars: setvars_or_boolvars[i][j] = 1 <=> edge (i,j) in digraphvar.

        :param digraphvar: An DirectedGraphVar.
        :param setvars_or_boolvars: A list of SetVars, or a matrix of BoolVars.
        :return: A graph_successors_channeling constraint.
        """
        self._assert_directed(digraphvar, "graph_successors_channeling")
        assert len(setvars_or_boolvars) > 0
        if isinstance(setvars_or_boolvars[0], SetVar):
            sets_handle = make_setvar_array(setvars_or_boolvars)
            handle = backend.graph_successors_channeling_sets(self._handle, digraphvar._handle, sets_handle)
        else:
            assert len(setvars_or_boolvars[0]) > 0 and isinstance(setvars_or_boolvars[0][0], BoolVar)
            bools_handle = make_boolvar_2d_array(setvars_or_boolvars)
            handle = backend.graph_successors_channeling_bools(self._handle, digraphvar._handle, bools_handle)
        return Constraint(handle, self)

    def graph_node_successors_channeling(self, digraphvar: DirectedGraphVar,
                                         setvar_or_boolvars: Union[SetVar, List[BoolVar]], node: int):
        """
        Channeling constraint:
        - if `setvar_or_boolvars` is a SetVar: int j in setvar_or_boolvars <=> edge (node, j) in digraphvar.
        - if `setvar_or_boolvars` is a list of BoolVars: setvar_or_boolvars[j] = 1 <=> edge (node, j) in digraphvar.

        :param digraphvar: An DirectedGraphVar.
        :param setvar_or_boolvars: A SetVar of a list of BoolVars.
        :param node: An int.
        :return: A graph_node_successors_channeling constraint.
        """
        self._assert_directed(digraphvar, "graph_node_successors_channeling")
        if isinstance(setvar_or_boolvars, SetVar):
            handle = backend.graph_successors_channeling_node_set(self._handle, digraphvar._handle,
                                                                  setvar_or_boolvars._handle, node)
        else:
            assert len(setvar_or_boolvars) == digraphvar.get_nb_max_nodes(), \
                "[graph_neighbors_channeling] The number of boolvars must be equal to" \
                " the maximum number of nodes in the graphvar"
            bools_handle = make_boolvar_array(setvar_or_boolvars)
            handle = backend.graph_successors_channeling_node_bools(self._handle, digraphvar._handle, bools_handle, node)
        return Constraint(handle, self)

    def graph_node_predecessors_channeling(self, digraphvar: DirectedGraphVar,
                                           setvar_or_boolvars: Union[SetVar, List[BoolVar]], node: int):
        """
        Channeling constraint:
        - if `setvar_or_boolvars` is a SetVar: int j in setvar_or_boolvars <=> edge (j, node) in digraphvar.
        - if `setvar_or_boolvars` is a list of BoolVars: setvar_or_boolvars[j] = 1 <=> edge (j, node) in digraphvar.

        :param digraphvar: An DirectedGraphVar.
        :param setvar_or_boolvars: A SetVar of a list of BoolVars.
        :param node: An int.
        :return: A graph_node_predecessors_channeling constraint.
        """
        self._assert_directed(digraphvar, "graph_node_predecessors_channeling")
        if isinstance(setvar_or_boolvars, SetVar):
            handle = backend.graph_predecessors_channeling_node_set(self._handle, digraphvar._handle,
                                                                    setvar_or_boolvars._handle, node)
        else:
            assert len(setvar_or_boolvars) == digraphvar.get_nb_max_nodes(), \
                "[graph_neighbors_channeling] The number of boolvars must be equal to" \
                " the maximum number of nodes in the graphvar"
            bools_handle = make_boolvar_array(setvar_or_boolvars)
            handle = backend.graph_predecessors_channeling_node_bools(self._handle, digraphvar._handle, bools_handle,
                                                                      node)
        return Constraint(handle, self)

    def graph_min_degree(self, graphvar: UndirectedGraphVar, min_degree: int):
        """
        Minimum degree constraint: for any vertex i in graphvar, | (i, j) | >= min_degree
        This constraint only holds on vertices that are mandatory.

        :param graphvar: An UndirectedGraphVar.
        :param min_degree:  An int.
        :return: A graph_min_degree constraint.
        """
        self._assert_undirected(graphvar, "graph_min_degree")
        handle = backend.graph_min_degree(self._handle, graphvar._handle, min_degree)
        return Constraint(handle, self)

    def graph_min_degrees(self, graphvar: UndirectedGraphVar, min_degrees: List[int]):
        """
        Minimum degree constraint: for any vertex i in graphvar, | (i, j) | >= min_degrees[i]
        This constraint only holds on vertices that are mandatory.

        :param graphvar: An UndirectedGraphVar.
        :param min_degrees:  A list of int.
        :return: A graph_min_degrees constraint.
        """
        self._assert_undirected(graphvar, "graph_min_degrees")
        degrees_handle = make_int_array(min_degrees)
        handle = backend.graph_min_degrees(self._handle, graphvar._handle, degrees_handle)
        return Constraint(handle, self)

    def graph_max_degree(self, graphvar: UndirectedGraphVar, max_degree: int):
        """
        Maximum degree constraint: for any vertex i in graphvar, | (i, j) | <= max_degree
        This constraint only holds on vertices that are mandatory.

        :param graphvar: An UndirectedGraphVar.
        :param max_degree:  An int.
        :return: A graph_max_degree constraint.
        """
        self._assert_undirected(graphvar, "graph_max_degree")
        handle = backend.graph_max_degree(self._handle, graphvar._handle, max_degree)
        return Constraint(handle, self)

    def graph_max_degrees(self, graphvar: UndirectedGraphVar, max_degrees: List[int]):
        """
        Maximum degree constraint: for any vertex i in graphvar, | (i, j) | <= max_degrees[i]
        This constraint only holds on vertices that are mandatory.

        :param graphvar: An UndirectedGraphVar.
        :param max_degrees:  A list of int.
        :return: A graph_max_degrees constraint.
        """
        self._assert_undirected(graphvar, "graph_max_degrees")
        degrees_handle = make_int_array(max_degrees)
        handle = backend.graph_max_degrees(self._handle, graphvar._handle, degrees_handle)
        return Constraint(handle, self)

    def graph_degrees(self, graphvar: UndirectedGraphVar, degrees: List[IntVar]):
        """
        Graph degree constraint: for any vertex i in graphvar, | (i, j) | = degrees[i]
        This constraint only holds on vertices that are mandatory.

        :param graphvar: An UndirectedGraphVar.
        :param degrees:  A list of IntVars.
        :return: A graph_degrees constraint.
        """
        self._assert_undirected(graphvar, "graph_degrees")
        degrees_handle = make_intvar_array(degrees)
        handle = backend.graph_degrees(self._handle, graphvar._handle, degrees_handle)
        return Constraint(handle, self)

    def graph_min_in_degree(self, digraphvar: DirectedGraphVar, min_in_degree: int):
        """
        Minimum inner degree constraint: for any vertex i in digraphvar, | (i, j) | >= min_in_degree
        This constraint only holds on vertices that are mandatory.

        :param digraphvar: An DirectedGraphVar.
        :param min_in_degree:  An int.
        :return: A graph_min_in_degree constraint.
        """
        self._assert_directed(digraphvar, "graph_min_in_degree")
        handle = backend.graph_min_in_degree(self._handle, digraphvar._handle, min_in_degree)
        return Constraint(handle, self)

    def graph_min_in_degrees(self, digraphvar: DirectedGraphVar, min_in_degrees: List[int]):
        """
        Minimum inner degree constraint: for any vertex i in graphvar, | (i, j) | >= min_in_degrees[i]
        This constraint only holds on vertices that are mandatory.

        :param digraphvar: An DirectedGraphVar.
        :param min_in_degrees:  A list of int.
        :return: A graph_min_in_degrees constraint.
        """
        self._assert_directed(digraphvar, "graph_min_in_degrees")
        degrees_handle = make_int_array(min_in_degrees)
        handle = backend.graph_min_in_degrees(self._handle, digraphvar._handle, degrees_handle)
        return Constraint(handle, self)

    def graph_max_in_degree(self, digraphvar: DirectedGraphVar, max_in_degree: int):
        """
        Maximum inner degree constraint: for any vertex i in digraphvar, | (i, j) | <= max_in_degree
        This constraint only holds on vertices that are mandatory.

        :param digraphvar: An DirectedGraphVar.
        :param max_in_degree:  An int.
        :return: A graph_max_in_degree constraint.
        """
        self._assert_directed(digraphvar, "graph_max_in_degree")
        handle = backend.graph_max_in_degree(self._handle, digraphvar._handle, max_in_degree)
        return Constraint(handle, self)

    def graph_max_in_degrees(self, digraphvar: DirectedGraphVar, max_in_degrees: List[int]):
        """
        Maximum inner degree constraint: for any vertex i in graphvar, | (i, j) | <= max_in_degrees[i]
        This constraint only holds on vertices that are mandatory.

        :param digraphvar: An DirectedGraphVar.
        :param max_in_degrees:  A list of int.
        :return: A graph_max_in_degrees constraint.
        """
        self._assert_directed(digraphvar, "graph_max_in_degrees")
        degrees_handle = make_int_array(max_in_degrees)
        handle = backend.graph_max_in_degrees(self._handle, digraphvar._handle, degrees_handle)
        return Constraint(handle, self)

    def graph_in_degrees(self, digraphvar: DirectedGraphVar, in_degrees: List[IntVar]):
        """
        Graph inner degree constraint: for any vertex i in graphvar, | (i, j) | = in_degrees[i]
        This constraint only holds on vertices that are mandatory.

        :param digraphvar: An DirectedGraphVar.
        :param in_degrees:  A list of IntVars.
        :return: A graph_in_degrees constraint.
        """
        self._assert_directed(digraphvar, "graph_in_degrees")
        degrees_handle = make_intvar_array(in_degrees)
        handle = backend.graph_in_degrees(self._handle, digraphvar._handle, degrees_handle)
        return Constraint(handle, self)

    def graph_min_out_degree(self, digraphvar: DirectedGraphVar, min_out_degree: int):
        """
        Minimum outer degree constraint: for any vertex i in digraphvar, | (i, j) | >= min_out_degree
        This constraint only holds on vertices that are mandatory.

        :param digraphvar: An DirectedGraphVar.
        :param min_out_degree:  An int.
        :return: A graph_min_out_degree constraint.
        """
        self._assert_directed(digraphvar, "graph_min_out_degree")
        handle = backend.graph_min_out_degree(self._handle, digraphvar._handle, min_out_degree)
        return Constraint(handle, self)

    def graph_min_out_degrees(self, digraphvar: DirectedGraphVar, min_out_degrees: List[int]):
        """
        Minimum outer degree constraint: for any vertex i in graphvar, | (i, j) | >= min_out_degrees[i]
        This constraint only holds on vertices that are mandatory.

        :param digraphvar: An DirectedGraphVar.
        :param min_out_degrees:  A list of int.
        :return: A graph_min_out_degrees constraint.
        """
        self._assert_directed(digraphvar, "graph_min_out_degrees")
        degrees_handle = make_int_array(min_out_degrees)
        handle = backend.graph_min_out_degrees(self._handle, digraphvar._handle, degrees_handle)
        return Constraint(handle, self)

    def graph_max_out_degree(self, digraphvar: DirectedGraphVar, max_out_degree: int):
        """
        Maximum outer degree constraint: for any vertex i in digraphvar, | (i, j) | <= max_out_degree
        This constraint only holds on vertices that are mandatory.

        :param digraphvar: An DirectedGraphVar.
        :param max_out_degree:  An int.
        :return: A graph_max_out_degree constraint.
        """
        self._assert_directed(digraphvar, "graph_max_in_degree")
        handle = backend.graph_max_out_degree(self._handle, digraphvar._handle, max_out_degree)
        return Constraint(handle, self)

    def graph_max_out_degrees(self, digraphvar: DirectedGraphVar, max_out_degrees: List[int]):
        """
        Maximum outer degree constraint: for any vertex i in graphvar, | (i, j) | <= max_out_degrees[i]
        This constraint only holds on vertices that are mandatory.

        :param digraphvar: An DirectedGraphVar.
        :param max_out_degrees:  A list of int.
        :return: A graph_max_out_degrees constraint.
        """
        self._assert_directed(digraphvar, "graph_max_out_degrees")
        degrees_handle = make_int_array(max_out_degrees)
        handle = backend.graph_max_out_degrees(self._handle, digraphvar._handle, degrees_handle)
        return Constraint(handle, self)

    def graph_out_degrees(self, digraphvar: DirectedGraphVar, out_degrees: List[IntVar]):
        """
        Graph outer degree constraint: for any vertex i in graphvar, | (i, j) | = out_degrees[i]
        This constraint only holds on vertices that are mandatory.

        :param digraphvar: An DirectedGraphVar.
        :param out_degrees:  A list of IntVars.
        :return: A graph_out_degrees constraint.
        """
        self._assert_directed(digraphvar, "graph_out_degree")
        degrees_handle = make_intvar_array(out_degrees)
        handle = backend.graph_out_degrees(self._handle, digraphvar._handle, degrees_handle)
        return Constraint(handle, self)

    def graph_cycle(self, graphvar: UndirectedGraphVar):
        """
        graphvar must form a cycle. Empty graph is accepted.

        :param graphvar: An UndirectedGraphVar.
        :return: A graph_cycle constraint.
        """
        self._assert_undirected(graphvar, "graph_cycle")
        handle = backend.graph_cycle(self._handle, graphvar._handle)
        return Constraint(handle, self)

    def graph_no_cycle(self, graphvar: UndirectedGraphVar):
        """
        Cycle elimination constraint. Prevent the graph from containing cycles.
        e.g. an edge set of the form { (i1, i2), (i2, i3), (i3, i1) }.

        :param graphvar: An UndirectedGraphVar.
        :return: A graph_cycle constraint.
        """
        self._assert_undirected(graphvar, "graph_no_cycle")
        handle = backend.graph_no_cycle(self._handle, graphvar._handle)
        return Constraint(handle, self)

    def graph_no_circuit(self, digraphvar: DirectedGraphVar):
        """
        Circuit elimination constraint. Prevent the graph from containing circuits.
        e.g. an edge set of the form { (i1, i2), (i2, i3), (i3, i1) }.

        :param digraphvar: A DirectedGaphVar.
        :return: A graph_no_circuit constraint.
        """
        self._assert_directed(digraphvar, "graph_no_circuit")
        handle = backend.graph_no_circuit(self._handle, digraphvar._handle)
        return Constraint(handle, self)

    def graph_connected(self, graphvar: UndirectedGraphVar):
        """
        Creates a connectedness constraint which ensures that graphvar is connected.

        BEWARE : empty graphs or graph with 1 node are allowed (they are not disconnected...)
        if one wants a graph with >= 2 nodes he should use the node number constraint (nbNodes)
        connected only focuses on the graph structure to prevent two nodes not to be connected
        if there is 0 or only 1 node, the constraint is therefore not violated.

        The purpose of CP is to compose existing constraints, and nbNodes already exists

        :param graphvar: An UndirectedGraphVar.
        :return: A graph_connected_constraint.
        """
        self._assert_undirected(graphvar, "graph_connected")
        handle = backend.graph_connected(self._handle, graphvar._handle)
        return Constraint(handle, self)

    def graph_biconnected(self, graphvar: UndirectedGraphVar):
        """
        Creates a connectedness constraint which ensures that graphvar is biconnected.
        Beware : should be used in addition to connected.
        The empty graph is not considered biconnected.

        :param graphvar: An UndirectedGraphVar.
        :return: A graph_biconnected constraint.
        """
        self._assert_undirected(graphvar, "graph_biconnected")
        handle = backend.graph_biconnected(self._handle, graphvar._handle)
        return Constraint(handle, self)

    def graph_nb_connected_components(self, graphvar: UndirectedGraphVar, nb_cc: IntVar):
        """
        Creates a connectedness constraint which ensures that graphvar has nb_cc connected components.

        :param graphvar: An UndirectedGraphVar.
        :param nb_cc: An IntVar.
        :return: A graph_nc_connected_components constraints.
        """
        self._assert_undirected(graphvar, "graph_nb_connected components")
        handle = backend.graph_nb_connected_components(self._handle, graphvar._handle, nb_cc._handle)
        return Constraint(handle, self)

    def graph_size_connected_components(self, graphvar: UndirectedGraphVar, min_size: IntVar, max_size: IntVar):
        """
        Creates a constraint which ensures that every connected component of graphvar has a number of nodes bounded by
        min_size and max_size.

        :param graphvar: An UndirectedGraphVar.
        :param min_size: An IntVar.
        :param max_size: An IntVar.
        :return: A graph_size_connected_components constraint.
        """
        self._assert_undirected(graphvar, "graph_size_connected_components")
        handle = backend.graph_size_connected_components(self._handle, graphvar._handle, min_size._handle, max_size._handle)
        return Constraint(handle, self)

    def graph_size_min_connected_components(self, graphvar: UndirectedGraphVar, min_size: IntVar):
        """
        Creates a constraint which ensures that every connected component of graphvar has a minimum number of
        nodes equal to min_size.

        :param graphvar: An UndirectedGraphVar.
        :param min_size: An IntVar.
        :return: A graph_size_min_connected_components constraint.
        """
        self._assert_undirected(graphvar, "graph_size_min_connected_components")
        handle = backend.graph_size_min_connected_components(self._handle, graphvar._handle, min_size._handle)
        return Constraint(handle, self)

    def graph_size_max_connected_components(self, graphvar: UndirectedGraphVar, max_size: IntVar):
        """
        Creates a constraint which ensures that every connected component of graphvar has a maximum number of
        nodes equal to max_size.

        :param graphvar: An UndirectedGraphVar.
        :param max_size: An IntVar.
        :return: A graph_size_max_connected_components constraint.
        """
        self._assert_undirected(graphvar, "graph_size_max_connected_components")
        handle = backend.graph_size_max_connected_components(self._handle, graphvar._handle, max_size._handle)
        return Constraint(handle, self)

    def graph_strongly_connected(self, digraphvar: DirectedGraphVar):
        """
        Creates a strong connectedness constraint which ensures that digraphvar has exactly one strongly
        connected component.

        :param digraphvar: A DirectedGraphVar.
        :return: A graph_strongly_connected constraint.
        """
        self._assert_directed(digraphvar, "graph_strongly_connected")
        handle = backend.graph_strongly_connected(self._handle, digraphvar._handle)
        return Constraint(handle, self)

    def graph_nb_strongly_connected_components(self, digraphvar: DirectedGraphVar, nb_scc: IntVar):
        """
        Creates a strong connectedness constraint which ensures that digraphvar has nb_scc strongly
        connected components.

        :param digraphvar: A DirectedGraphVar.
        :param nb_scc: An IntVar.
        :return: A graph_nb_strongly_connected_components constraint.
        """
        self._assert_directed(digraphvar, "graph_nb_strongly_connected_components")
        handle = backend.graph_nb_strongly_connected_components(self._handle, digraphvar._handle, nb_scc._handle)
        return Constraint(handle, self)

    def graph_tree(self, graphvar: UndirectedGraphVar):
        """
        Creates a tree constraint : graphvar is connected and has no cycle.

        :param graphvar: An UndirectedGraphVar.
        :return: A graph_tree constraint.
        """
        self._assert_undirected(graphvar, "graph_tree")
        handle = backend.graph_tree(self._handle, graphvar._handle)
        return Constraint(handle, self)

    def graph_forest(self, graphvar: UndirectedGraphVar):
        """
        Creates a forest constraint : graphvar has no cycle but may have several connected components.

        :param graphvar: An UndirectedGraphVar.
        :return: A graph_forest constraint.
        """
        self._assert_undirected(graphvar, "graph_forest")
        handle = backend.graph_forest(self._handle, graphvar._handle)
        return Constraint(handle, self)

    def graph_directed_tree(self, digraphvar: DirectedGraphVar, root: int):
        """
        Creates a directed tree constraint : digraphvar forms an arborescence rooted in vertex 'root',
        i.e. digraphvar has no circuit and a path exists from the root to every node.

        :param digraphvar: A DirectedGraphVar.
        :param root: An int.
        :return: A graph_directed_tree constraint.
        """
        self._assert_directed(digraphvar, "graph_directed_tree")
        handle = backend.graph_directed_tree(self._handle, digraphvar._handle, root)
        return Constraint(handle, self)

    def graph_directed_forest(self, digraphvar: DirectedGraphVar):
        """
        Creates a directed forest constraint: digraphvar form is composed of several disjoint
        (potentially singleton) arborescences.

        :param digraphvar: A DirectedGraphVar.
        :return: A graph_directed_forest constraint.
        """
        self._assert_directed(digraphvar, "graph_directed_forest")
        handle = backend.graph_directed_forest(self._handle, digraphvar._handle)
        return Constraint(handle, self)

    def graph_reachability(self, digraphvar: DirectedGraphVar, root: int):
        """
        Creates a constraint which ensures that every vertex in digraphvar is reachable by a simple path from the root.

        :param digraphvar: A DirectedGraphVar.
        :param root: An int.
        :return: A graph_reachability constraint.
        """
        self._assert_directed(digraphvar, "graph_reachability")
        handle = backend.graph_reachability(self._handle, digraphvar._handle, root)
        return Constraint(handle, self)

    def graph_nb_cliques(self, graphvar: UndirectedGraphVar, nb_cliques: IntVar):
        """
        Partition a graph variable into `nb_cliques` cliques.

        :param graphvar: An UndirectedGraphVar.
        :param nb_cliques: An IntVar.
        :return: A graph_nb_cliques constraint.
        """
        self._assert_undirected(graphvar, "graph_nb_cliques")
        handle = backend.graph_nb_cliques(self._handle, graphvar._handle, nb_cliques._handle)
        return Constraint(handle, self)

    def graph_diameter(self, graphvar: UndirectedGraphVar, diameter: IntVar):
        """
        Creates a constraint which states that diameter is the diameter of graphvar,
        i.e. diameter is the length (number of edges) of the largest shortest path among any pair of nodes.
        This constraint implies that graphvar is connected.

        :param graphvar: An UndirectedGraphVar.
        :param diameter: An IntVar.
        :return: A graph_diameter constraint.
        """
        self._assert_undirected(graphvar, "graph_diameter")
        handle = backend.graph_diameter(self._handle, graphvar._handle, diameter._handle)
        return Constraint(handle, self)
