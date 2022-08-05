from typing import Union, List

from pychoco import backend
from pychoco._internals._boolvar import _BoolVar
from pychoco._internals._constraint import _Constraint
from pychoco._internals._handle_wrapper import _HandleWrapper
from pychoco._internals._intvar import _IntVar
from pychoco._internals._solver import _Solver
from pychoco._internals._utils import make_intvar_array, make_int_array, make_boolvar_array, make_constraint_array
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
            assert op in {"=", ">", "<"}
        else:
            assert op in {"=", "!=", ">", "<"}
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

    def times(self, x: _IntVar, y: Union[int, _IntVar], z: Union[int, _IntVar]):
        constraint_handle = None
        if isinstance(z, IntVar) and isinstance(y, int):
            constraint_handle = backend.times_iv_i_iv(self.handle, x.handle, y, z.handle)
        if isinstance(y, IntVar) and isinstance(z, int):
            constraint_handle = backend.times_iv_iv_i(self.handle, x.handle, y.handle, z)
        if isinstance(y, IntVar) and isinstance(z, IntVar):
            constraint_handle = backend.times_iv_iv_iv(self.handle, x.handle, y.handle, z.handle)
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

    def and_(self, bools_or_constraints: Union[List[BoolVar], List[Constraint]]):
        assert len(bools_or_constraints) >= 1
        if isinstance(bools_or_constraints[0], BoolVar):
            vars_array = make_boolvar_array(*bools_or_constraints)
            constraint_handle = backend.and_bv_bv(self.handle, vars_array)
        else:
            cons_array = make_constraint_array(*bools_or_constraints)
            constraint_handle = backend.and_cs_cs(self.handle, cons_array)
        return _Constraint(constraint_handle, self)


def _create_model(name=None):
    if name is not None:
        handle = backend.create_model_s(name)
    else:
        handle = backend.create_model()
    return _Model(handle)
