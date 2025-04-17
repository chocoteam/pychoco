from abc import abstractmethod

from pychoco import backend
from pychoco._handle_wrapper import _HandleWrapper
from pychoco.utils import ESat
from pychoco.variables.boolvar import BoolVar


class Constraint(_HandleWrapper):
    """
    A constraint is a logic formula defining allowed combinations of values for a set of
    variables, i.e., restrictions over variables that must be respected in order to get
    a feasible solution. A constraint is equipped with a (set of) filtering algorithm(s),
    named propagator(s). A propagator removes, from the domains of the target variables,
    values that cannot correspond to a valid combination of values. A solution of a
    problem is a variable-value assignment verifying all the constraints.

    To be effective, a constraint must be either posted or reified.
    """

    def __init__(self, handle: "SwigPyObject", model: "_Model"):
        """
        Warning: Not intended to be used by users, use a Model object to instantiate constraints instead.
        """
        super().__init__(handle)
        self._model = model

    def get_name(self):
        """
        :return: The name of the constraint.
        """
        return backend.get_constraint_name(self._handle)

    @property
    def model(self):
        """
        :return: The model associated with this constraint.
        """
        return self._model

    @abstractmethod
    def post(self):
        """
        :return: Post the constraint.
        """
        backend.post(self._handle)

    @abstractmethod
    def reify(self):
        """
        Reifies the constraint, i.e. return a boolvar whose instantiation in a solution
        correspond to the satisfaction state of the constraint in this solution.

        :return: A BoolVar.
        """
        var_handle = backend.reify(self._handle)
        return BoolVar(var_handle, self.model)

    @abstractmethod
    def reify_with(self, boolvar):
        """
        Reifies the constraint with a given boolvar whose instantiation in a solution
        correspond to the satisfaction state of the constraint in this solution.
        """
        backend.reify_with(self._handle, boolvar._handle)


    @abstractmethod
    def implies(self, boolvar):
        """
        Encapsulate this constraint in an implication relationship.
        The truth value of this constraints implies the truth value of te boolvar.
        """
        backend.implies(self._handle, boolvar._handle)

    @abstractmethod
    def implied_by(self, boolvar):
        """
        Encapsulate this constraint in an implication relationship.
        Represents half-reification of the constraint.
        """
        backend.implied_by(self._handle, boolvar._handle)

    @abstractmethod
    def is_satisfied(self):
        """
        Check whether the constraint is satisfied (ESat.TRUE), not satisfied (ESat.FALSE),
        or if it is not yet possible to define whether it is satisfied or not (ESat.UNDEFINED).
        **Note:** this method is used internally by Choco, but it can be useful to verify whether
        a constraint is satisfied (or not) regardless of the variables' instantiation.
        :return: The satisfaction state of the constraint.
        """
        state = backend.is_satisfied(self._handle)
        if state == 0:
            return ESat.FALSE
        if state == 1:
            return ESat.TRUE
        return ESat.UNDEFINED

    def __repr__(self):
        return "Choco Constraint ('" + self.get_name() + "')"
