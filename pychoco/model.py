from typing import Any, Optional

from pychoco import backend
from pychoco._handle_wrapper import _HandleWrapper
from pychoco.constraints.graph_constraint_factory import GraphConstraintFactory
from pychoco.constraints.int_constraint_factory import IntConstraintFactory
from pychoco.constraints.sat_factory import SatFactory
from pychoco.constraints.set_constraint_factory import SetConstraintFactory
from pychoco.constraints.reification_factory import ReificationFactory
from pychoco.settings import Settings
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

    def __init__(self, 
                 name: Optional[str] = None, 
                 lcg: bool = False, 
                 warn_user: bool = False, 
                 check_constraints: bool = True,
                 check_views: bool = True, 
                 check_monitors: bool = True, 
                 max_dom_size_for_enum: int = 1<<16, 
                 min_card_size_for_sum_decomp : int = 50,
                 table_substitution=True,
                 max_tuple_size_for_table_decomp: int = 10000,
                 max_mem_size_for_compect_table: int = 1024,
                 enable_sat: bool = False,
                 swap_prop_on_passive: bool = True,
                 print_undeclared_constraints: bool = False,
                 max_learnt_clauses: int = 100000,
                 **kwargs: Any) -> None:
        """
        Choco Model constructor.

        :param name: The name of the model (optional).
        :param settings: The settings for the model (optional).
        """

        if "_handle" in kwargs:
            super(Model, self).__init__(kwargs["_handle"])
        else:
            settings = Settings()
            settings.set_lcg(lcg)
            settings.set_warn_user(warn_user)
            settings.set_check_declared_constraints(check_constraints)
            settings.set_check_declared_views(check_views)
            settings.set_check_declared_monitors(check_monitors)
            settings.set_max_dom_size_for_enumerated(max_dom_size_for_enum)
            settings.set_min_cardinality_for_sum_decomposition(min_card_size_for_sum_decomp)
            settings.set_enable_table_substitution(table_substitution)
            settings.set_max_tuple_size_for_substitution(max_tuple_size_for_table_decomp)
            settings.set_max_size_in_mb_to_use_compact_table(max_mem_size_for_compect_table)
            settings.set_enable_sat(enable_sat)
            settings.set_swap_on_passivate(swap_prop_on_passive)
            settings.set_print_all_undeclared_constraints(print_undeclared_constraints)
            settings.set_nb_max_learnt_clauses(max_learnt_clauses)

            if name is None:
                name = "Model "+ str(id(self))
            handle = backend.create_model_s_s(name, settings.handle)
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
