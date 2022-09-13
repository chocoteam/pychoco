from typing import Union, List

from pychoco import backend
from pychoco._internals._boolvar import _BoolVar
from pychoco._internals._constraint import _Constraint
from pychoco._internals._cost_automaton import _CostAutomaton
from pychoco._internals._handle_wrapper import _HandleWrapper
from pychoco._internals._intvar import _IntVar
from pychoco._internals._solver import _Solver
from pychoco._internals._utils import make_intvar_array, make_int_array, make_boolvar_array, make_constraint_array, \
    make_int_array_array
from pychoco.constraints.constraint import Constraint
from pychoco.model import Model
from pychoco.variables.boolvar import BoolVar
from pychoco.variables.intvar import IntVar


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
        if isinstance(y, IntVar) and op2 is None and z is None:
            constraint_handle = backend.arithm_iv_iv(self.handle, x.handle, op1, y.handle)
        if isinstance(y, IntVar) and op2 is not None and isinstance(z, int):
            constraint_handle = backend.arithm_iv_iv_cst(self.handle, x.handle, op1, y.handle, op2, z)
        if isinstance(y, IntVar) and op2 is not None and isinstance(z, IntVar):
            constraint_handle = backend.arithm_iv_iv_iv(self.handle, x.handle, op1, y.handle, op2, z.handle)
        if constraint_handle is None:
            raise AttributeError("Invalid parameters combination for arithm constraint. Please refer to the doc")
        return _Constraint(constraint_handle, self)

    def member(self, x: _IntVar, table: Union[list, tuple, None] = None,
               lb: Union[None, int] = None, ub: Union[None, int] = None):
        if table is not None:
            ints_array = make_int_array(*table)
            constraint_handle = backend.member_iv_iarray(self.handle, x.handle, ints_array)
        else:
            constraint_handle = backend.member_iv_i_i(self.handle, x.handle, lb, ub)
        return _Constraint(constraint_handle, self)

    def not_member(self, x: _IntVar, table: Union[list, tuple, None] = None,
                   lb: Union[None, int] = None, ub: Union[None, int] = None):
        if table is not None:
            ints_array = make_int_array(*table)
            constraint_handle = backend.not_member_iv_iarray(self.handle, x.handle, ints_array)
        else:
            constraint_handle = backend.not_member_iv_i_i(self.handle, x.handle, lb, ub)
        return _Constraint(constraint_handle, self)

    def mod(self, x, mod: Union[int, _IntVar], res: Union[int, _IntVar]):
        constraint_handle = None
        if isinstance(mod, int) and isinstance(res, int):
            constraint_handle = backend.mod_iv_i_i(self.handle, x.handle, mod, res)
        if isinstance(mod, int) and isinstance(res, IntVar):
            constraint_handle = backend.mod_iv_i_iv(self.handle, x.handle, mod, res.handle)
        if isinstance(mod, IntVar) and isinstance(res, IntVar):
            constraint_handle = backend.mod_iv_iv_iv(self.handle, x.handle, mod.handle, res.handle)
        return _Constraint(constraint_handle, self)

    def not_(self, constraint: _Constraint):
        constraint_handle = backend.not_(self.handle, constraint.handle)
        return _Constraint(constraint_handle, self)

    def absolute(self, x: _IntVar, y: _IntVar):
        constraint_handle = backend.absolute(self.handle, x.handle, y.handle)
        return _Constraint(constraint_handle, self)

    def distance(self, x: _IntVar, y: _IntVar, op: str, z: Union[int, _IntVar]):
        if isinstance(z, IntVar):
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
            ints_array_handle = make_int_array(*table)
            constraint_handle = backend.element_iv_iarray_iv_i(self.handle, x.handle, ints_array_handle,
                                                               index.handle, offset)
        else:
            int_var_array_handle = make_intvar_array(*table)
            constraint_handle = backend.element_iv_ivarray_iv_i(self.handle, x.handle, int_var_array_handle,
                                                                index.handle, offset)
        return _Constraint(constraint_handle, self)

    def square(self, x: _IntVar, y: _IntVar):
        constraint_handle = backend.square(self.handle, x.handle, y.handle)
        return _Constraint(constraint_handle, self)

    def table(self, intvars: List[IntVar], tuples: List[List[int]], feasible: bool = True, algo: str = "GAC3rm"):
        assert algo in ["CT+", "GAC3rm", "GAC2001", "GACSTR", "GAC2001+", "GAC3rm+",
                        "FC", "STR2+"], '[table] algo must be in ["CT+", "GAC3rm", "GAC2001", "GACSTR", "GAC2001+", ' \
                                        '"GAC3rm+", "FC", "STR2+"]'
        vars_handle = make_intvar_array(*intvars)
        tuples_handle = make_int_array_array(*tuples)
        constraint_handle = backend.table(self.handle, vars_handle, tuples_handle, feasible, algo)
        return _Constraint(constraint_handle, self)

    def times(self, x: _IntVar, y: Union[int, _IntVar], z: Union[int, _IntVar]):
        constraint_handle = None
        if isinstance(z, IntVar) and isinstance(y, int):
            constraint_handle = backend.times_iv_i_iv(self.handle, x.handle, y, z.handle)
        if isinstance(y, IntVar) and isinstance(z, int):
            constraint_handle = backend.times_iv_iv_i(self.handle, x.handle, y.handle, z)
        if isinstance(y, IntVar) and isinstance(z, IntVar):
            constraint_handle = backend.times_iv_iv_iv(self.handle, x.handle, y.handle, z.handle)
        return _Constraint(constraint_handle, self)

    def pow(self, x: IntVar, c: int, y: IntVar):
        constraint_handle = backend.pow_(self.handle, x.handle, c, y.handle)
        return _Constraint(constraint_handle, self)

    def div(self, dividend: _IntVar, divisor: _IntVar, result: _IntVar):
        constraint_handle = backend.div_(self.handle, dividend.handle, divisor.handle, result.handle)
        return _Constraint(constraint_handle, self)

    def max(self, x: _IntVar, *intvars: List[_IntVar]):
        int_var_array_handle = make_intvar_array(*intvars)
        constraint_hande = backend.max_iv_ivarray(self.handle, x.handle, int_var_array_handle)
        return _Constraint(constraint_hande, self)

    def min(self, x: IntVar, *intvars: List[IntVar]):
        int_var_array_handle = make_intvar_array(*intvars)
        constraint_hande = backend.min_iv_ivarray(self.handle, x.handle, int_var_array_handle)
        return _Constraint(constraint_hande, self)

    def all_different(self, *intvars: List[IntVar]):
        vars_array = make_intvar_array(*intvars)
        constraint_handle = backend.all_different(self.handle, vars_array)
        return _Constraint(constraint_handle, self)

    def all_equal(self, *intvars: List[IntVar]):
        vars_array = make_intvar_array(*intvars)
        constraint_handle = backend.all_equal(self.handle, vars_array)
        return _Constraint(constraint_handle, self)

    def not_all_equal(self, *intvars: List[IntVar]):
        vars_array = make_intvar_array(*intvars)
        constraint_handle = backend.not_all_equal(self.handle, vars_array)
        return _Constraint(constraint_handle, self)

    def among(self, nb_var: IntVar, intvars: List[IntVar], values: List[int]):
        vars_array = make_intvar_array(*intvars)
        values_array = make_int_array(*values)
        constraint_handle = backend.among(self.handle, nb_var.handle, vars_array, values_array)
        return _Constraint(constraint_handle, self)

    def and_(self, *bools_or_constraints: Union[List[BoolVar], List[Constraint]]):
        assert len(bools_or_constraints) >= 1, "[and_] bools_or_constraints must not be empty"
        if isinstance(bools_or_constraints[0], BoolVar):
            vars_array = make_boolvar_array(*bools_or_constraints)
            constraint_handle = backend.and_bv_bv(self.handle, vars_array)
        else:
            cons_array = make_constraint_array(*bools_or_constraints)
            constraint_handle = backend.and_cs_cs(self.handle, cons_array)
        return _Constraint(constraint_handle, self)

    def at_least_n_values(self, intvars: List[IntVar], n_values: IntVar, ac: bool = False):
        vars_array = make_intvar_array(*intvars)
        constraint_handle = backend.at_least_n_values(self.handle, vars_array, n_values.handle, ac)
        return _Constraint(constraint_handle, self)

    def at_most_n_values(self, intvars: List[IntVar], n_values: IntVar, strong: bool = False):
        vars_array = make_intvar_array(*intvars)
        constraint_handle = backend.at_most_n_values(self.handle, vars_array, n_values.handle, strong)
        return _Constraint(constraint_handle, self)

    def bin_packing(self, item_bin: List[IntVar], item_size: List[int], bin_load: List[IntVar], offset: int = 0):
        item_bin_handle = make_intvar_array(*item_bin)
        item_size_handle = make_int_array(*item_size)
        bin_load_handle = make_intvar_array(*bin_load)
        constraint_handle = backend.bin_packing(self.handle, item_bin_handle, item_size_handle,
                                                bin_load_handle, offset)
        return _Constraint(constraint_handle, self)

    def bools_int_channeling(self, boolvars: List[BoolVar], intvar: IntVar, offset: int = 0):
        boolvars_handle = make_boolvar_array(*boolvars)
        constraint_handle = backend.bools_int_channeling(self.handle, boolvars_handle, intvar.handle, offset)
        return _Constraint(constraint_handle, self)

    def bits_int_channeling(self, bits: List[BoolVar], intvar: IntVar):
        bits_handle = make_boolvar_array(*bits)
        constraint_handle = backend.bits_int_channeling(self.handle, bits_handle, intvar.handle)
        return _Constraint(constraint_handle, self)

    def clauses_int_channeling(self, intvar: IntVar, e_vars: List[BoolVar], l_vars: List[BoolVar]):
        assert len(e_vars) == len(l_vars) == abs(1 + intvar.get_ub() - intvar.get_lb()), \
            "[clauses_int_channeling] e_vars and l_vars must have the same length as intvar's domain size"
        assert not isinstance(intvar, BoolVar), "[clauses_int_channeling] intvar cannot be a BoolVar"
        e_vars_handle = make_boolvar_array(*e_vars)
        l_vars_handle = make_boolvar_array(*l_vars)
        constraint_handle = backend.clauses_int_channeling(self.handle, intvar.handle, e_vars_handle, l_vars_handle)
        return _Constraint(constraint_handle, self)

    def circuit(self, intvars: List[IntVar], offset: int = 0, conf: str = "RD"):
        intvars_handle = make_intvar_array(*intvars)
        assert conf in ["LIGHT", "FIRST", "RD", "ALL"], "[circuit] conf must be in ['LIGHT', 'FIRST', 'RD', 'ALL']"
        constraint_handle = backend.circuit(self.handle, intvars_handle, offset, conf)
        return _Constraint(constraint_handle, self)

    def cost_regular(self, intvars: List[IntVar], cost: IntVar, cost_automaton: _CostAutomaton):
        intvars_handle = make_intvar_array(*intvars)
        constraint_handle = backend.cost_regular(self.handle, intvars_handle, cost.handle, cost_automaton.handle)
        return _Constraint(constraint_handle, self)

    def count(self, value: Union[int, IntVar], intvars: List[IntVar], limit: IntVar):
        intvars_handle = make_intvar_array(*intvars)
        if isinstance(value, int):
            constraint_handle = backend.count_i(self.handle, value, intvars_handle, limit.handle)
        else:
            constraint_handle = backend.count_iv(self.handle, value.handle, intvars_handle, limit.handle)
        return _Constraint(constraint_handle, self)

    def diff_n(self, x: List[IntVar], y: List[IntVar], width: List[IntVar], height: List[IntVar],
               add_cumulative_reasoning: bool = True):
        x_handle = make_intvar_array(*x)
        y_handle = make_intvar_array(*y)
        width_handle = make_intvar_array(*width)
        height_handle = make_intvar_array(*height)
        constraint_handle = backend.diff_n(self.handle, x_handle, y_handle, width_handle, height_handle,
                                           add_cumulative_reasoning)
        return _Constraint(constraint_handle, self)

    def decreasing(self, intvars: List[IntVar], delta: int = 0):
        intvars_handle = make_intvar_array(*intvars)
        constraint_handle = backend.decreasing(self.handle, intvars_handle, delta)
        return _Constraint(constraint_handle, self)

    def increasing(self, intvars: List[IntVar], delta: int = 0):
        intvars_handle = make_intvar_array(*intvars)
        constraint_handle = backend.increasing(self.handle, intvars_handle, delta)
        return _Constraint(constraint_handle, self)

    def global_cardinality(self, intvars: List[IntVar], values: List[int], occurrences: List[IntVar],
                           closed: bool = False):
        intvars_handle = make_intvar_array(*intvars)
        values_handle = make_int_array(*values)
        occurrences_handle = make_intvar_array(*occurrences)
        constraint_handle = backend.global_cardinality(self.handle, intvars_handle, values_handle, occurrences_handle,
                                                       closed)
        return _Constraint(constraint_handle, self)

    def inverse_channeling(self, intvars1: List[IntVar], intvars2: List[IntVar], offset1: int = 0, offset2: int = 0,
                           ac: bool = False):
        intvars1_handle = make_intvar_array(*intvars1)
        intvars2_handle = make_intvar_array(*intvars2)
        constraint_handle = backend.inverse_channeling(self.handle, intvars1_handle, intvars2_handle,
                                                       offset1, offset2, ac)
        return _Constraint(constraint_handle, self)

    def int_value_precede_chain(self, intvars: List[IntVar], *values: List[int]):
        intvars_handle = make_intvar_array(*intvars)
        values_handle = make_int_array(*values)
        constraint_handle = backend.int_value_precede_chain(self.handle, intvars_handle, values_handle)
        return _Constraint(constraint_handle, self)

    def knapsack(self, occurrences: List[IntVar], weight_sum: IntVar, energy_sum: IntVar, weight: List[int],
                 energy: List[int]):
        occ_handle = make_intvar_array(*occurrences)
        weight_handle = make_int_array(*weight)
        energy_handle = make_int_array(*energy)
        constraint_handle = backend.knapsack(self.handle, occ_handle, weight_sum.handle, energy_sum.handle,
                                             weight_handle, energy_handle)
        return _Constraint(constraint_handle, self)

    def lex_chain_less(self, *intvars: List[IntVar]):
        intvars_handle = make_intvar_array(*intvars)
        constraint_handle = backend.lex_chain_less(self.handle, intvars_handle)
        return _Constraint(constraint_handle, self)

    def lex_chain_less_eq(self, *intvars: List[IntVar]):
        intvars_handle = make_intvar_array(*intvars)
        constraint_handle = backend.lex_chain_less_eq(self.handle, intvars_handle)
        return _Constraint(constraint_handle, self)

    def lex_less(self, intvars1: List[IntVar], intvars2: List[IntVar]):
        intvars_handle1 = make_intvar_array(*intvars1)
        intvars_handle2 = make_intvar_array(*intvars2)
        constraint_handle = backend.lex_less(self.handle, intvars_handle1, intvars_handle2)
        return _Constraint(constraint_handle, self)

    def lex_less_eq(self, intvars1: List[IntVar], intvars2: List[IntVar]):
        intvars_handle1 = make_intvar_array(*intvars1)
        intvars_handle2 = make_intvar_array(*intvars2)
        constraint_handle = backend.lex_less_eq(self.handle, intvars_handle1, intvars_handle2)
        return _Constraint(constraint_handle, self)

    def argmax(self, intvar: IntVar, offset: int, intvars: List[IntVar]):
        intvars_handle = make_intvar_array(*intvars)
        constraint_handle = backend.argmax(self.handle, intvar.handle, offset, intvars_handle)
        return _Constraint(constraint_handle, self)

    def argmin(self, intvar: IntVar, offset: int, intvars: List[IntVar]):
        intvars_handle = make_intvar_array(*intvars)
        constraint_handle = backend.argmin(self.handle, intvar.handle, offset, intvars_handle)
        return _Constraint(constraint_handle, self)

    def n_values(self, intvars: List[IntVar], n_values: IntVar):
        intvars_handle = make_intvar_array(*intvars)
        constraint_handle = backend.n_values(self.handle, intvars_handle, n_values.handle)
        return _Constraint(constraint_handle, self)

    def or_(self, *bools_or_constraints: Union[List[BoolVar], List[Constraint]]):
        assert len(bools_or_constraints) >= 1, "[or_] bools_or_constraint must not be empty"
        if isinstance(bools_or_constraints[0], BoolVar):
            vars_array = make_boolvar_array(*bools_or_constraints)
            constraint_handle = backend.or_bv_bv(self.handle, vars_array)
        else:
            cons_array = make_constraint_array(*bools_or_constraints)
            constraint_handle = backend.or_cs_cs(self.handle, cons_array)
        return _Constraint(constraint_handle, self)

    def path(self, intvars: List[IntVar], start: IntVar, end: IntVar, offset: int = 0):
        intvars_handle = make_intvar_array(*intvars)
        constraint_handle = backend.path(self.handle, intvars_handle, start.handle, end.handle, offset)
        return _Constraint(constraint_handle, self)

    def scalar(self, intvars: List[IntVar], coeffs: List[int], operator: str, scalar: Union[int, IntVar]):
        assert len(intvars) == len(coeffs), "[scalar] intvars and coeffs must have the same length"
        assert operator in ["=", "!=", ">", "<", ">=",
                            "<="], "[scalar] operator must be in ['=', '!=', '>', '<', '>=', '<=']"
        intvars_handle = make_intvar_array(*intvars)
        coeffs_handle = make_int_array(*coeffs)
        if isinstance(scalar, IntVar):
            constraint_handle = backend.scalar_iv(self.handle, intvars_handle, coeffs_handle, operator, scalar.handle)
        else:
            constraint_handle = backend.scalar_i(self.handle, intvars_handle, coeffs_handle, operator, scalar)
        return _Constraint(constraint_handle, self)

    def sort(self, intvars: List[IntVar], sorted_intvars: List[IntVar]):
        intvars_handle = make_intvar_array(*intvars)
        sorted_intvars_handle = make_intvar_array(*sorted_intvars)
        constraint_handle = backend.sort(self.handle, intvars_handle, sorted_intvars_handle)
        return _Constraint(constraint_handle, self)

    def sub_circuit(self, intvars: List[IntVar], offset: int, sub_circuit_length: IntVar):
        intvars_handle = make_intvar_array(*intvars)
        constraint_handle = backend.sub_circuit(self.handle, intvars_handle, offset, sub_circuit_length.handle)
        return _Constraint(constraint_handle, self)

    def sub_path(self, intvars: List[IntVar], start: IntVar, end: IntVar, offset: int, sub_path_length: IntVar):
        assert len(intvars) > 0, "[sub_path] intvars must not be empty"
        intvars_handle = make_intvar_array(*intvars)
        constraint_handle = backend.sub_path(self.handle, intvars_handle, start.handle, end.handle, offset,
                                             sub_path_length.handle)
        return _Constraint(constraint_handle, self)

    def sum(self, intvars_or_boolvars: Union[List[IntVar], List[BoolVar]], operator: str,
            sum_result: Union[int, IntVar, List[IntVar]]):
        assert len(intvars_or_boolvars) > 0, "[sum] intvars_or_boolvars must not be empty"
        assert operator in ["=", "!=", ">", "<", ">=",
                            "<="], "[sum] operator must be in ['=', '!=', '>', '<', '>=', '<=']"
        if isinstance(intvars_or_boolvars[0], IntVar):
            vars_handle = make_intvar_array(*intvars_or_boolvars)
            if isinstance(sum_result, int):
                constraint_handle = backend.sum_iv_i(self.handle, vars_handle, operator, sum_result)
            elif isinstance(sum_result, IntVar):
                constraint_handle = backend.sum_iv_iv(self.handle, vars_handle, operator, sum_result.handle)
            else:
                sum_result_handle = make_intvar_array(*sum_result)
                constraint_handle = backend.sum_ivarray_ivarry(self.handle, vars_handle, operator, sum_result_handle)
        else:
            vars_handle = make_boolvar_array(*intvars_or_boolvars)
            if isinstance(sum_result, int):
                constraint_handle = backend.sum_bv_i(self.handle, vars_handle, operator, sum_result)
            elif isinstance(sum_result, IntVar):
                constraint_handle = backend.sum_bv_iv(self.handle, vars_handle, operator, sum_result.handle)
            else:
                sum_result_handle = make_intvar_array(*sum_result)
                constraint_handle = backend.sum_ivarray_ivarry(self.handle, vars_handle, operator, sum_result_handle)
        return _Constraint(constraint_handle, self)

    def tree(self, successors: List[IntVar], nb_trees: IntVar, offset: int = 0):
        successors_handle = make_intvar_array(*successors)
        constraint_handle = backend.tree(self.handle, successors_handle, nb_trees.handle, offset)
        return _Constraint(constraint_handle, self)


def _create_model(name=None):
    if name is not None:
        handle = backend.create_model_s(name)
    else:
        handle = backend.create_model()
    return _Model(handle)
