from typing import Any, Optional

from pychoco import backend
from pychoco._handle_wrapper import _HandleWrapper
from pychoco.constraints.graph_constraint_factory import GraphConstraintFactory
from pychoco.constraints.int_constraint_factory import IntConstraintFactory
from pychoco.constraints.sat_factory import SatFactory
from pychoco.constraints.set_constraint_factory import SetConstraintFactory
from pychoco.constraints.reification_factory import ReificationFactory
from pychoco.solver import Solver
from pychoco.variables.variable_factory import VariableFactory
from pychoco.variables.view_factory import ViewFactory


class Model(VariableFactory, ViewFactory, IntConstraintFactory, SetConstraintFactory, GraphConstraintFactory,
            ReificationFactory, SatFactory, _HandleWrapper):
    """
    The Model is the header component of Constraint Programming. It embeds the list of
    Variable (and their Domain), the Constraint's network, and a propagation engine to
    pilot the propagation.
    """

    def __init__(self, name: Optional[str] = None, **kwargs: Any) -> None:
        """
        Choco Model constructor.

        :param name: The name of the model (optional).
        """
        if "_handle" in kwargs:
            super(Model, self).__init__(kwargs["_handle"])
        else:
            if name is not None:
                handle = backend.create_model_s(name)
            else:
                handle = backend.create_model()
            super(Model, self).__init__(handle)

    @property
    def _handle(self):
        return self._handle_

    @property
    def name(self):
        """
        :return: The name of the model.
        """
        return backend.get_model_name(self._handle)

    def get_solver(self) -> Solver:
        """
        :return: The solver associated with this model.
        """
        solver_handler = backend.get_solver(self._handle)
        return Solver(solver_handler, self)

    def set_objective(self, objective: "Variable", maximize: bool = True):
        """
        Define an optimization objective.
        :param objective: The optimization objective.
        :param maximize: if True, maximizes objective, otherwise minimizes it.
        """
        backend.set_objective(self._handle, maximize, objective._handle)

    def __repr__(self):
        return "Choco Model ('" + self.name + "')"
