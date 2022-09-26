from pychoco.variables.intvar import IntVar


class BoolVar(IntVar):
    """
    A boolean variable (BoolVar) is an unknown whose value should be a boolean (0 / 1,
    or False / True). Therefore, the domain of an integer variable is [0, 1].
    """

    def get_type(self):
        return "BoolVar"

    def get_value(self):
        return bool(super().get_value())
