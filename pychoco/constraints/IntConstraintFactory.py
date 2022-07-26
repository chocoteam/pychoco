from abc import ABC, abstractmethod
from typing import Union, List

from pychoco.constraints.Constraint import Constraint
from pychoco.variables.IntVar import IntVar


class IntConstraintFactory(ABC):
    """
    Factory for constraints over integer variables.
    """

    @abstractmethod
    def arithm(self, x: IntVar, op1: str, y: Union[int, IntVar],
               op2: Union[None, str] = None, z: Union[None, int, IntVar] = None):
        """
        Creates an arithmetic constraint, where operators are in in {"=", "!=", ">","<",">=","<="}.
        Four options are possible:
            - `x <op1> y`,
                    x -> IntVar; y -> constant; op2 and z -> None.
            - `x <op1> y`,
                    x and y -> IntVar; operator3 and z -> None.
            - `x <op1> y <op2> z`,
                    x and y -> IntVar, z -> constant.
            - `x <op1> y <op2> z`,
                    x, y, and z -> IntVar.
        :param x: An IntVar object.
        :param op1: An str in {"=", "!=", ">","<",">=","<="}.
        :param y: An IntVar object or a constant (integer).
        :param op2: An str in {"=", "!=", ">","<",">=","<="}, or None.
        :param z: An IntVar object, a constant (integer), or None.
        :return: An arithmetic constraint.
        """
        pass

    @abstractmethod
    def member(self, x: IntVar, table: Union[list, tuple, None] = None,
               lb: Union[None, int] = None, ub: Union[None, int] = None):
        """
        Creates a member constraint. Ensures `x` takes its values in `table`, or in [`lb`, `ub`].
        If `table` is not `None`, the first option is applied, otherwise `lb` and `ub` must not be `None`.
        :param x: An `IntVar`.
        :param table: A list of integers, or `None`.
        :param lb: An integer, or `None`.
        :param ub: An integer, or `None`.
        :return: A member constraint.
        """
        pass

    @abstractmethod
    def not_member(self, x: IntVar, table: Union[list, tuple, None] = None,
                   lb: Union[None, int] = None, ub: Union[None, int] = None):
        """
        Creates a not_member constraint. Ensures `x` does not take its values in `table`, or in [`lb`, `ub`].
        If `table` is not `None`, the first option is applied, otherwise `lb` and `ub` must not be `None`.
        :param x: An `IntVar`.
        :param table: A list of integers, or `None`.
        :param lb: An integer, or `None`.
        :param ub: An integer, or `None`.
        :return: A not_member constraint.
        """
        pass

    @abstractmethod
    def all_different(self, *intvars: List[IntVar]):
        """
        Creates an allDifferent constraint, which ensures that all variables from vars take a different value.
        :param intvars: A list of integer variables.
        :return: An allDifferent constraint.
        """
        pass

    @abstractmethod
    def mod(self, x, mod: Union[int, IntVar], res: Union[int, IntVar]):
        """
        Creates a modulo constraint. Ensures X % mod = res.
        If mod is an `IntVar`, the constraint uses truncated division: the quotient is defined by truncation
        q = trunc(a/n) and the remainder would have same sign as the dividend. The quotient is rounded towards
        zero: equal to the first integer in the direction of zero from the exact rational quotient.
        :param x: An `IntVar`.
        :param mod: A constant (int), or an `IntVar`.
        :param res: A constant (int), or an `IntVar`.
        :return: A modulo constraint.
        """
        pass

    @abstractmethod
    def not_(self, constraint: Constraint):
        """
        Gets the opposite of a given constraint.
        Works for any constraint, including globals, but the associated performances might be weak.
        :param constraint: A constraint.
        :return: A not constraint.
        """
        pass

    @abstractmethod
    def absolute(self, x: IntVar, y: IntVar):
        """
        Creates an absolute value constraint: x = |y|.
        :param x: An IntVar.
        :param y: An IntVar.
        :return: An absolute constraint.
        """
        pass

    @abstractmethod
    def distance(self, x: IntVar, y: IntVar, op: str, z: Union[int, IntVar]):
        """
        Creates a distance constraint : |x-y| op z,
        where op can take its value among {"=", ">", "<", "!="}.
        :param x: An IntVar.
        :param y: An IntVar.
        :param op: An operator (str), which can take its value among {"=", ">", "<", "!="}.
        :param z: An IntVar or a constant (integer).
        :return: A distance constraint.
        """
        pass

    @abstractmethod
    def element(self, x: IntVar, table: Union[List[int], List[IntVar]], index: IntVar, offset: int = 0):
        """
        Creates an element constraint: x = table[index-offset]
        where table is a list of variables or integers.
        :param x: An IntVar.
        :param table: A list of IntVars or a list of integers.
        :param index: An IntVar.
        :param offset: An integer.
        :return: An element constraint.
        """
        pass

    @abstractmethod
    def square(self, x: IntVar, y: IntVar):
        """
        Creates a square constraint: x = y^2.
        :param x: An IntVar.
        :param y: An IntVar.
        :return: A square constraint.
        """
        pass

    @abstractmethod
    def times(self, x: IntVar, y: Union[int, IntVar], z: Union[int, IntVar]):
        """
        Creates a multiplication constraint: x * y = z.
        :param x: An IntVar.
        :param y: An IntVar or an int.
        :param z: An IntVar or an int.
        :return: A times constraint.
        """
        pass

    @abstractmethod
    def div(self, dividend: IntVar, divisor: IntVar, result: IntVar):
        """
        Creates a euclidean division constraint. Ensures dividend / divisor = result, rounding towards 0.
        Also ensures divisor != 0
        :param dividend: An IntVar.
        :param divisor: An IntVar.
        :param result: An IntVar.
        :return: A div constraint.
        """
        pass

    @abstractmethod
    def max(self, x: IntVar, *intvars: List[IntVar]):
        """
        Creates a maximum constraint, x is the maximum value among IntVars in *intvars.
        :param x: An IntVar.
        :param intvars: A list of IntVars.
        :return: A max constraint.
        """
        pass

    @abstractmethod
    def min(self, x: IntVar, *intvars: List[IntVar]):
        """
        Creates a minimum constraint, x is the minimum value among IntVars in *intvars.
        :param x: An IntVar.
        :param intvars: A list of IntVars.
        :return: A min constraint.
        """
        pass
