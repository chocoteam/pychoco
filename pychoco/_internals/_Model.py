from pychoco import backend
from pychoco.Model import Model
from pychoco._internals._Constraint import _Constraint
from pychoco._internals._HandleWrapper import _HandleWrapper
from pychoco._internals._IntVar import _IntVar
from pychoco.constraints.IntConstraintFactory import IntConstraintFactory
from pychoco.variables.VariableFactory import VariableFactory


class _Model(Model, VariableFactory, IntConstraintFactory, _HandleWrapper):
    """
    Internal class to represent a choco model.
    """

    def __init__(self, handle):
        super().__init__(handle)

    # Model methods implementation

    def get_name(self):
        return backend.get_model_name(self.handle)

    # VariableFactory methods implementation

    def intvar(self, lb, ub, name=None):
        if name is None:
            var_handle = backend.intvar_ii(self.handle, lb, ub)
        else:
            var_handle = backend.intvar_sii(self.handle, name, lb, ub)
        return _IntVar(var_handle, self)

    # IntConstraintFactor methods implementation

    def all_different(self, *intvars):
        vars_array = backend.create_intvar_array(len(intvars))
        for i in range(0, len(intvars)):
            backend.intvar_array_set(vars_array, intvars[i].handle, i)
        constraint_handle = backend.all_different(self.handle, vars_array)
        return _Constraint(constraint_handle)


def _create_model(name):
    handle = backend.create_model(name)
    return _Model(handle)
