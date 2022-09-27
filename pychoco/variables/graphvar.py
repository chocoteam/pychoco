from abc import ABC, abstractmethod

from pychoco.variables.variable import Variable


class GraphVar(Variable, ABC):
    """
    A Graph Variable is defined by a domain which is a graph interval [LB, UB].
    An instantiation of a graph variable is a graph composed of nodes and edges (directed or not).
    LB is the kernel graph (or lower bound), that must be a subgraph of any instantiation.
    UB is the envelope graph (or upper bound), such that any instantiation is a subgraph of it.
    """

    def __init__(self, handle, model: "Model", lb: "Graph", ub: "Graph"):
        self._lb = lb
        self._ub = ub
        super().__init__(handle, model)

    @abstractmethod
    def is_directed(self):
        """
        :return: True if the graphvar is directed, False otherwise.
        """
        pass

    @abstractmethod
    def get_lb(self):
        pass

    @abstractmethod
    def get_ub(self):
        pass

    def get_nb_max_nodes(self):
        """
        :return: The maximum number of node the graph variable may have.
        """
        return self.get_ub().get_nb_max_nodes()
