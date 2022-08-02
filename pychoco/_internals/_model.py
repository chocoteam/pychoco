from typing import Union, List

from pychoco import backend
from pychoco._internals._boolvar import _BoolVar
from pychoco._internals._constraint import _Constraint
from pychoco._internals._handle_wrapper import _HandleWrapper
from pychoco._internals._intvar import _IntVar
from pychoco._internals._solver import _Solver
from pychoco._internals._utils import make_int_var_array, make_int_array
from pychoco.model import Model
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

    def intvar(self, lb, ub, name=None):
        if name is None:
            var_handle = backend.intvar_ii(self.handle, lb, ub)
        else:
            var_handle = backend.intvar_sii(self.handle, name, lb, ub)
        return _IntVar(var_handle, self)

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

    # IntConstraintFactor methods implementation

    def arithm(self, x: _IntVar, op1: str, y: Union[int, _IntVar],
               op2: Union[None, str] = None, z: Union[None, int, _IntVar] = None):
        constraint_handle = None
        # Case 1
        if isinstance(y, int) and op2 is None and z is None:
            constraint_handle = backend.arithm_iv_cst(self.handle, x.handle, op1, y)
        if isinstance(y, IntVar) and op2 is None and z is None:
            constraint_handle = backend.arithm_iv_iv(self.handle, x.handle, op1, y.handle)
        if isinstance(y, IntVar) and op2 is not None and isinstance(z, int):
            constraint_handle = backend.arithm_iv_iv_cst(self.handle, x.handle, op1, y.handle, op2, z)
        if isinstance(y, IntVar) and op2 is not None and isinstance(z, IntVar):
            constraint_handle = backend.arithm_iv_iv_iv(self.handle, x.handle, op1, y.handle, op2, z.handle)
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
        constraint_handle = backend._not(self.handle, constraint.handle)
        return _Constraint(constraint_handle, self)

    def absolute(self, x: _IntVar, y: _IntVar):
        constraint_handle = backend.absolute(self.handle, x.handle, y.handle)
        return _Constraint(constraint_handle, self)

    def distance(self, x: _IntVar, y: _IntVar, op: str, z: Union[int, _IntVar]):
        if isinstance(z, int):
            constraint_handle = backend.distance_iv_iv_i(self.handle, x.handle, y.handle, z)
        else:
            constraint_handle = backend.distance_iv_iv_iv(self.handle, x.handle, y.handle, z.handle)
        return _Constraint(constraint_handle, self)

    def element(self, x: _IntVar, table: Union[List[int], List[_IntVar]], index: _IntVar, offset: int = 0):
        if len(table) == 0:
            raise AttributeError("table parameter in element constraint must have a length > 0")
        if isinstance(table[0], int):
            ints_array_handle = make_int_array(*table)
            constraint_handle = backend.element_iv_iarray_iv_i(self.handle, x.handle, ints_array_handle,
                                                               index.handle, offset)
        else:
            int_var_array_handle = make_int_var_array(*table)
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
        int_var_array_handle = make_int_var_array(*intvars)
        constraint_hande = backend.max_iv_ivarray(self.handle, x.handle, int_var_array_handle)
        return _Constraint(constraint_hande, self)

    def min(self, x: IntVar, *intvars: List[IntVar]):
        int_var_array_handle = make_int_var_array(*intvars)
        constraint_hande = backend.min_iv_ivarray(self.handle, x.handle, int_var_array_handle)
        return _Constraint(constraint_hande, self)

    def all_different(self, *intvars: List[IntVar]):
        vars_array = make_int_var_array(*intvars)
        constraint_handle = backend.all_different(self.handle, vars_array)
        return _Constraint(constraint_handle, self)


def _create_model(name):
    handle = backend.create_model(name)
    return _Model(handle)
