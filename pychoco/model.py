from abc import ABC, abstractmethod

from constraints.set_constraint_factory import SetConstraintFactory
from pychoco.constraints.int_constraint_factory import IntConstraintFactory
from pychoco.variables.variable_factory import VariableFactory


class Model(VariableFactory, IntConstraintFactory, SetConstraintFactory, ABC):
    """
    The Model is the header component of Constraint Programming. It embeds the list of
    Variable (and their Domain), the Constraint's network, and a propagation engine to
    pilot the propagation.
    """

    @property
    @abstractmethod
    def name(self):
        """
        :return: The name of the model.
        """
        pass

    @abstractmethod
    def get_solver(self):
        """
        :return: The solver associated with this model.
        """
        pass

    def __repr__(self):
        return "Choco Model ('" + self.name + "')"
