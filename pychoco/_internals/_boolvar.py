from pychoco._internals._handle_wrapper import _HandleWrapper
from pychoco._internals._intvar import _IntVar
from pychoco.variables.boolvar import BoolVar


class _BoolVar(BoolVar, _IntVar, _HandleWrapper):
    """
    Internal class to represent a boolvar.
    """

    def __init__(self, handle, model):
        super().__init__(handle, model)
