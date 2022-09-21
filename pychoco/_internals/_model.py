from typing import Union, List

from pychoco import backend
from pychoco._internals._boolvar import _BoolVar
from pychoco._internals._constraint import _Constraint
from pychoco._internals._cost_automaton import _CostAutomaton
from pychoco._internals._finite_automaton import _FiniteAutomaton
from pychoco._internals._handle_wrapper import _HandleWrapper
from pychoco._internals._intvar import _IntVar
from pychoco._internals._solver import _Solver
from pychoco._internals._task import _Task
from pychoco._internals._utils import make_intvar_2d_array
from pychoco._internals._utils import make_intvar_array, make_int_array, make_boolvar_array, make_constraint_array, \
    make_int_2d_array
from pychoco._internals._utils import make_setvar_array
from pychoco._internals._utils import make_task_array
from pychoco.constraints.constraint import Constraint
from pychoco.model import Model
from pychoco.objects.graphs.multivalued_decision_diagram import MultivaluedDecisionDiagram
from pychoco.variables.boolvar import BoolVar
from pychoco.variables.setvar import SetVar


class _Model(Model, _HandleWrapper):
    """
    Internal class to represent a choco model.
    """

    def __init__(self, handle):
        super().__init__(handle)

    # Model methods implementation

    @property
    def name(self):
        return backend.get_model_name(self.handle)

    def get_solver(self):
        solver_handler = backend.get_solver(self.handle)
        return _Solver(solver_handler, self)

    # VariableFactory methods implementation

    def intvar(self, lb: int, ub: Union[int, None] = None, name: Union[str, None] = None):
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
        return _IntVar(var_handle, self)

    def intvars(self, size: int, lb: int, ub: Union[int, None] = None, name: Union[str, None] = None):
        if isinstance(lb, list):
            assert len(lb) == size
            return [self.intvar(lb[i], None, name) for i in range(0, size)]
        else:
            return [self.intvar(lb, ub, name) for i in range(0, size)]

    def boolvar(self, value: Union[bool, None] = None, name: Union[str, None] = None):
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
        return _BoolVar(var_handle, self)

    def boolvars(self, size: int, value: Union[List[bool], bool, None] = None, name: Union[str, None] = None):
        if isinstance(value, list):
            assert len(value) == size
            return [self.boolvar(value[i], name) for i in range(0, size)]
        else:
            return [self.boolvar(value, name) for i in range(0, size)]

    def task(self, start: _IntVar, duration: Union[int, _IntVar], end: Union[None, _IntVar] = None):
        has_monitor = True
        if end is None:
            if isinstance(duration, _IntVar):
                end_ = self.intvar(start.get_lb() + duration.get_lb(), start.get_ub() + duration.get_ub())
                handle = backend.create_task_iv_iv_iv(start.handle, duration.handle, end_.handle)
            else:
                handle = backend.create_task_iv_i(start.handle, duration)
                has_monitor = False
        else:
            if isinstance(duration, _IntVar):
                handle = backend.create_task_iv_iv_iv(start.handle, duration.handle, end.handle)
            else:
                handle = backend.create_task_iv_i_iv(start.handle, duration, end.handle)
        return _Task(handle, self, has_monitor)

    def setvar(self, lb_or_value: set, ub: Union[set, None] = None, name: Union[str, None] = None):
        return SetVar(self, lb_or_value, ub, name)

    # IntConstraintFactor methods implementation

    def arithm(self, x: _IntVar, op1: str, y: Union[int, _IntVar],
               op2: Union[None, str] = None, z: Union[None, int, _IntVar] = None):
        constraint_handle = None
        eq_operators = ["=", "!=", ">", "<", ">=", "<="]
        alg_operators = ["+", "-", "*", "/"]
        if op2 is None:
            assert op1 in eq_operators
        else:
            assert (op1 in eq_operators and op2 in alg_operators) or (op1 in alg_operators and op2 in eq_operators)
        # Case 1
        if isinstance(y, int) and op2 is None and z is None:
            constraint_handle = backend.arithm_iv_cst(self.handle, x.handle, op1, y)
        if isinstance(y, int) and op2 is not None and z is not None:
            yy = self.intvar(y)
            if isinstance(z, int):
                constraint_handle = backend.arithm_iv_iv_cst(self.handle, x.handle, op1, yy.handle, op2, z)
            else:
                constraint_handle = backend.arithm_iv_iv_iv(self.handle, x.handle, op1, yy.handle, op2, z)
        if isinstance(y, _IntVar) and op2 is None and z is None:
            constraint_handle = backend.arithm_iv_iv(self.handle, x.handle, op1, y.handle)
        if isinstance(y, _IntVar) and op2 is not None and isinstance(z, int):
            constraint_handle = backend.arithm_iv_iv_cst(self.handle, x.handle, op1, y.handle, op2, z)
        if isinstance(y, _IntVar) and op2 is not None and isinstance(z, _IntVar):
            constraint_handle = backend.arithm_iv_iv_iv(self.handle, x.handle, op1, y.handle, op2, z.handle)
        if constraint_handle is None:
            raise AttributeError("Invalid parameters combination for arithm constraint. Please refer to the doc")
        return _Constraint(constraint_handle, self)

    def member(self, x: _IntVar, table: Union[list, tuple, None] = None,
               lb: Union[None, int] = None, ub: Union[None, int] = None):
        if table is not None:
            ints_array = make_int_array(table)
            constraint_handle = backend.member_iv_iarray(self.handle, x.handle, ints_array)
        else:
            constraint_handle = backend.member_iv_i_i(self.handle, x.handle, lb, ub)
        return _Constraint(constraint_handle, self)

    def not_member(self, x: _IntVar, table: Union[list, tuple, None] = None,
                   lb: Union[None, int] = None, ub: Union[None, int] = None):
        if table is not None:
            ints_array = make_int_array(table)
            constraint_handle = backend.not_member_iv_iarray(self.handle, x.handle, ints_array)
        else:
            constraint_handle = backend.not_member_iv_i_i(self.handle, x.handle, lb, ub)
        return _Constraint(constraint_handle, self)

    def mod(self, x, mod: Union[int, _IntVar], res: Union[int, _IntVar]):
        constraint_handle = None
        if isinstance(mod, int) and isinstance(res, int):
            constraint_handle = backend.mod_iv_i_i(self.handle, x.handle, mod, res)
        if isinstance(mod, int) and isinstance(res, _IntVar):
            constraint_handle = backend.mod_iv_i_iv(self.handle, x.handle, mod, res.handle)
        if isinstance(mod, _IntVar) and isinstance(res, _IntVar):
            constraint_handle = backend.mod_iv_iv_iv(self.handle, x.handle, mod.handle, res.handle)
        return _Constraint(constraint_handle, self)

    def not_(self, constraint: _Constraint):
        constraint_handle = backend.not_(self.handle, constraint.handle)
        return _Constraint(constraint_handle, self)

    def absolute(self, x: _IntVar, y: _IntVar):
        constraint_handle = backend.absolute(self.handle, x.handle, y.handle)
        return _Constraint(constraint_handle, self)

    def distance(self, x: _IntVar, y: _IntVar, op: str, z: Union[int, _IntVar]):
        if isinstance(z, _IntVar):
            assert op in {"=", ">", "<"}, "[distance] op must be in ['=', '>', '<']"
        else:
            assert op in {"=", "!=", ">", "<"}, "[distance] op must be in ['=', '!=', '>', '<']"
        if isinstance(z, int):
            constraint_handle = backend.distance_iv_iv_i(self.handle, x.handle, y.handle, op, z)
        else:
            constraint_handle = backend.distance_iv_iv_iv(self.handle, x.handle, y.handle, op, z.handle)
        return _Constraint(constraint_handle, self)

    def element(self, x: _IntVar, table: Union[List[int], List[_IntVar]], index: _IntVar, offset: int = 0):
        if len(table) == 0:
            raise AttributeError("table parameter in element constraint must have a length > 0")
        if isinstance(table[0], int):
            ints_array_handle = make_int_array(table)
            constraint_handle = backend.element_iv_iarray_iv_i(self.handle, x.handle, ints_array_handle,
                                                               index.handle, offset)
        else:
            int_var_array_handle = make_intvar_array(table)
            constraint_handle = backend.element_iv_ivarray_iv_i(self.handle, x.handle, int_var_array_handle,
                                                                index.handle, offset)
        return _Constraint(constraint_handle, self)

    def square(self, x: _IntVar, y: _IntVar):
        constraint_handle = backend.square(self.handle, x.handle, y.handle)
        return _Constraint(constraint_handle, self)

    def table(self, intvars: List[_IntVar], tuples: List[List[int]], feasible: bool = True, algo: str = "GAC3rm"):
        assert algo in ["CT+", "GAC3rm", "GAC2001", "GACSTR", "GAC2001+", "GAC3rm+",
                        "FC", "STR2+"], '[table] algo must be in ["CT+", "GAC3rm", "GAC2001", "GACSTR", "GAC2001+", ' \
                                        '"GAC3rm+", "FC", "STR2+"]'
        vars_handle = make_intvar_array(intvars)
        tuples_handle = make_int_2d_array(tuples)
        constraint_handle = backend.table(self.handle, vars_handle, tuples_handle, feasible, algo)
        return _Constraint(constraint_handle, self)

    def times(self, x: _IntVar, y: Union[int, _IntVar], z: Union[int, _IntVar]):
        constraint_handle = None
        if isinstance(z, _IntVar) and isinstance(y, int):
            constraint_handle = backend.times_iv_i_iv(self.handle, x.handle, y, z.handle)
        if isinstance(y, _IntVar) and isinstance(z, int):
            constraint_handle = backend.times_iv_iv_i(self.handle, x.handle, y.handle, z)
        if isinstance(y, _IntVar) and isinstance(z, _IntVar):
            constraint_handle = backend.times_iv_iv_iv(self.handle, x.handle, y.handle, z.handle)
        return _Constraint(constraint_handle, self)

    def pow(self, x: _IntVar, c: int, y: _IntVar):
        constraint_handle = backend.pow_(self.handle, x.handle, c, y.handle)
        return _Constraint(constraint_handle, self)

    def div(self, dividend: _IntVar, divisor: _IntVar, result: _IntVar):
        constraint_handle = backend.div_(self.handle, dividend.handle, divisor.handle, result.handle)
        return _Constraint(constraint_handle, self)

    def max(self, x: _IntVar, intvars: List[_IntVar]):
        int_var_array_handle = make_intvar_array(intvars)
        constraint_hande = backend.max_iv_ivarray(self.handle, x.handle, int_var_array_handle)
        return _Constraint(constraint_hande, self)

    def mddc(self, intvars: List[_IntVar], mdd: MultivaluedDecisionDiagram):
        intvars_handle = make_intvar_array(intvars)
        constraint_handle = backend.mddc(self.handle, intvars_handle, mdd.handle)
        return _Constraint(constraint_handle, self)

    def min(self, x: _IntVar, intvars: List[_IntVar]):
        int_var_array_handle = make_intvar_array(intvars)
        constraint_hande = backend.min_iv_ivarray(self.handle, x.handle, int_var_array_handle)
        return _Constraint(constraint_hande, self)

    def multi_cost_regular(self, intvars: List[_IntVar], costs: List[_IntVar], cost_automaton: _CostAutomaton):
        intvar_array_handle = make_intvar_array(intvars)
        costs_handle = make_intvar_array(costs)
        constraint_handle = backend.multi_cost_regular(self.handle, intvar_array_handle, costs_handle,
                                                       cost_automaton.handle)
        return _Constraint(constraint_handle, self)

    def all_different(self, intvars: List[_IntVar]):
        vars_array = make_intvar_array(intvars)
        constraint_handle = backend.all_different(self.handle, vars_array)
        return _Constraint(constraint_handle, self)

    def all_different_except_0(self, intvars: List[_IntVar]):
        vars_array = make_intvar_array(intvars)
        constraint_handle = backend.all_different_except_0(self.handle, vars_array)
        return _Constraint(constraint_handle, self)

    def all_different_prec(self, intvars: List[_IntVar], predecessors: List[List[int]], successors: List[List[int]]):
        intvars_handle = make_intvar_array(intvars)
        predHandle = make_int_2d_array(predecessors)
        succHandle = make_int_2d_array(successors)
        constraint_handle = backend.all_different_prec_pred_succ(self.handle, intvars_handle, predHandle, succHandle)
        return _Constraint(constraint_handle, self)

    def all_equal(self, intvars: List[_IntVar]):
        vars_array = make_intvar_array(intvars)
        constraint_handle = backend.all_equal(self.handle, vars_array)
        return _Constraint(constraint_handle, self)

    def not_all_equal(self, intvars: List[_IntVar]):
        vars_array = make_intvar_array(intvars)
        constraint_handle = backend.not_all_equal(self.handle, vars_array)
        return _Constraint(constraint_handle, self)

    def among(self, nb_var: _IntVar, intvars: List[_IntVar], values: List[int]):
        vars_array = make_intvar_array(intvars)
        values_array = make_int_array(values)
        constraint_handle = backend.among(self.handle, nb_var.handle, vars_array, values_array)
        return _Constraint(constraint_handle, self)

    def and_(self, bools_or_constraints: Union[List[BoolVar], List[Constraint]]):
        assert len(bools_or_constraints) >= 1, "[and_] bools_or_constraints must not be empty"
        if isinstance(bools_or_constraints[0], BoolVar):
            vars_array = make_boolvar_array(bools_or_constraints)
            constraint_handle = backend.and_bv_bv(self.handle, vars_array)
        else:
            cons_array = make_constraint_array(bools_or_constraints)
            constraint_handle = backend.and_cs_cs(self.handle, cons_array)
        return _Constraint(constraint_handle, self)

    def at_least_n_values(self, intvars: List[_IntVar], n_values: _IntVar, ac: bool = False):
        vars_array = make_intvar_array(intvars)
        constraint_handle = backend.at_least_n_values(self.handle, vars_array, n_values.handle, ac)
        return _Constraint(constraint_handle, self)

    def at_most_n_values(self, intvars: List[_IntVar], n_values: _IntVar, strong: bool = False):
        vars_array = make_intvar_array(intvars)
        constraint_handle = backend.at_most_n_values(self.handle, vars_array, n_values.handle, strong)
        return _Constraint(constraint_handle, self)

    def bin_packing(self, item_bin: List[_IntVar], item_size: List[int], bin_load: List[_IntVar], offset: int = 0):
        item_bin_handle = make_intvar_array(item_bin)
        item_size_handle = make_int_array(item_size)
        bin_load_handle = make_intvar_array(bin_load)
        constraint_handle = backend.bin_packing(self.handle, item_bin_handle, item_size_handle,
                                                bin_load_handle, offset)
        return _Constraint(constraint_handle, self)

    def bools_int_channeling(self, boolvars: List[BoolVar], intvar: _IntVar, offset: int = 0):
        boolvars_handle = make_boolvar_array(boolvars)
        constraint_handle = backend.bools_int_channeling(self.handle, boolvars_handle, intvar.handle, offset)
        return _Constraint(constraint_handle, self)

    def bits_int_channeling(self, bits: List[BoolVar], intvar: _IntVar):
        bits_handle = make_boolvar_array(bits)
        constraint_handle = backend.bits_int_channeling(self.handle, bits_handle, intvar.handle)
        return _Constraint(constraint_handle, self)

    def clauses_int_channeling(self, intvar: _IntVar, e_vars: List[BoolVar], l_vars: List[BoolVar]):
        assert len(e_vars) == len(l_vars) == abs(1 + intvar.get_ub() - intvar.get_lb()), \
            "[clauses_int_channeling] e_vars and l_vars must have the same length as intvar's domain size"
        assert not isinstance(intvar, BoolVar), "[clauses_int_channeling] intvar cannot be a BoolVar"
        e_vars_handle = make_boolvar_array(e_vars)
        l_vars_handle = make_boolvar_array(l_vars)
        constraint_handle = backend.clauses_int_channeling(self.handle, intvar.handle, e_vars_handle, l_vars_handle)
        return _Constraint(constraint_handle, self)

    def circuit(self, intvars: List[_IntVar], offset: int = 0, conf: str = "RD"):
        intvars_handle = make_intvar_array(intvars)
        assert conf in ["LIGHT", "FIRST", "RD", "ALL"], "[circuit] conf must be in ['LIGHT', 'FIRST', 'RD', 'ALL']"
        constraint_handle = backend.circuit(self.handle, intvars_handle, offset, conf)
        return _Constraint(constraint_handle, self)

    def cost_regular(self, intvars: List[_IntVar], cost: _IntVar, cost_automaton: _CostAutomaton):
        intvars_handle = make_intvar_array(intvars)
        constraint_handle = backend.cost_regular(self.handle, intvars_handle, cost.handle, cost_automaton.handle)
        return _Constraint(constraint_handle, self)

    def count(self, value: Union[int, _IntVar], intvars: List[_IntVar], limit: _IntVar):
        intvars_handle = make_intvar_array(intvars)
        if isinstance(value, int):
            constraint_handle = backend.count_i(self.handle, value, intvars_handle, limit.handle)
        else:
            constraint_handle = backend.count_iv(self.handle, value.handle, intvars_handle, limit.handle)
        return _Constraint(constraint_handle, self)

    def cumulative(self, tasks: List[_Task], heights: List[_IntVar], capacity: _IntVar, incremental: bool = True):
        tasks_handle = make_task_array(tasks)
        vars_handle = make_intvar_array(heights)
        constraint_handle = backend.cumulative(self.handle, tasks_handle, vars_handle, capacity.handle, incremental)
        return _Constraint(constraint_handle, self)

    def diff_n(self, x: List[_IntVar], y: List[_IntVar], width: List[_IntVar], height: List[_IntVar],
               add_cumulative_reasoning: bool = True):
        x_handle = make_intvar_array(x)
        y_handle = make_intvar_array(y)
        width_handle = make_intvar_array(width)
        height_handle = make_intvar_array(height)
        constraint_handle = backend.diff_n(self.handle, x_handle, y_handle, width_handle, height_handle,
                                           add_cumulative_reasoning)
        return _Constraint(constraint_handle, self)

    def decreasing(self, intvars: List[_IntVar], delta: int = 0):
        intvars_handle = make_intvar_array(intvars)
        constraint_handle = backend.decreasing(self.handle, intvars_handle, delta)
        return _Constraint(constraint_handle, self)

    def increasing(self, intvars: List[_IntVar], delta: int = 0):
        intvars_handle = make_intvar_array(intvars)
        constraint_handle = backend.increasing(self.handle, intvars_handle, delta)
        return _Constraint(constraint_handle, self)

    def global_cardinality(self, intvars: List[_IntVar], values: List[int], occurrences: List[_IntVar],
                           closed: bool = False):
        intvars_handle = make_intvar_array(intvars)
        values_handle = make_int_array(values)
        occurrences_handle = make_intvar_array(occurrences)
        constraint_handle = backend.global_cardinality(self.handle, intvars_handle, values_handle, occurrences_handle,
                                                       closed)
        return _Constraint(constraint_handle, self)

    def inverse_channeling(self, intvars1: List[_IntVar], intvars2: List[_IntVar], offset1: int = 0, offset2: int = 0,
                           ac: bool = False):
        intvars1_handle = make_intvar_array(intvars1)
        intvars2_handle = make_intvar_array(intvars2)
        constraint_handle = backend.inverse_channeling(self.handle, intvars1_handle, intvars2_handle,
                                                       offset1, offset2, ac)
        return _Constraint(constraint_handle, self)

    def int_value_precede_chain(self, intvars: List[_IntVar], values: List[int]):
        intvars_handle = make_intvar_array(intvars)
        values_handle = make_int_array(values)
        constraint_handle = backend.int_value_precede_chain(self.handle, intvars_handle, values_handle)
        return _Constraint(constraint_handle, self)

    def keysort(self, intvars: List[List[_IntVar]], permutation_intvars: Union[List[_IntVar], None],
                sorted_intvars: List[List[_IntVar]], k: int):
        intvars_handle = make_intvar_2d_array(intvars)
        permutation_intvars_handle = None
        if permutation_intvars is not None:
            permutation_intvars_handle = make_intvar_array(permutation_intvars)
        sorted_intvars_handle = make_intvar_2d_array(sorted_intvars)
        constraint_handle = backend.keysort(self.handle, intvars_handle, permutation_intvars_handle,
                                            sorted_intvars_handle, k)
        return _Constraint(constraint_handle, self)

    def knapsack(self, occurrences: List[_IntVar], weight_sum: _IntVar, energy_sum: _IntVar, weight: List[int],
                 energy: List[int]):
        occ_handle = make_intvar_array(occurrences)
        weight_handle = make_int_array(weight)
        energy_handle = make_int_array(energy)
        constraint_handle = backend.knapsack(self.handle, occ_handle, weight_sum.handle, energy_sum.handle,
                                             weight_handle, energy_handle)
        return _Constraint(constraint_handle, self)

    def lex_chain_less(self, intvars: List[_IntVar]):
        intvars_handle = make_intvar_array(intvars)
        constraint_handle = backend.lex_chain_less(self.handle, intvars_handle)
        return _Constraint(constraint_handle, self)

    def lex_chain_less_eq(self, intvars: List[_IntVar]):
        intvars_handle = make_intvar_array(intvars)
        constraint_handle = backend.lex_chain_less_eq(self.handle, intvars_handle)
        return _Constraint(constraint_handle, self)

    def lex_less(self, intvars1: List[_IntVar], intvars2: List[_IntVar]):
        intvars_handle1 = make_intvar_array(intvars1)
        intvars_handle2 = make_intvar_array(intvars2)
        constraint_handle = backend.lex_less(self.handle, intvars_handle1, intvars_handle2)
        return _Constraint(constraint_handle, self)

    def lex_less_eq(self, intvars1: List[_IntVar], intvars2: List[_IntVar]):
        intvars_handle1 = make_intvar_array(intvars1)
        intvars_handle2 = make_intvar_array(intvars2)
        constraint_handle = backend.lex_less_eq(self.handle, intvars_handle1, intvars_handle2)
        return _Constraint(constraint_handle, self)

    def argmax(self, intvar: _IntVar, offset: int, intvars: List[_IntVar]):
        intvars_handle = make_intvar_array(intvars)
        constraint_handle = backend.argmax(self.handle, intvar.handle, offset, intvars_handle)
        return _Constraint(constraint_handle, self)

    def argmin(self, intvar: _IntVar, offset: int, intvars: List[_IntVar]):
        intvars_handle = make_intvar_array(intvars)
        constraint_handle = backend.argmin(self.handle, intvar.handle, offset, intvars_handle)
        return _Constraint(constraint_handle, self)

    def n_values(self, intvars: List[_IntVar], n_values: _IntVar):
        intvars_handle = make_intvar_array(intvars)
        constraint_handle = backend.n_values(self.handle, intvars_handle, n_values.handle)
        return _Constraint(constraint_handle, self)

    def or_(self, bools_or_constraints: Union[List[BoolVar], List[Constraint]]):
        assert len(bools_or_constraints) >= 1, "[or_] bools_or_constraint must not be empty"
        if isinstance(bools_or_constraints[0], BoolVar):
            vars_array = make_boolvar_array(bools_or_constraints)
            constraint_handle = backend.or_bv_bv(self.handle, vars_array)
        else:
            cons_array = make_constraint_array(bools_or_constraints)
            constraint_handle = backend.or_cs_cs(self.handle, cons_array)
        return _Constraint(constraint_handle, self)

    def path(self, intvars: List[_IntVar], start: _IntVar, end: _IntVar, offset: int = 0):
        intvars_handle = make_intvar_array(intvars)
        constraint_handle = backend.path(self.handle, intvars_handle, start.handle, end.handle, offset)
        return _Constraint(constraint_handle, self)

    def regular(self, intvars: List[_IntVar], automaton: _FiniteAutomaton):
        intvars_handle = make_intvar_array(intvars)
        constraint_handle = backend.regular(self.handle, intvars_handle, automaton.handle)
        return _Constraint(constraint_handle, self)

    def scalar(self, intvars: List[_IntVar], coeffs: List[int], operator: str, scalar: Union[int, _IntVar]):
        assert len(intvars) == len(coeffs), "[scalar] intvars and coeffs must have the same length"
        assert operator in ["=", "!=", ">", "<", ">=",
                            "<="], "[scalar] operator must be in ['=', '!=', '>', '<', '>=', '<=']"
        intvars_handle = make_intvar_array(intvars)
        coeffs_handle = make_int_array(coeffs)
        if isinstance(scalar, _IntVar):
            constraint_handle = backend.scalar_iv(self.handle, intvars_handle, coeffs_handle, operator, scalar.handle)
        else:
            constraint_handle = backend.scalar_i(self.handle, intvars_handle, coeffs_handle, operator, scalar)
        return _Constraint(constraint_handle, self)

    def sort(self, intvars: List[_IntVar], sorted_intvars: List[_IntVar]):
        intvars_handle = make_intvar_array(intvars)
        sorted_intvars_handle = make_intvar_array(sorted_intvars)
        constraint_handle = backend.sort(self.handle, intvars_handle, sorted_intvars_handle)
        return _Constraint(constraint_handle, self)

    def sub_circuit(self, intvars: List[_IntVar], offset: int, sub_circuit_length: _IntVar):
        intvars_handle = make_intvar_array(intvars)
        constraint_handle = backend.sub_circuit(self.handle, intvars_handle, offset, sub_circuit_length.handle)
        return _Constraint(constraint_handle, self)

    def sub_path(self, intvars: List[_IntVar], start: _IntVar, end: _IntVar, offset: int, sub_path_length: _IntVar):
        assert len(intvars) > 0, "[sub_path] intvars must not be empty"
        intvars_handle = make_intvar_array(intvars)
        constraint_handle = backend.sub_path(self.handle, intvars_handle, start.handle, end.handle, offset,
                                             sub_path_length.handle)
        return _Constraint(constraint_handle, self)

    def sum(self, intvars_or_boolvars: Union[List[_IntVar], List[BoolVar]], operator: str,
            sum_result: Union[int, _IntVar, List[_IntVar]]):
        assert len(intvars_or_boolvars) > 0, "[sum] intvars_or_boolvars must not be empty"
        assert operator in ["=", "!=", ">", "<", ">=",
                            "<="], "[sum] operator must be in ['=', '!=', '>', '<', '>=', '<=']"
        if isinstance(intvars_or_boolvars[0], _IntVar):
            vars_handle = make_intvar_array(intvars_or_boolvars)
            if isinstance(sum_result, int):
                constraint_handle = backend.sum_iv_i(self.handle, vars_handle, operator, sum_result)
            elif isinstance(sum_result, _IntVar):
                constraint_handle = backend.sum_iv_iv(self.handle, vars_handle, operator, sum_result.handle)
            else:
                sum_result_handle = make_intvar_array(sum_result)
                constraint_handle = backend.sum_ivarray_ivarray(self.handle, vars_handle, operator, sum_result_handle)
        else:
            vars_handle = make_boolvar_array(intvars_or_boolvars)
            if isinstance(sum_result, int):
                constraint_handle = backend.sum_bv_i(self.handle, vars_handle, operator, sum_result)
            elif isinstance(sum_result, _IntVar):
                constraint_handle = backend.sum_bv_iv(self.handle, vars_handle, operator, sum_result.handle)
            else:
                sum_result_handle = make_intvar_array(sum_result)
                constraint_handle = backend.sum_ivarray_ivarray(self.handle, vars_handle, operator, sum_result_handle)
        return _Constraint(constraint_handle, self)

    def tree(self, successors: List[_IntVar], nb_trees: _IntVar, offset: int = 0):
        successors_handle = make_intvar_array(successors)
        constraint_handle = backend.tree(self.handle, successors_handle, nb_trees.handle, offset)
        return _Constraint(constraint_handle, self)

    # Set constraints

    def set_union(self, intvars_or_setvars: Union[List[_IntVar], List[SetVar]], union: SetVar):
        assert len(intvars_or_setvars) > 0
        if isinstance(intvars_or_setvars[0], _IntVar):
            vars_handle = make_intvar_array(intvars_or_setvars)
            constraint_handle = backend.set_union_ints(self.handle, vars_handle, union.handle)
        else:
            vars_handle = make_setvar_array(intvars_or_setvars)
            constraint_handle = backend.set_union(self.handle, vars_handle, union.handle)
        return _Constraint(constraint_handle, self)

    def set_union_indices(self, setvars: List[SetVar], union: SetVar, indices: SetVar, v_offset: int = 0,
                          i_offset: int = 0):
        setvars_handle = make_setvar_array(setvars)
        constraint_handle = backend.set_union_indices(self.handle, setvars_handle, union.handle, indices.handle,
                                                      v_offset, i_offset)
        return _Constraint(constraint_handle, self)

    def set_intersection(self, setvars: List[SetVar], intersection: SetVar, bc: bool = False):
        setvars_handle = make_setvar_array(setvars)
        constraint_handle = backend.set_intersection(self.handle, setvars_handle, intersection.handle, bc)
        return _Constraint(constraint_handle, self)

    def set_subset_eq(self, setvars: List[SetVar]):
        setvars_handle = make_setvar_array(setvars)
        constraint_handle = backend.set_subset_eq(self.handle, setvars_handle)
        return _Constraint(constraint_handle, self)

    def set_nb_empty(self, setvars: List[SetVar], nb_empty: Union[_IntVar, int]):
        setvars_handle = make_setvar_array(setvars)
        constraint_handle = backend.set_nb_empty(self.handle, setvars_handle, nb_empty.handle)
        return _Constraint(constraint_handle, self)

    def set_offset(self, setvar_1: SetVar, setvar_2: SetVar, offset: int):
        constraint_handle = backend.set_offset(self.handle, setvar_1.handle, setvar_2.handle, offset)
        return _Constraint(constraint_handle, self)

    def set_not_empty(self, setvar: SetVar):
        constraint_handle = backend.set_not_empty(self.handle, setvar.handle)
        return _Constraint(constraint_handle, self)

    def set_sum(self, setvar: SetVar, sum_var: _IntVar):
        constraint_handle = backend.set_sum(self.handle, setvar.handle, sum_var.handle)
        return _Constraint(constraint_handle, self)

    def set_sum_element(self, indices: SetVar, weights: List[int], sum_var: _IntVar, offset: int = 0):
        weights_handle = make_int_array(weights)
        constraint_handle = backend.set_sum_elements(self.handle, indices.handle, weights_handle, offset,
                                                     sum_var.handle)
        return _Constraint(constraint_handle, self)

    def set_max(self, setvar: SetVar, max_var: _IntVar, not_empty: bool):
        constraint_handle = backend.set_max(self.handle, setvar.handle, max_var.handle, not_empty)
        return _Constraint(constraint_handle, self)

    def set_max_indices(self, indices: SetVar, weights: List[int], max_var: _IntVar, not_empty: bool, offset: int = 0):
        weights_handle = make_int_array(weights)
        constraint_handle = backend.set_max_indices(self.handle, indices.handle, weights_handle, offset, max_var.handle,
                                                    not_empty)
        return _Constraint(constraint_handle, self)

    def set_min(self, setvar: SetVar, min_var: _IntVar, not_empty: bool):
        constraint_handle = backend.set_min(self.handle, setvar.handle, min_var.handle, not_empty)
        return _Constraint(constraint_handle, self)

    def set_min_indices(self, indices: SetVar, weights: List[int], min_var: _IntVar, not_empty: bool, offset: int = 0):
        weights_handle = make_int_array(weights)
        constraint_handle = backend.set_min_indices(self.handle, indices.handle, weights_handle, offset, min_var.handle,
                                                    not_empty)
        return _Constraint(constraint_handle, self)

    def set_bools_channeling(self, boolvars: List[BoolVar], setvar: SetVar, offset: int = 0):
        boolvars_handle = make_boolvar_array(boolvars)
        constraint_handle = backend.set_bools_channeling(self.handle, boolvars_handle, setvar.handle, offset)
        return _Constraint(constraint_handle, self)

    def set_ints_channeling(self, setvars: List[SetVar], intvars: List[_IntVar], offset_1: int = 0, offset_2: int = 0):
        setvars_handle = make_setvar_array(setvars)
        intvars_handle = make_intvar_array(intvars)
        constraint_handle = backend.set_ints_channeling(self.handle, setvars_handle, intvars_handle, offset_1, offset_2)
        return _Constraint(constraint_handle, self)

    def set_disjoint(self, setvar_1: SetVar, setvar_2: SetVar):
        constraint_handle = backend.set_disjoint(self.handle, setvar_1.handle, setvar_2.handle)
        return _Constraint(constraint_handle, self)

    def set_all_disjoint(self, setvars: List[SetVar]):
        setvars_handle = make_setvar_array(setvars)
        constraint_handle = backend.set_all_disjoint(self.handle, setvars_handle)
        return _Constraint(constraint_handle, self)

    def set_all_different(self, setvars: List[SetVar]):
        setvars_handle = make_setvar_array(setvars)
        constraint_handle = backend.set_all_different(self.handle, setvars_handle)
        return _Constraint(constraint_handle, self)

    def set_all_equal(self, setvars: List[SetVar]):
        setvars_handle = make_setvar_array(setvars)
        constraint_handle = backend.set_all_equal(self.handle, setvars_handle)
        return _Constraint(constraint_handle, self)

    def set_partition(self, setvars: List[SetVar], universe: SetVar):
        setvars_handle = make_setvar_array(setvars)
        constraint_handle = backend.set_partition(self.handle, setvars_handle, universe.handle)
        return _Constraint(constraint_handle, self)

    def set_inverse_set(self, setvars: List[SetVar], inverse_setvars: List[SetVar], offset_1: int = 0,
                        offset_2: int = 0):
        setvars_handle = make_setvar_array(setvars)
        inv_setvars_handle = make_setvar_array(inverse_setvars)
        constraint_handle = backend.set_inverse_set(self.handle, setvars_handle, inv_setvars_handle, offset_1, offset_2)
        return _Constraint(constraint_handle, self)

    def set_symmetric(self, setvars: List[SetVar], offset: int = 0):
        setvars_handle = make_setvar_array(setvars)
        constraint_handle = backend.set_symmetric(self.handle, setvars_handle, offset)
        return _Constraint(constraint_handle, self)

    def set_element(self, index: _IntVar, setvars: List[SetVar], setvar: SetVar, offset: int = 0):
        setvars_handle = make_setvar_array(setvars)
        constraint_handle = backend.set_element(self.handle, index.handle, setvars_handle, setvar.handle, offset)
        return _Constraint(constraint_handle, self)

    def set_member_set(self, setvars: List[SetVar], setvar: SetVar):
        setvars_handle = make_setvar_array(setvars)
        constraint_handle = backend.set_member_set(self.handle, setvars_handle, setvar.handle)
        return _Constraint(constraint_handle, self)

    def set_member_int(self, intvar: Union[_IntVar, int], setvar: SetVar):
        iv = intvar
        if isinstance(intvar, int):
            iv = self.intvar(intvar)
        constraint_handle = backend.set_member_int(self.handle, iv.handle, setvar.handle)
        return _Constraint(constraint_handle, self)

    def set_not_member_int(self, intvar: Union[_IntVar, int], setvar: SetVar):
        iv = intvar
        if isinstance(intvar, int):
            iv = self.intvar(intvar)
        constraint_handle = backend.set_member_int(self.handle, iv.handle, setvar.handle)
        return _Constraint(constraint_handle, self)

    def set_le(self, setvar_1: SetVar, setvar_2: SetVar):
        constraint_handle = backend.set_le(self.handle, setvar_1.handle, setvar_2.handle)
        return _Constraint(constraint_handle, self)

    def set_lt(self, setvar_1: SetVar, setvar_2: SetVar):
        constraint_handle = backend.set_lt(self.handle, setvar_1.handle, setvar_2.handle)
        return _Constraint(constraint_handle, self)


def _create_model(name=None):
    if name is not None:
        handle = backend.create_model_s(name)
    else:
        handle = backend.create_model()
    return _Model(handle)
