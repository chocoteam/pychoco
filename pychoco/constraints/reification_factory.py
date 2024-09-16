
from abc import ABC, abstractmethod
from typing import Union, List

from pychoco._utils import make_int_array
from pychoco.constraints.constraint import Constraint
from pychoco import backend
from pychoco.variables.boolvar import BoolVar
from pychoco.variables.intvar import IntVar


class ReificationFactory(ABC):
    """
    Reification of constraints
    """

    @property
    @abstractmethod
    def handle(self):
        pass

    def if_then_else(self, if_constraint_or_boolvar: Union[Constraint, BoolVar], then_constraint: Constraint,
                     else_constraint: Constraint):
        """
        Posts a constraint ensuring that if `if_constraint_or_boolvar`is satisfied (or true), then `then_constraint`
        must be satisfied as well. Otherwise, `else_constraint`must be satisfied.

        :param if_constraint_or_boolvar: A Constraint or a BoolVar.
        :param then_constraint: A Constraint.
        :param else_constraint: A Constraint.
        """
        if isinstance(if_constraint_or_boolvar, Constraint):
            backend.if_then_else(self.handle, if_constraint_or_boolvar.handle, then_constraint.handle, else_constraint.handle)
        else:
            backend.if_then_else_bool(self.handle, if_constraint_or_boolvar.handle, then_constraint.handle, else_constraint.handle)


    def if_then(self, if_constraint_or_boolvar: Union[Constraint, BoolVar], then_constraint: Constraint):
        """
        Creates an if-then constraint: if_constraint -> then_constraint.

        :param if_constraint_or_boolvar: A Constraint or a BoolVar.
        :param then_constraint: A Constraint.
        """
        if isinstance(if_constraint_or_boolvar, Constraint):
            backend.if_then(self.handle, if_constraint_or_boolvar.handle, then_constraint.handle)
        else:
            backend.if_then_bool(self.handle, if_constraint_or_boolvar.handle, then_constraint.handle)

    def if_only_if(self, constraint1_or_boolvar: Union[Constraint, BoolVar], constraint2: Constraint):
        """
        Posts an equivalence constraint stating that:
        `constraint1_or_boolvar` is satisfied (or true) <=> `constraint2` is satisfied.

        :param constraint1_or_boolvar: A Constraint or a BoolVar.
        :param constraint2: A Constraint.
        """
        if isinstance(constraint1_or_boolvar, Constraint):
            backend.if_only_if(self.handle, constraint1_or_boolvar.handle, constraint2.handle)
        else:
            backend.reification(self.handle, constraint1_or_boolvar.handle, constraint2.handle)

    def reify_x_eq_y(self, x: IntVar, y: Union[IntVar, int], b: BoolVar):
        """
        Posts a constraint that expresses: (x = y) <=> (b = true).

        :param x: An IntVar.
        :param y: An IntVar or an int.
        :param b: A BoolVar.
        """
        if isinstance(y, IntVar):
            backend.reify_x_eq_y(self.handle, x.handle, y.handle, b.handle)
        else:
            backend.reify_x_eq_c(self.handle, x.handle, y, b.handle)

    def reify_x_ne_y(self, x: IntVar, y: Union[IntVar, int], b: BoolVar):
        """
        Posts a constraint that expresses: (x != y) <=> (b is true).

        :param x: An IntVar.
        :param y: An IntVar or an int.
        :param b: A BoolVar.
        """
        if isinstance(y, IntVar):
            backend.reify_x_ne_y(self.handle, x.handle, y.handle, b.handle)
        else:
            backend.reify_x_ne_c(self.handle, x.handle, y, b.handle)

    def reify_x_eq_yc(self, x: IntVar, y: IntVar, c: int, b: BoolVar):
        """
        Posts a constraint that expresses : (x = y + c) <=> (b is true).

        :param x : An IntVar.
        :param y: An IntVar.
        :param c: An int.
        :param b: A BoolVar.
        """
        backend.reify_x_eq_yc(self.handle, x.handle, y.handle, c, b.handle)

    def reify_x_ne_yc(self, x: IntVar, y: IntVar, c: int, b: BoolVar):
        """
        Posts a constraint that expresses : (x != y + c) <=> (b is true).

        :param x : An IntVar.
        :param y: An IntVar.
        :param c: An int.
        :param b: A BoolVar.
        """
        backend.reify_x_ne_yc(self.handle, x.handle, y.handle, c, b.handle)

    def reify_x_lt_y(self, x: IntVar, y: Union[IntVar, int], b: BoolVar):
        """
        Posts a constraint that expresses: (x < y) <=> (b = true).

        :param x: An IntVar.
        :param y: An IntVar or an int.
        :param b: A BoolVar.
        """
        if isinstance(y, IntVar):
            backend.reify_x_lt_y(self.handle, x.handle, y.handle, b.handle)
        else:
            backend.reify_x_lt_c(self.handle, x.handle, y, b.handle)

    def reify_x_gt_y(self, x: IntVar, y: Union[IntVar, int], b: BoolVar):
        """
        Posts a constraint that expresses: (x > y) <=> (b = true).

        :param x: An IntVar.
        :param y: An IntVar or an int.
        :param b: A BoolVar.
        """
        if isinstance(y, IntVar):
            backend.reify_x_gt_y(self.handle, x.handle, y.handle, b.handle)
        else:
            backend.reify_x_gt_c(self.handle, x.handle, y, b.handle)

    def reify_x_le_y(self, x: IntVar, y: Union[IntVar, int], b: BoolVar):
        """
        Posts a constraint that expresses: (x <= y) <=> (b = true).

        :param x: An IntVar.
        :param y: An IntVar or an int.
        :param b: A BoolVar.
        """
        if isinstance(y, IntVar):
            backend.reify_x_le_y(self.handle, x.handle, y.handle, b.handle)
        else:
            backend.reify_x_lt_c(self.handle, x.handle, y + 1, b.handle)

    def reify_x_ge_y(self, x: IntVar, y: Union[IntVar, int], b: BoolVar):
        """
        Posts a constraint that expresses: (x >= y) <=> (b = true).

        :param x: An IntVar.
        :param y: An IntVar or an int.
        :param b: A BoolVar.
        """
        if isinstance(y, IntVar):
            backend.reify_x_ge_y(self.handle, x.handle, y.handle, b.handle)
        else:
            backend.reify_x_gt_c(self.handle, x.handle, y - 1, b.handle)

    def reify_x_lt_yc(self, x: IntVar, y: IntVar, c: int, b: BoolVar):
        """
        Posts a constraint that expresses : (x < y + c) <=> b.

        :param x: An IntVar.
        :param y: An IntVar.
        :param c: An int.
        :param b: A BoolVar.
        """
        backend.reify_x_lt_yc(self.handle, x.handle, y.handle, c, b.handle)

    def reify_x_gt_yc(self, x: IntVar, y: IntVar, c: int, b: BoolVar):
        """
        Posts a constraint that expresses : (x > y + c) <=> b.

        :param x: An IntVar.
        :param y: An IntVar.
        :param c: An int.
        :param b: A BoolVar.
        """
        backend.reify_x_gt_yc(self.handle, x.handle, y.handle, c, b.handle)

    def reify_x_in_s(self, x: IntVar, s: List[int], b: BoolVar):
        """
        Posts a constraint that expresses : (x in s) <=> B.

        :param x: An IntVar.
        :param s: A list of ints.
        :param b: A BoolVar.
        """
        shandle = make_int_array(s)
        backend.reify_x_in_s(self.handle, x.handle, shandle, b.handle)

    def reify_x_not_in_s(self, x: IntVar, s: List[int], b: BoolVar):
        """
        Posts a constraint that expresses : (x not in s) <=> B.

        :param x: An IntVar.
        :param s: A list of ints.
        :param b: A BoolVar.
        """
        shandle = make_int_array(s)
        backend.reify_x_not_in_s(self.handle, x.handle, shandle, b.handle)
