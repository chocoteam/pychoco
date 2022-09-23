from pychoco.variables.graphvar import GraphVar


class DirectedGraphVar(GraphVar):
    """
    A Directed Graph Variable is defined by a domain which is a graph interval [LB, UB].
    An instantiation of a directed graph variable is a directed graph composed of nodes and edges.
    LB is the kernel graph (or lower bound), that must be a subgraph of any instantiation.
    UB is the envelope graph (or upper bound), such that any instantiation is a subgraph of it.
    """

    def __init__(self, handle, model: "Model", lb: "DirectedGraph", ub: "DirectedGraph"):
        self._lb = lb
        self._ub = ub
        super().__init__(handle, model, lb, ub)

    def is_directed(self):
        return True

    def get_lb(self):
        """
        :return: The lower bound of this directed graph variable (a DirectedGraph).
        """
        return self._lb

    def get_ub(self):
        """
        :return: The upper bound of this directed graph variable (a DirectedGraph).
        """
        return self._ub

    def get_value(self):
        """
        :return: The value of this variable, if it is instantiated.
        """
        assert self.is_instantiated(), "{} is not instantiated".format(self.name)
        return self._lb

    def get_type(self):
        return "DirectedGraphVar"
