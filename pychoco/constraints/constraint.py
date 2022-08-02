from abc import ABC, abstractmethod


class Constraint(ABC):
    """
    A constraint is a logic formula defining allowed combinations of values for a set of
    variables, i.e., restrictions over variables that must be respected in order to get
    a feasible solution. A constraint is equipped with a (set of) filtering algorithm(s),
    named propagator(s). A propagator removes, from the domains of the target variables,
    values that cannot correspond to a valid combination of values. A solution of a
    problem is a variable-value assignment verifying all the constraints.

    To be effective, a constraint must be either posted or reified.
    """

    @abstractmethod
    def get_name(self):
        """
        :return: The name of the constraint.
        """
        pass

    @abstractmethod
    def post(self):
        """
        :return: Post the constraint.
        """
        pass

    def __repr__(self):
        return "Choco Constraint ('" + self.get_name() + "')"
