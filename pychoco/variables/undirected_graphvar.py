from pychoco.variables.graphvar import GraphVar


class UndirectedGraphVar(GraphVar):
    """
    An Undirected Graph Variable is defined by a domain which is a graph interval [LB, UB].
    An instantiation of an undirected graph variable is an undirected graph composed of nodes and edges.
    LB is the kernel graph (or lower bound), that must be a subgraph of any instantiation.
    UB is the envelope graph (or upper bound), such that any instantiation is a subgraph of it.
    """

    def __init__(self, handle, model: "Model", lb: "UndirectedGraph", ub: "UndirectedGraph"):
        self._lb = lb
        self._ub = ub
        super().__init__(handle, model, lb, ub)

    def is_directed(self):
        return False

    def get_lb(self):
        """
        :return: The lower bound of this undirected graph variable (an UndirectedGraph).
        """
        return self._lb

    def get_ub(self):
        """
        :return: The upper bound of this undirected graph variable (an UndirectedGraph).
        """
        return self._ub

    def get_value(self):
        """
        :return: The value of this variable, if it is instantiated.
        """
        assert self.is_instantiated(), "{} is not instantiated".format(self.name)
        return self._lb

    def get_type(self):
        return "UndirectedGraphVar"
