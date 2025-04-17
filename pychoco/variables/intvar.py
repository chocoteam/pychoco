from pychoco import backend
from pychoco._utils import get_int_array
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
        return backend.get_intvar_lb(self._handle)

    def get_ub(self):
        """
        :return: The upper bound of the variable.
        """
        return backend.get_intvar_ub(self._handle)

    def get_value(self):
        """
        :return: The value of the variable (only valid if it is instantiated).
        """
        assert self.is_instantiated(), "{} is not instantiated".format(self.name)
        return backend.get_intvar_value(self._handle)

    def has_enumerated_domain(self):
        """
        :return: True if the domain of this variable is enumerated.
        """
        return backend.has_enumerated_domain(self._handle)

    def get_domain_values(self):
        """
        :return The enumerated values of this variable's domain.
        """
        val_handle = backend.get_domain_values(self._handle)
        vals = get_int_array(val_handle)
        return vals

    def get_type(self):
        return "IntVar"

    def __repr__(self):
        if self.has_enumerated_domain():
            return super().__repr__() + " = {}".format(self.get_domain_values())
        else:
            return super().__repr__() + " = [{}, {}]".format(self.get_lb(), self.get_ub())

    def __abs__(self):
        return self.model.int_abs_view(self)

    def __add__(self, other):
        if isinstance(other, IntVar):
            res = self.model.intvar(self.get_lb() + other.get_lb(), self.get_ub() + other.get_ub())
            self.model.arithm(self, "+", other, "=", res).post()
            return res
        elif isinstance(other, int):
            return self.model.int_offset_view(self, other)
        else:
            raise NotImplementedError("Unsupported operation between IntVar and {}".format(other.__class__))

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, IntVar):
            res = self.model.intvar(self.get_lb() - other.get_ub(), self.get_ub() - other.get_lb())
            self.model.arithm(self, "-", other, "=", res).post()
            return res
        elif isinstance(other, int):
            return self.model.int_offset_view(self, -other)
        else:
            raise NotImplementedError("Unsupported operation between IntVar and {}".format(other.__class__))

    def __rsub__(self, other):
        return - self.__sub__(other)

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
            raise NotImplementedError("Unsupported operation between IntVar and {}".format(other.__class__))

    def __rmul__(self, other):
        return self.__mul__(other)

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
            raise NotImplementedError("Unsupported operation between IntVar and {}".format(other.__class__))

    def __pow__(self, power):
        if isinstance(power, int):
            if power <= 0:
                raise NotImplementedError("Unsupported operation between IntVar and int <= 0")
            a = [self.get_lb() ** power, self.get_ub() ** power]
            res = self.model.intvar(min(a), max(a))
            self.model.pow(self, power, res).post()
            return res
        else:
            raise NotImplementedError("Unsupported operation between IntVar and {}".format(power.__class__))

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
            raise NotImplementedError("Unsupported operation between IntVar and {}".format(other.__class__))

    def __eq__(self, other):
        if isinstance(other, IntVar):
            return self.model.arithm(self, "=", other).reify()
        elif isinstance(other, int):
            return self.model.int_eq_view(self, other)
        else:
            raise NotImplementedError("Unsupported operation between IntVar and {}".format(other.__class__))

    def __ne__(self, other):
        if isinstance(other, IntVar):
            return self.model.arithm(self, "!=", other).reify()
        elif isinstance(other, int):
            return self.model.int_ne_view(self, other)
        else:
            raise NotImplementedError("Unsupported operation between IntVar and {}".format(other.__class__))

    def __le__(self, other):
        if isinstance(other, IntVar):
            return self.model.arithm(self, "<=", other).reify()
        elif isinstance(other, int):
            return self.model.int_le_view(self, other)
        else:
            raise NotImplementedError("Unsupported operation between IntVar and {}".format(other.__class__))

    def __ge__(self, other):
        if isinstance(other, IntVar):
            return self.model.arithm(self, ">=", other).reify()
        elif isinstance(other, int):
            return self.model.int_ge_view(self, other)
        else:
            raise NotImplementedError("Unsupported operation between IntVar and {}".format(other.__class__))

    def __lt__(self, other):
        if isinstance(other, IntVar):
            return self.model.arithm(self, "<", other).reify()
        elif isinstance(other, int):
            return self.model.int_le_view(self, other - 1)
        else:
            raise NotImplementedError("Unsupported operation between IntVar and {}".format(other.__class__))

    def __gt__(self, other):
        if isinstance(other, IntVar):
            return self.model.arithm(self, ">", other).reify()
        elif isinstance(other, int):
            return self.model.int_ge_view(self, other + 1)
        else:
            raise NotImplementedError("Unsupported operation between IntVar and {}".format(other.__class__))
