from abc import ABC

from pychoco.variables.intvar import IntVar


class BoolVar(IntVar, ABC):
    """
    An integer variable (IntVar) is an unknown whose value should be a boolean (0 / 1,
    or False / True). Therefore, the domain of an integer variable is [0, 1].
    """

    def __repr__(self):
        return "Choco BoolVar ('" + self.get_name() + "')"
