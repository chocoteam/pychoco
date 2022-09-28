from pychoco import backend
from pychoco.variables.variable import Variable


class IntVar(Variable):
    """
    An integer variable (IntVar) is an unknown whose value should be an integer.
    Therefore, the domain of an integer variable is a set of integers (representing
    possible values). This set of integers can be either represented by an interval
    (with a lower bound and an upper bound), or enumerated.
    """

    def get_lb(self):
        """
        :return: The lower bound of the variable.
        """
        return backend.get_intvar_lb(self.handle)

    def get_ub(self):
        """
        :return: The upper bound of the variable.
        """
        return backend.get_intvar_ub(self.handle)

    def get_value(self):
        """
        :return: The value of the variable (only valid if it is instantiated).
        """
        assert self.is_instantiated(), "{} is not instantiated".format(self.name)
        return backend.get_intvar_value(self.handle)

    def get_type(self):
        return "IntVar"

    def __add__(self, other):
        if isinstance(other, IntVar):
            res = self.model.intvar(self.get_lb() + other.get_lb(), self.get_ub() + other.get_ub())
            self.model.arithm(self, "+", other, "=", res).post()
            return res
        elif isinstance(other, int):
            return self.model.int_offset_view(self, other)
        else:
            raise TypeError("Unsupported operation between IntVar and {}".format(other.__class__))

    def __sub__(self, other):
        if isinstance(other, IntVar):
            res = self.model.intvar(self.get_lb() - other.get_ub(), self.get_ub() - other.get_lb())
            self.model.arithm(self, "-", other, "=", res).post()
            return res
        elif isinstance(other, int):
            return self.model.int_offset_view(self, -other)
        else:
            raise TypeError("Unsupported operation between IntVar and {}".format(other.__class__))

    def __neg__(self):
        return self.model.int_minus_view(self)

    def __mul__(self, other):
        if isinstance(other, IntVar):
            a = [self.get_lb() * other.get_lb(), self.get_lb() * other.get_ub(), self.get_ub() * other.get_lb(),
                 self.get_ub() * other.get_ub()]
            res = self.model.intvar(min(a), max(a))
            self.model.arithm(self, "*", other, "=", res).post()
            return res
        elif isinstance(other, int):
            return self.model.int_scale_view(self, other)
        else:
            raise TypeError("Unsupported operation between IntVar and {}".format(other.__class__))

    def __truediv__(self, other):
        if isinstance(other, IntVar):
            a = [int(self.get_lb() / other.get_lb()), int(self.get_lb() / other.get_ub()),
                 int(self.get_ub() / other.get_lb()),
                 int(self.get_ub() / other.get_ub())]
            res = self.model.intvar(min(a), max(a))
            self.model.arithm(self, "/", other, "=", res).post()
            return res
        elif isinstance(other, int):
            a = [int(self.get_lb() / other), int(self.get_ub() / other)]
            res = self.model.intvar(min(a), max(a))
            self.model.arithm(self, "/", other, "=", res).post()
            return res
        else:
            raise TypeError("Unsupported operation between IntVar and {}".format(other.__class__))

    def __pow__(self, power):
        if isinstance(power, int):
            if power <= 0:
                raise TypeError("Unsupported operation between IntVar and int <= 0")
            a = [self.get_lb() ** power, self.get_ub() ** power]
            res = self.model.intvar(min(a), max(a))
            self.model.pow(self, power, res).post()
            return res
        else:
            raise TypeError("Unsupported operation between IntVar and {}".format(power.__class__))

    def __mod__(self, other):
        if isinstance(other, IntVar):
            a = [self.get_lb() % other.get_lb(), self.get_lb() % other.get_ub(), self.get_ub() % other.get_lb(),
                 self.get_ub() % other.get_ub()]
            res = self.model.intvar(min(a), max(a))
            self.model.mod(self, other, res).post()
            return res
        elif isinstance(other, int):
            a = [self.get_lb() % other, self.get_ub() % other]
            res = self.model.intvar(min(a), max(a))
            self.model.mod(self, other, res).post()
            return res
        else:
            raise TypeError("Unsupported operation between IntVar and {}".format(other.__class__))

    def __eq__(self, other):
        if isinstance(other, IntVar):
            return self.model.arithm(self, "=", other).reify()
        elif isinstance(other, int):
            return self.model.int_eq_view(self, other)
        else:
            raise TypeError("Unsupported operation between IntVar and {}".format(other.__class__))

    def __ne__(self, other):
        if isinstance(other, IntVar):
            return self.model.arithm(self, "!=", other).reify()
        elif isinstance(other, int):
            return self.model.int_ne_view(self, other)
        else:
            raise TypeError("Unsupported operation between IntVar and {}".format(other.__class__))

    def __le__(self, other):
        if isinstance(other, IntVar):
            return self.model.arithm(self, "<=", other).reify()
        elif isinstance(other, int):
            return self.model.int_le_view(self, other)
        else:
            raise TypeError("Unsupported operation between IntVar and {}".format(other.__class__))

    def __ge__(self, other):
        if isinstance(other, IntVar):
            return self.model.arithm(self, ">=", other).reify()
        elif isinstance(other, int):
            return self.model.int_ge_view(self, other)
        else:
            raise TypeError("Unsupported operation between IntVar and {}".format(other.__class__))

    def __lt__(self, other):
        if isinstance(other, IntVar):
            return self.model.arithm(self, "<", other).reify()
        elif isinstance(other, int):
            return self.model.int_le_view(self, other - 1)
        else:
            raise TypeError("Unsupported operation between IntVar and {}".format(other.__class__))

    def __gt__(self, other):
        if isinstance(other, IntVar):
            return self.model.arithm(self, ">", other).reify()
        elif isinstance(other, int):
            return self.model.int_ge_view(self, other + 1)
        else:
            raise TypeError("Unsupported operation between IntVar and {}".format(other.__class__))
