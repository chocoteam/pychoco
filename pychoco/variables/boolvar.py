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

    def __and__(self, other):
        if isinstance(other, BoolVar):
            return self.model.and_([self, other]).reify()
        elif isinstance(other, bool):
            return self.model.and_([self, self.model.boolvar(other)]).reify()
        else:
            raise NotImplementedError("Unsupported operation between BoolVar and {}".format(other.__class__))

    def __rand__(self, other):
        return self.__and__(other)

    def __or__(self, other):
        if isinstance(other, BoolVar):
            return self.model.or_([self, other]).reify()
        elif isinstance(other, bool):
            return self.model.or_([self, self.model.boolvar(other)]).reify()
        else:
            raise NotImplementedError("Unsupported operation between BoolVar and {}".format(other.__class__))

    def __ror__(self, other):
        return self.__or__(other)

    def __invert__(self):
        return self.model.bool_not_view(self)

    def __eq__(self, other):
        if isinstance(other, (IntVar, BoolVar)):
            return self.model.arithm(self, "=", other).reify()
        elif isinstance(other, bool):
            return self.model.int_eq_view(self, other)
        else:
            raise NotImplementedError("Unsupported operation between BoolVar and {}".format(other.__class__))

    def __ne__(self, other):
        if isinstance(other, (IntVar, BoolVar)):
            return self.model.arithm(self, "!=", other).reify()
        elif isinstance(other, bool):
            return self.model.int_ne_view(self, other)
        else:
            raise NotImplementedError("Unsupported operation between BoolVar and {}".format(other.__class__))
