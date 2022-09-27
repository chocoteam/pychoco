from abc import ABC, abstractmethod
from typing import Union, List

from pychoco import backend
from pychoco._utils import make_int_array
from pychoco.objects.graphs.directed_graph import DirectedGraph
from pychoco.objects.graphs.undirected_graph import UndirectedGraph
from pychoco.variables.boolvar import BoolVar
from pychoco.variables.directed_graphvar import DirectedGraphVar
from pychoco.variables.intvar import IntVar
from pychoco.variables.setvar import SetVar
from pychoco.variables.task import Task
from pychoco.variables.undirected_graphvar import UndirectedGraphVar


class VariableFactory(ABC):
    """
    Factory for creating variables.
    """

    @property
    @abstractmethod
    def handle(self):
        pass

    # Integer variables #

    def intvar(self, lb: int, ub: Union[int, None] = None, name: Union[str, None] = None):
        """
        Creates an intvar.

        :param lb: Lower bound (integer).
        :param ub: upper bound (integer). If None: the variable is a constant equals to lb.
        :param name: The name of the intvar (automatically given if None).
        :return: An intvar.
        """
        if name is None:
            if ub is None:
                var_handle = backend.intvar_i(self.handle, lb)
            else:
                var_handle = backend.intvar_ii(self.handle, lb, ub)
        else:
            if ub is None:
                var_handle = backend.intvar_si(self.handle, name, lb)
            else:
                var_handle = backend.intvar_sii(self.handle, name, lb, ub)
        return IntVar(var_handle, self)

    def intvars(self, size: int, lb: Union[List[int], int], ub: Union[int, None] = None, name: Union[str, None] = None):
        """
        Creates a list of intvars.

        :param size: Number of intvars.
        :param lb: Lower bound (integer). If lb is a list of ints, constant variables are created.
        :param ub: upper bound (integer). If None: the variable is a constant equals to lb.
        :param name: Prefix name of the intvars (automatically given if None).
        :return: A list of intvars.
        """
        if isinstance(lb, list):
            assert len(lb) == size
            return [self.intvar(lb[i], None, name) for i in range(0, size)]
        else:
            return [self.intvar(lb, ub, name) for i in range(0, size)]

    # Boolean variables #

    def boolvar(self, value: Union[bool, None] = None, name: Union[str, None] = None):
        """
        Creates a boolvar.

        :param value: If not None, a fixed value for the variable (which is thus a constant).
        :param name: The name of the variable (optional).
        :return: A boolvar.
        """
        if name is not None:
            if value is not None:
                var_handle = backend.boolvar_sb(self.handle, name, value)
            else:
                var_handle = backend.boolvar_s(self.handle, name)
        else:
            if value is not None:
                var_handle = backend.boolvar_b(self.handle, value)
            else:
                var_handle = backend.boolvar(self.handle)
        return BoolVar(var_handle, self)

    def boolvars(self, size: int, value: Union[List[bool], bool, None] = None, name: Union[str, None] = None):
        """
        Creates a list of boolvars.

        :param size: Number of boolvars.
        :param value: If not None, a fixed value for the variables (which is thus a constant). This value is either
            the same for all variables (bool), or given as a list of bools.
        :param name: The name of the variable (optional).
        :return: A list of boolvars.
        """
        if isinstance(value, list):
            assert len(value) == size
            return [self.boolvar(value[i], name) for i in range(0, size)]
        else:
            return [self.boolvar(value, name) for i in range(0, size)]

    # Task variables #

    def task(self, start: IntVar, duration: Union[int, IntVar], end: Union[None, IntVar] = None):
        """
        Creates a task container, based on a starting time `start`, a duration `duration`, and
        optionally an ending time `end`, such that: `start` + `duration` = `end`.

        A call to ensure_bound_consistency() is required before launching the resolution,
        this will not be done automatically.

        :param start: The starting time (IntVar).
        :param duration: The duration (int or IntVar).
        :param end: The ending time (IntVar, or None).
        :return: A task container.
        """
        return Task(self, start, duration, end)

    # Set variables

    def setvar(self, lb_or_value: Union[set, list], ub: Union[set, list, None] = None, name: Union[str, None] = None):
        """
        Creates a set variable taking its domain in [lb, ub], or a a constant setvar if ub is None.
        For instance [{0,3},{-2,0,2,3}] means the variable must include both 0 and 3 and can additionally include -2
        and 2.

        :param lb_or_value: Initial domain lower bound (contains mandatory elements that should be present in
            every solution). If ub is None, corresponds to the constant value of this variable.
        :param ub: Initial domain upper bound (contains potential elements)
        :param name: Name of the variable (optional).
        :return: A SetVar.
        """
        lb_handle = make_int_array(list(lb_or_value))
        if ub is None:
            if name is None:
                handle = backend.setvar_iv(self.handle, lb_handle)
            else:
                handle = backend.setvar_s_iv(self.handle, name, lb_handle)
        else:
            ub_handle = make_int_array(list(ub))
            if name is None:
                handle = backend.setvar_iviv(self.handle, lb_handle, ub_handle)
            else:
                handle = backend.setvar_s_iviv(self.handle, lb_handle, ub_handle)
        return SetVar(handle, self)

    # Graph variables

    def graphvar(self, lb: "UndirectedGraph", ub: "UndirectedGraph", name: str):
        """
        Creates an undirected graph variable, taking its values in the graph domain [LB, UB].
        An instantiation of a graph variable is a graph composed of nodes and edges.
        lb is the kernel graph (or lower bound), that must be a subgraph of any instantiation.
        ub is the envelope graph (or upper bound), such that any instantiation is a subgraph of it.

        :param lb: Lower bound of the graphvar (or kernel), an UndirectedGraph.
        :param ub: Upper bound of the graphvar (or envelope), an UndirectedGraph.
        :param name: Name of the graphvar.
        :return: An undirected graph variable taking its values in the graph domain [lb, ub].
        """
        assert isinstance(lb, UndirectedGraph) and isinstance(ub, UndirectedGraph), \
            "[graphvar] Bounds must be Undirected graph."
        handle = backend.create_graphvar(self.handle, name, lb.handle, ub.handle)
        return UndirectedGraphVar(handle, self, lb, ub)

    def node_induced_graphvar(self, lb: "UndirectedGraphVar", ub: "UndirectedGraphVar", name: str):
        """
        Creates a node-induced undirected graph variable guaranteeing that any instantiation is a node-induced subgraph
        of the envelope used to construct the graph variable. Any two nodes that are connected in the envelope
        are connected by an edge in any instantiation containing these two nodes. More formally:
        - G = (V, E) in [G_lb, G_ub], with G_ub = (V_ub, E_ub);
        - E = { (x, y) in E_ub | x in V and y in V }.

        :param lb: Lower bound of the graphvar (or kernel), an UndirectedGraph.
        :param ub: Upper bound of the graphvar (or envelope), an UndirectedGraph.
        :param name: Name of the graphvar.
        :return: An UndirectedGraphVar taking its values in the graph domain [lb, ub] and such that any value is
            a node-induced subgraph of UB.
        """
        assert isinstance(lb, UndirectedGraph) and isinstance(ub, UndirectedGraph), \
            "[graphvar] Bounds must be Undirected graph."
        handle = backend.create_node_induced_graphvar(self.handle, name, lb.handle, ub.handle)
        return UndirectedGraphVar(handle, self, lb, ub)

    def digraphvar(self, lb: "DirectedGraph", ub: "DirectedGraph", name: str):
        """
        Creates a directed graph variable, taking its values in the graph domain [lb, ub].
        An instantiation of a graph variable is a graph composed of nodes and edges.
        lb is the kernel graph (or lower bound), that must be a subgraph of any instantiation.
        ub is the envelope graph (or upper bound), such that any instantiation is a subgraph of it.

        :param lb: Lower bound of the digraphvar (or kernel), a DirectedGraph.
        :param ub: Upper bound of the digraphvar (or Envelope), a DirectedGraph.
        :param name: The name of the digraphvar.
        :return: A DirectedGraphVariable.
        """
        assert isinstance(lb, DirectedGraph) and isinstance(ub, DirectedGraph), \
            "[digraphvar] Bounds must be Directed graph."
        handle = backend.create_digraphvar(self.handle, name, lb.handle, ub.handle)
        return DirectedGraphVar(handle, self, lb, ub)

    def node_induced_digraphvar(self, lb: "DirectedGraphVar", ub: "DirectedGraphVar", name: str):
        """
        Creates a node-induced directed graph variable guaranteeing that any instantiation is a node-induced subgraph
        of the envelope used to construct the graph variable. Any two nodes that are connected in the envelope
        are connected by an edge in any instantiation containing these two nodes. More formally:
        - G = (V, E) in [G_lb, G_ub], with G_ub = (V_ub, E_ub);
        - E = { (x, y) in E_ub | x in V and y in V }.

        :param lb: Lower bound of the graphvar (or kernel), a DirectedGraph.
        :param ub: Upper bound of the graphvar (or envelope), a DirectedGraph.
        :param name: Name of the graphvar.
        :return: An DirectedGraphVar taking its values in the graph domain [lb, ub] and such that any value is
            a node-induced subgraph of UB.
        """
        assert isinstance(lb, DirectedGraph) and isinstance(ub, DirectedGraph), \
            "[digraphvar] Bounds must be Directed graph."
        handle = backend.create_node_induced_digraphvar(self.handle, name, lb.handle, ub.handle)
        return DirectedGraphVar(handle, self, lb, ub)
