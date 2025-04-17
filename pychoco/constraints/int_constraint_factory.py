from abc import ABC, abstractmethod
from typing import Union, List

from pychoco import backend
from pychoco._utils import make_int_array, make_intvar_array, make_int_2d_array, make_boolvar_array, \
    make_constraint_array, make_task_array, make_intvar_2d_array, make_supportable_2d_array
from pychoco.constraints.constraint import Constraint
from pychoco.constraints.extension.hybrid.supportable import Supportable
from pychoco.objects.automaton.cost_automaton import CostAutomaton
from pychoco.objects.automaton.finite_automaton import FiniteAutomaton
from pychoco.objects.graphs.multivalued_decision_diagram import MultivaluedDecisionDiagram
from pychoco.variables.boolvar import BoolVar
from pychoco.variables.intvar import IntVar
from pychoco.variables.task import Task


class IntConstraintFactory(ABC):
    """
    Constraints over integer and boolean variables.
    """

    @property
    @abstractmethod
    def _handle(self):
        pass

    def arithm(self, x: IntVar, op1: str, y: Union[int, IntVar],
               op2: Union[None, str] = None, z: Union[None, int, IntVar] = None):
        """
        Creates an arithmetic constraint, where operators are in {"=", "!=", ">","<",">=","<="}
        and {"+", "-", "*", "/"}.

        Four options are possible:

        - `x <op1> y`,

            - x -> IntVar; y -> constant; op2 and z -> None.
            - op1 in {"=", "!=", ">","<",">=","<="}

        - `x <op1> y`,

            - x and y -> IntVar; operator3 and z -> None.
            - op1 in {"=", "!=", ">","<",">=","<="}

        - `x <op1> y <op2> z`,

            - x and y -> IntVar, z -> constant.
            - op1 in {"=", "!=", ">","<",">=","<="} and op2 in {"+", "-", "*", "/"}, or vice-versa.

        - `x <op1> y <op2> z`,

            - x, y, and z -> IntVar.
            - op1 in {"=", "!=", ">","<",">=","<="} and op2 in {"+", "-", "*", "/"}, or vice-versa.

        :param x: An IntVar object.
        :param op1: An str in {"=", "!=", ">","<",">=","<="} or {"+", "-", "*", "/"}.
        :param y: An IntVar object or a constant (integer).
        :param op2: An str in {"=", "!=", ">","<",">=","<="} or {"+", "-", "*", "/"}, or None.
        :param z: An IntVar object, a constant (integer), or None.
        :return: An arithmetic constraint.
        """
        constraint_handle = None
        eq_operators = ["=", "!=", ">", "<", ">=", "<="]
        alg_operators = ["+", "-", "*", "/"]
        if op2 is None:
            assert op1 in eq_operators
        else:
            assert (op1 in eq_operators and op2 in alg_operators) or (op1 in alg_operators and op2 in eq_operators)
        # Case 1
        if isinstance(y, int) and op2 is None and z is None:
            constraint_handle = backend.arithm_iv_cst(self._handle, x._handle, op1, y)
        if isinstance(y, int) and op2 is not None and z is not None:
            yy = self.intvar(y)
            if isinstance(z, int):
                constraint_handle = backend.arithm_iv_iv_cst(self._handle, x._handle, op1, yy._handle, op2, z)
            else:
                constraint_handle = backend.arithm_iv_iv_iv(self._handle, x._handle, op1, yy._handle, op2, z._handle)
        if isinstance(y, IntVar) and op2 is None and z is None:
            constraint_handle = backend.arithm_iv_iv(self._handle, x._handle, op1, y._handle)
        if isinstance(y, IntVar) and op2 is not None and isinstance(z, int):
            constraint_handle = backend.arithm_iv_iv_cst(self._handle, x._handle, op1, y._handle, op2, z)
        if isinstance(y, IntVar) and op2 is not None and isinstance(z, IntVar):
            constraint_handle = backend.arithm_iv_iv_iv(self._handle, x._handle, op1, y._handle, op2, z._handle)
        if constraint_handle is None:
            raise AttributeError("Invalid parameters combination for arithm constraint. Please refer to the doc")
        return Constraint(constraint_handle, self)

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
        if table is not None:
            ints_array = make_int_array(table)
            constraint_handle = backend.member_iv_iarray(self._handle, x._handle, ints_array)
        else:
            constraint_handle = backend.member_iv_i_i(self._handle, x._handle, lb, ub)
        return Constraint(constraint_handle, self)

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
        if table is not None:
            ints_array = make_int_array(table)
            constraint_handle = backend.not_member_iv_iarray(self._handle, x._handle, ints_array)
        else:
            constraint_handle = backend.not_member_iv_i_i(self._handle, x._handle, lb, ub)
        return Constraint(constraint_handle, self)

    def all_different(self, intvars: List[IntVar]):
        """
        Creates an allDifferent constraint, which ensures that all variables from vars take a different value.

        :param intvars: A list of integer variables.
        :return: An allDifferent constraint.
        """
        vars_array = make_intvar_array(intvars)
        constraint_handle = backend.all_different(self._handle, vars_array)
        return Constraint(constraint_handle, self)

    def all_different_except_0(self, intvars: List[IntVar]):
        """
        Creates an allDifferent constraint for variables that are not equal to 0.
        There can be multiple variables equal to 0.

        :param intvars: A list of integer variables.
        :return: An allDifferent constraint.
        """
        vars_array = make_intvar_array(intvars)
        constraint_handle = backend.all_different_except_0(self._handle, vars_array)
        return Constraint(constraint_handle, self)

    def all_different_prec(self, intvars: List[IntVar], predecessors: List[List[int]], successors: List[List[int]]):
        """
        Creates an AllDiffPrec constraint. The predecessors and successors matrix are built as following:
        with n = | variables | , for all i in [0, n-1], if there is k such that predecessors[i][k] = j then variables[j]
        is a predecessor of variables[i]. Similarly, with n = | variables | , for all i in [0, n-1], if there is k such
        that successors[i][k] = j then variables[j] is a successor of variables[i]. The matrix should be built such
        that, if variables[i] is a predecessor of variables[j], then i is in successors[j] and vice versa.

        :param intvars: A list of integer variables.
        :param predecessors: predecessors matrix.
        :param successors: successors matrix.
        :return: An allDifferent constraint.
        """
        intvars_handle = make_intvar_array(intvars)
        predHandle = make_int_2d_array(predecessors)
        succHandle = make_int_2d_array(successors)
        constraint_handle = backend.all_different_prec_pred_succ(self._handle, intvars_handle, predHandle, succHandle)
        return Constraint(constraint_handle, self)

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
        constraint_handle = None
        if isinstance(mod, int) and isinstance(res, int):
            constraint_handle = backend.mod_iv_i_i(self._handle, x._handle, mod, res)
        if isinstance(mod, int) and isinstance(res, IntVar):
            constraint_handle = backend.mod_iv_i_iv(self._handle, x._handle, mod, res._handle)
        if isinstance(mod, IntVar) and isinstance(res, IntVar):
            constraint_handle = backend.mod_iv_iv_iv(self._handle, x._handle, mod._handle, res._handle)
        return Constraint(constraint_handle, self)

    def not_(self, constraint: Constraint):
        """
        Gets the opposite of a given constraint.
        Works for any constraint, including globals, but the associated performances might be weak.

        :param constraint: A constraint.
        :return: A not constraint.
        """
        constraint_handle = backend.not_(self._handle, constraint._handle)
        return Constraint(constraint_handle, self)

    def absolute(self, x: IntVar, y: IntVar):
        """
        Creates an absolute value constraint: x = | y | .

        :param x: An IntVar.
        :param y: An IntVar.
        :return: An absolute constraint.
        """
        constraint_handle = backend.absolute(self._handle, x._handle, y._handle)
        return Constraint(constraint_handle, self)

    def distance(self, x: IntVar, y: IntVar, op: str, z: Union[int, IntVar]):
        """
        Creates a distance constraint : | x - y | op z, where op can take its value among:

            - {"=", ">", "<", "!="} if z is a constant
            - {"=", ">", "<"} if z is an IntVar

        :param x: An IntVar.
        :param y: An IntVar.
        :param op: An operator (str), which can take its value among {"=", ">", "<", "!="} if z is a constant or
            {"=", ">", "<"} if z is an IntVar.
        :param z: An IntVar or a constant (int).
        :return: A distance constraint.
        """
        if isinstance(z, IntVar):
            assert op in {"=", ">", "<"}, "[distance] op must be in ['=', '>', '<']"
        else:
            assert op in {"=", "!=", ">", "<"}, "[distance] op must be in ['=', '!=', '>', '<']"
        if isinstance(z, int):
            constraint_handle = backend.distance_iv_iv_i(self._handle, x._handle, y._handle, op, z)
        else:
            constraint_handle = backend.distance_iv_iv_iv(self._handle, x._handle, y._handle, op, z._handle)
        return Constraint(constraint_handle, self)

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
        if len(table) == 0:
            raise AttributeError("table parameter in element constraint must have a length > 0")
        if isinstance(table[0], int):
            ints_array_handle = make_int_array(table)
            constraint_handle = backend.element_iv_iarray_iv_i(self._handle, x._handle, ints_array_handle,
                                                               index._handle, offset)
        else:
            int_var_array_handle = make_intvar_array(table)
            constraint_handle = backend.element_iv_ivarray_iv_i(self._handle, x._handle, int_var_array_handle,
                                                                index._handle, offset)
        return Constraint(constraint_handle, self)

    def square(self, x: IntVar, y: IntVar):
        """
        Creates a square constraint: x = y^2.

        :param x: An IntVar.
        :param y: An IntVar.
        :return: A square constraint.
        """
        constraint_handle = backend.square(self._handle, x._handle, y._handle)
        return Constraint(constraint_handle, self)

    def table(self, intvars: List[IntVar], tuples: List[List[int]], feasible: bool = True, algo: str = "GAC3rm",
              universal_value: Union[None, int] = None):
        """
        Creates a table constraint, with the specified algorithm defined algo
        - CT+: Compact-Table algorithm (AC),
        - GAC2001: Arc Consistency version 2001 for tuples,
        - GAC2001+: Arc Consistency version 2001 for allowed tuples,
        - GAC3rm: Arc Consistency version AC3 rm for tuples,
        - GAC3rm+ (default): Arc Consistency version 3rm for allowed tuples,
        - GACSTR+: Arc Consistency version STR for allowed tuples,
        - STR2+: Arc Consistency version STR2 for allowed tuples,
        - FC: Forward Checking.
        - MDD+: uses a multi-valued decision diagram for allowed tuples (see mddc constraint).

        :param intvars: integer variables forming the tuples.
        :param tuples: the relation between the variables (list of allowed/forbidden tuples)
        :param feasible: if True, the tuples describe allowed tuples, otherwise forbidden tuples.
        :param algo: filtering algorithm, to choose among: "CT+", "GAC3rm", "GAC2001", "GACSTR", "GAC2001+", "GAC3rm+",
            "FC", "STR2+". Default is "GAC3rm".
        :param universal_value If not None, set an universal value to the tuples.
        :return: A table constraint.
        """
        assert algo in ["CT+", "GAC3rm", "GAC2001", "GACSTR", "GAC2001+", "GAC3rm+",
                        "FC", "STR2+"], '[table] algo must be in ["CT+", "GAC3rm", "GAC2001", "GACSTR", "GAC2001+", ' \
                                        '"GAC3rm+", "FC", "STR2+"]'
        vars_handle = make_intvar_array(intvars)
        tuples_handle = make_int_2d_array(tuples)
        if universal_value is None:
            constraint_handle = backend.table(self._handle, vars_handle, tuples_handle, feasible, algo)
        else:
            constraint_handle = backend.table_universal_value(self._handle, vars_handle, tuples_handle, feasible, algo, universal_value)
        return Constraint(constraint_handle, self)

    def hybrid_table(self, intvars: List[IntVar], hybrid_tuples: List[List[Supportable]]):
        """
        Create a table constraint based on hybrid tuples.
        Such tuples make possible to declare expressions as restriction on values a variable can take.

        :param intvars: scope of the constraint
        :param hybrid_tuples: hybrid tuples
        """
        vars_handle = make_intvar_array(intvars)
        tuples_handles = make_supportable_2d_array(hybrid_tuples)
        constraint_handle = backend.hybrid_table(self._handle, vars_handle, tuples_handles)
        return Constraint(constraint_handle, self)

    def times(self, x: IntVar, y: Union[int, IntVar], z: Union[int, IntVar]):
        """
        Creates a multiplication constraint: x * y = z.

        :param x: An IntVar.
        :param y: An IntVar or an int.
        :param z: An IntVar or an int.
        :return: A times constraint.
        """
        constraint_handle = None
        if isinstance(z, IntVar) and isinstance(y, int):
            constraint_handle = backend.times_iv_i_iv(self._handle, x._handle, y, z._handle)
        if isinstance(y, IntVar) and isinstance(z, int):
            constraint_handle = backend.times_iv_iv_i(self._handle, x._handle, y._handle, z)
        if isinstance(y, IntVar) and isinstance(z, IntVar):
            constraint_handle = backend.times_iv_iv_iv(self._handle, x._handle, y._handle, z._handle)
        return Constraint(constraint_handle, self)

    def pow(self, x: IntVar, c: int, y: IntVar):
        """
        Creates a power constraint: x^c = y

        :param x: An IntVar.
        :param c: An int.
        :param y: An IntVar.
        :return: A pow constraint.
        """
        constraint_handle = backend.pow_(self._handle, x._handle, c, y._handle)
        return Constraint(constraint_handle, self)

    def div(self, dividend: IntVar, divisor: IntVar, result: IntVar):
        """
        Creates a euclidean division constraint. Ensures dividend / divisor = result, rounding towards 0.
        Also ensures divisor != 0.

        :param dividend: An IntVar.
        :param divisor: An IntVar.
        :param result: An IntVar.
        :return: A div constraint.
        """
        constraint_handle = backend.div_(self._handle, dividend._handle, divisor._handle, result._handle)
        return Constraint(constraint_handle, self)

    def max(self, x: IntVar, intvars: List[IntVar]):
        """
        Creates a maximum constraint, x is the maximum value among IntVars in intvars.

        :param x: An IntVar.
        :param intvars: A list of IntVars.
        :return: A max constraint.
        """
        int_var_array_handle = make_intvar_array(intvars)
        constraint_hande = backend.max_iv_ivarray(self._handle, x._handle, int_var_array_handle)
        return Constraint(constraint_hande, self)

    def mddc(self, intvars: List[IntVar], mdd: MultivaluedDecisionDiagram):
        """
        Create a constraint where solutions (tuples) are encoded by a multi-valued decision diagram.
        The order of the variables in vars is important and must refer to the MDD.

        :param intvars: A list of IntVars.
        :param mdd: A MultiValuedDecisionDiagram object.
        :return: A mddc constraint.
        """
        intvars_handle = make_intvar_array(intvars)
        constraint_handle = backend.mddc(self._handle, intvars_handle, mdd._handle)
        return Constraint(constraint_handle, self)

    def min(self, x: IntVar, intvars: List[IntVar]):
        """
        Creates a minimum constraint, x is the minimum value among IntVars in intvars.

        :param x: An IntVar.
        :param intvars: A list of IntVars.
        :return: A min constraint.
        """
        int_var_array_handle = make_intvar_array(intvars)
        constraint_hande = backend.min_iv_ivarray(self._handle, x._handle, int_var_array_handle)
        return Constraint(constraint_hande, self)

    def multi_cost_regular(self, intvars: List[IntVar], costs: List[IntVar], cost_automaton: CostAutomaton):
        """
        Creates a regular constraint that supports a multiple cost function.
        Ensures that the assignment of a sequence of `intvars` is recognized by `cost_automaton`, a deterministic finite
        automaton, and that the sum of the cost vector associated to each assignment is bounded by the variable vector
        `costs`. This version allows to specify different costs according to the automaton state at which the
        assignment occurs (i.e. the transition starts).
        The precision is set to 1e-4.

        :param intvars: List of IntVars.
        :param costs: List of IntVars.
        :param cost_automaton: A cost automaton.
        :return: A multi_cost_regular constraint.
        """
        intvar_array_handle = make_intvar_array(intvars)
        costs_handle = make_intvar_array(costs)
        constraint_handle = backend.multi_cost_regular(self._handle, intvar_array_handle, costs_handle,
                                                       cost_automaton._handle)
        return Constraint(constraint_handle, self)

    def all_equal(self, intvars: List[IntVar]):
        """
        Creates an all_equal constraint.
        Ensures that all variables from vars take the same value.

        :param intvars: A list of IntVars.
        :return: An all_equal constraint.
        """
        vars_array = make_intvar_array(intvars)
        constraint_handle = backend.all_equal(self._handle, vars_array)
        return Constraint(constraint_handle, self)

    def not_all_equal(self, intvars: List[IntVar]):
        """
        Creates a not_all_equal constraint.
        Ensures that not all variables from vars take the same value.

        :param intvars: A list of IntVars.
        :return: A not_all_equal constraint.
        """
        vars_array = make_intvar_array(intvars)
        constraint_handle = backend.not_all_equal(self._handle, vars_array)
        return Constraint(constraint_handle, self)

    def among(self, nb_var: IntVar, intvars: List[IntVar], values: List[int]):
        """
        Creates an among constraint.
        `nb_var` is the number of variables of the collection `intvars` that take their value in `values`.

        Propagator :

            C. Bessiere, E. Hebrard, B. Hnich, Z. Kiziltan, T. Walsh, Among, common and disjoint Constraints CP-2005

        :param nb_var: An IntVar.
        :param intvars: A list of IntVars.
        :param values: A list of ints.
        :return: An among constraint.
        """
        vars_array = make_intvar_array(intvars)
        values_array = make_int_array(values)
        constraint_handle = backend.among(self._handle, nb_var._handle, vars_array, values_array)
        return Constraint(constraint_handle, self)

    def and_(self, bools_or_constraints: Union[List[BoolVar], List[Constraint]]):
        """
        Creates an and constraint that is satisfied if all boolean variables or constraint in
        `bools_or_constraints` are respectively true or satisfied.

        :param bools_or_constraints: Either a list of BoolVars or a list of Constraints.
        :return: An and constraint.
        """
        assert len(bools_or_constraints) >= 1, "[and_] bools_or_constraints must not be empty"
        if isinstance(bools_or_constraints[0], BoolVar):
            vars_array = make_boolvar_array(bools_or_constraints)
            constraint_handle = backend.and_bv_bv(self._handle, vars_array)
        else:
            cons_array = make_constraint_array(bools_or_constraints)
            constraint_handle = backend.and_cs_cs(self._handle, cons_array)
        return Constraint(constraint_handle, self)

    def at_least_n_values(self, intvars: List[IntVar], n_values: IntVar, ac: bool = False):
        """
        Creates an at_least_n_value constraint.
        Let N be the number of distinct values assigned to the variables of the intvars collection.
        Enforce condition N >= n_values to hold.
        This embeds a light propagator by default.
        Additional filtering algorithms can be added.

        :param intvars: list of IntVars.
        :param n_values: IntVar (limit variable).
        :param ac: If True, add additional filtering algorithm, domain filtering algorithm derivated
            from (Soft) AllDifferent.
        :return: An at_least_n_values constraint.
        """
        vars_array = make_intvar_array(intvars)
        constraint_handle = backend.at_least_n_values(self._handle, vars_array, n_values._handle, ac)
        return Constraint(constraint_handle, self)

    def at_most_n_values(self, intvars: List[IntVar], n_values: IntVar, strong: bool = False):
        """
        Creates an at_mostn_value constraint.
        Let N be the number of distinct values assigned to the variables of the intvars collection.
        Enforce condition N <= n_values to hold.
        This embeds a light propagator by default.
        Additional filtering algorithms can be added.

        :param intvars: list of IntVars.
        :param n_values: IntVar (limit variable).
        :param strong: "AMNV<Gci | MDRk | R13>" Filters the conjunction of AtMostNValue and inequalities
            (see Fages and Lap&egrave;gue Artificial Intelligence 2014)
            automatically detects inequalities and allDifferent constraints.
            Presumably useful when nValues must be minimized.
        :return: An at_most_n_values constraint.
        """
        vars_array = make_intvar_array(intvars)
        constraint_handle = backend.at_most_n_values(self._handle, vars_array, n_values._handle, strong)
        return Constraint(constraint_handle, self)

    def bin_packing(self, item_bin: List[IntVar], item_size: List[int], bin_load: List[IntVar], offset: int = 0):
        """
        Creates a bin_packing constraint.
        Bin Packing formulation:
        forall b in [0, bin_load.length - 1],
        bin_load[b] = sum(item_size[i] | i in [0,item_size.length-1], item_bin[i] = b + offset
        forall i in [0, item_size.length - 1], item_bin is in [offset, bin_load.length-1 + offset].

        :param item_bin: IntVars representing the bin of each item.
        :param item_size: ints representing the size of each item.
        :param bin_load: IntVars representing the load of each bin (i.e. the sum of the size of the items in it).
        :param offset: 0 by default but typically 1 if used within MiniZinc
            (which counts from 1 to n instead of from 0 to n-1)
        :return: A bin_packing constraint.
        """
        item_bin_handle = make_intvar_array(item_bin)
        item_size_handle = make_int_array(item_size)
        bin_load_handle = make_intvar_array(bin_load)
        constraint_handle = backend.bin_packing(self._handle, item_bin_handle, item_size_handle,
                                                bin_load_handle, offset)
        return Constraint(constraint_handle, self)

    def bools_int_channeling(self, boolvars: List[BoolVar], intvar: IntVar, offset: int = 0):
        """
        Creates a channeling constraint between an integer variable and a set of boolean variables.
        Maps the boolean assignments variables boolvars with the standard assignment variable intvar.

        intvar = i <-> boolvars[i - offset] = 1.

        :param boolvars: A list of BoolVars.
        :param intvar: An IntVar.
        :param offset: 0 by default but typically 1 if used within MiniZinc
            which counts from 1 to n instead of from 0 to n-1.
        :return: A bools_int_channeling constraint.
        """
        boolvars_handle = make_boolvar_array(boolvars)
        constraint_handle = backend.bools_int_channeling(self._handle, boolvars_handle, intvar._handle, offset)
        return Constraint(constraint_handle, self)

    def bits_int_channeling(self, bits: List[BoolVar], intvar: IntVar):
        """
        Creates a channeling constraint between an integer variable and a set of bit variables.
        Ensures that intvar = 2<sup>0</sup>*BIT_1 + 2<sup>1</sup>*BIT_2 + ... 2<sup>n-1</sup>*BIT_n.
        BIT_1 is related to the first bit of OCTET (2^0),
        BIT_2 is related to the first bit of OCTET (2^1), etc.
        The upper bound of intvar is given by 2<sup>n</sup>, where n is the size of the array bits.

        :param bits: A list of BoolVars.
        :param intvar: An IntVar.
        :return: A bits_int_channeling constraint.
        """
        bits_handle = make_boolvar_array(bits)
        constraint_handle = backend.bits_int_channeling(self._handle, bits_handle, intvar._handle)
        return Constraint(constraint_handle, self)

    def clauses_int_channeling(self, intvar: IntVar, e_vars: List[BoolVar], l_vars: List[BoolVar]):
        """
        Creates a channeling constraint between an integer variable and a set of clauses.
        Link each value from the domain of intvar to two boolean variable:
        one reifies the equality to the i^th value of the variable domain,
        the other reifies the less-or-equality to the i^th value of the variable domain.

        Contract: e_vars.lenght == l_vars.length == intvar.getUB() - intvar.getLB() + 1
        Contract: intvar is not a boolean variable.

        :param intvar: An IntVar.
        :param e_vars: A list of EQ BoolVars.
        :param l_vars: A list of LEQ BoolVars.
        :return: A clauses_int_channeling constraint.
        """
        assert len(e_vars) == len(l_vars) == abs(1 + intvar.get_ub() - intvar.get_lb()), \
            "[clauses_int_channeling] e_vars and l_vars must have the same length as intvar's domain size"
        assert not isinstance(intvar, BoolVar), "[clauses_int_channeling] intvar cannot be a BoolVar"
        e_vars_handle = make_boolvar_array(e_vars)
        l_vars_handle = make_boolvar_array(l_vars)
        constraint_handle = backend.clauses_int_channeling(self._handle, intvar._handle, e_vars_handle, l_vars_handle)
        return Constraint(constraint_handle, self)

    def circuit(self, intvars: List[IntVar], offset: int = 0, conf: str = "RD"):
        """
        Creates a circuit constraint which ensures that
        the elements of intvars define a covering circuit
        where intvars[i] = offset + j means that j is the successor of i.

        Filtering algorithms:

            - subtour elimination : Caseau & Laburthe (ICLP'97)
            - allDifferent GAC algorithm: R&eacute;gin (AAAI'94)
            - dominator-based filtering: Fages & Lorca (CP'11)
            - Strongly Connected Components based filtering (Cambazard & Bourreau JFPC'06 and Fages and Lorca TechReport'12)

        See Fages PhD Thesis (2014) for more information.

        :param intvars: A list of IntVars.
        :param offset: 0 by default but typically 1 if used within MiniZinc
            (which counts from 1 to n instead of from 0 to n-1).
        :param conf: Filtering options, among ["LIGHT", "FIRST", "RD", and "ALL"].
        :return: A circuit constraint.
        """
        intvars_handle = make_intvar_array(intvars)
        assert conf in ["LIGHT", "FIRST", "RD", "ALL"], "[circuit] conf must be in ['LIGHT', 'FIRST', 'RD', 'ALL']"
        constraint_handle = backend.circuit(self._handle, intvars_handle, offset, conf)
        return Constraint(constraint_handle, self)

    def cost_regular(self, intvars: List[IntVar], cost: IntVar, cost_automaton: CostAutomaton):
        """
        Creates a regular constraint that supports a cost function.
        Ensures that the assignment of a sequence of variables is recognized by costAutomaton, a deterministic
        finite automaton, and that the sum of the costs associated to each assignment is bounded by the cost variable.
        This version allows to specify different costs according to the automaton state at which the assignment occurs
        (i.e. the transition starts).

        :param intvars: sequence of variables.
        :param cost: cost variable.
        :param cost_automaton: A deterministic finite automaton defining the regular language and the costs.
        :return: A cost_regular constraint.
        """
        intvars_handle = make_intvar_array(intvars)
        constraint_handle = backend.cost_regular(self._handle, intvars_handle, cost._handle, cost_automaton._handle)
        return Constraint(constraint_handle, self)

    def count(self, value: Union[int, IntVar], intvars: List[IntVar], limit: IntVar):
        """
        Creates a count constraint.
        Let N be the number of variables of the intvars collection assigned to value `value`;
        Enforce condition N = limit to hold.

        :param value: An int.
        :param intvars: A list of IntVars.
        :param limit: An int or an IntVar.
        :return: A count constraint.
        """
        intvars_handle = make_intvar_array(intvars)
        if isinstance(value, int):
            constraint_handle = backend.count_i(self._handle, value, intvars_handle, limit._handle)
        else:
            constraint_handle = backend.count_iv(self._handle, value._handle, intvars_handle, limit._handle)
        return Constraint(constraint_handle, self)

    def cumulative(self, tasks: List[Task], heights: List[IntVar], capacity: IntVar, incremental: bool = True):
        """
        Creates a cumulative constraint: Enforces that at each point in time,
        the cumulated height of the set of tasks that overlap that point
        does not exceed a given limit.

        Task duration and height should be >= 0
        Discards tasks whose duration or height is equal to zero

        :param tasks: Task objects containing start, duration and end variables.
        :param heights: Integer variables representing the resource consumption of each task.
        :param capacity: Integer variable representing the resource capacity.
        :param incremental: Specifies if an incremental propagation should be applied (True by default).
        :return: A cumulative constraint.
        """
        tasks_handle = make_task_array(tasks)
        vars_handle = make_intvar_array(heights)
        constraint_handle = backend.cumulative(self._handle, tasks_handle, vars_handle, capacity._handle, incremental)
        return Constraint(constraint_handle, self)

    def diff_n(self, x: List[IntVar], y: List[IntVar], width: List[IntVar], height: List[IntVar],
               add_cumulative_reasoning: bool = True):
        """
        Creates a diff_n constraint. Constrains each rectangle<sub>i</sub>, given by their origins x<sub>i</sub>,y<sub>i</sub>
        and sizes width<sub>i</sub>,height<sub>i</sub>, to be non-overlapping.

        :param x: A list of IntVars.
        :param y: A list of IntVars.
        :param width: A list of IntVars.
        :param height: A list of IntVars.
        :param add_cumulative_reasoning: Indicates whether redundant cumulative constraints should be put
            on each dimension or not (advised).
        :return: A diff_n constraint.
        """
        x_handle = make_intvar_array(x)
        y_handle = make_intvar_array(y)
        width_handle = make_intvar_array(width)
        height_handle = make_intvar_array(height)
        constraint_handle = backend.diff_n(self._handle, x_handle, y_handle, width_handle, height_handle,
                                           add_cumulative_reasoning)
        return Constraint(constraint_handle, self)

    def decreasing(self, intvars: List[IntVar], delta: int = 0):
        """
        Create a decreasing constraint which ensures that the variables in intvars are decreasing.
        The delta parameter make possible to adjust bounds.
        That is: (X_0 >= X_1 +delta) and (X_1 >= X_2 + delta) and ...

        :param intvars: A list of IntVars.
        :param delta: An int.
        :return: A decreasing constraint.
        """
        intvars_handle = make_intvar_array(intvars)
        constraint_handle = backend.decreasing(self._handle, intvars_handle, delta)
        return Constraint(constraint_handle, self)

    def increasing(self, intvars: List[IntVar], delta: int = 0):
        """
        Create an increasing constraint which ensures that the variables in intvars are increasing.
        The delta parameter make possible to adjust bounds.
        That is: (X_0 <= X_1 +delta) and (X_1 <= X_2 + delta) and ...

        :param intvars: A list of IntVars.
        :param delta: An int.
        :return: An increasing constraint.
        """
        intvars_handle = make_intvar_array(intvars)
        constraint_handle = backend.increasing(self._handle, intvars_handle, delta)
        return Constraint(constraint_handle, self)

    def global_cardinality(self, intvars: List[IntVar], values: List[int], occurrences: List[IntVar],
                           closed: bool = False):
        """
        Creates a global cardinality constraint (GCC):
        Each value values[i] should be taken by exactly occurrences[i] variables of intvars.
        This constraint does not ensure any well-defined level of consistency, yet.

        :param intvars: A list of IntVars.
        :param values: A list of ints.
        :param occurrences: A list of IntVars.
        :param closed: If True, restricts domains of intvars to values.
        :return: A global_cardinality constraint.
        """
        intvars_handle = make_intvar_array(intvars)
        values_handle = make_int_array(values)
        occurrences_handle = make_intvar_array(occurrences)
        constraint_handle = backend.global_cardinality(self._handle, intvars_handle, values_handle, occurrences_handle,
                                                       closed)
        return Constraint(constraint_handle, self)

    def inverse_channeling(self, intvars1: List[IntVar], intvars2: List[IntVar], offset1: int = 0,
                           offset2: int = 0, ac: bool = False):
        """
        Creates an inverse channeling between vars1 and vars2:
        intvars1[i - offset2] = j <=> intvars2[j - offset1] = i
        Performs AC if domains are enumerated.
        If not, then it works on bounds without guaranteeing BC.
        (enumerated domains are strongly recommended).
        beware you should have | intvars1 | = | intvars2 | .

        :param intvars1: A list of IntVars.
        :param intvars2: A list of IntVars.
        :param offset1: an int.
        :param offset2: an int.
        :param ac: A bool.
        :return: An inverse_channeling constraint.
        """
        intvars1_handle = make_intvar_array(intvars1)
        intvars2_handle = make_intvar_array(intvars2)
        constraint_handle = backend.inverse_channeling(self._handle, intvars1_handle, intvars2_handle,
                                                       offset1, offset2, ac)
        return Constraint(constraint_handle, self)

    def int_value_precede_chain(self, intvars: List[IntVar], values: List[int]):
        """
        Creates an int_value_precede_chain constraint.
        Ensure that, for each pair of values[k] and values[l], such that k < l,
        if there exists j such that intvars[j] = intvars[l], then, there must exist
        i < j such that intvars[i] = intvars[k].

        :param intvars: A list of IntVars.
        :param values: A list of distinct ints.
        :return: An int_value_precede_chain constraint.
        """
        intvars_handle = make_intvar_array(intvars)
        values_handle = make_int_array(values)
        constraint_handle = backend.int_value_precede_chain(self._handle, intvars_handle, values_handle)
        return Constraint(constraint_handle, self)

    def keysort(self, intvars: List[List[IntVar]], permutation_intvars: Union[List[IntVar], None],
                sorted_intvars: List[List[IntVar]], k: int):
        """
        Creates a keySort constraint which ensures that the variables of `sorted_intvars` correspond to the variables
        of `intvars` according to a permutation stored in `permutation_variables` (optional, can be null).
        The variables of `sorted_intvars` are also sorted in increasing order wrt to `k`-size tuples.
        The sort is stable, that is, ties are broken using the position of the tuple in vars.

        :param intvars: A list of list of Intvars.
        :param permutation_intvars: List of permutation variables, domains should be [1, len(intvars)] -- Can be null
        :param sorted_intvars: List of array of variables sorted in increasing order.
        :param k: key prefix size (0 <= k <= m, where m is the size of intvars).
        :return: A keysort constraint.
        """
        intvars_handle = make_intvar_2d_array(intvars)
        permutation_intvars_handle = None
        if permutation_intvars is not None:
            permutation_intvars_handle = make_intvar_array(permutation_intvars)
        sorted_intvars_handle = make_intvar_2d_array(sorted_intvars)
        constraint_handle = backend.keysort(self._handle, intvars_handle, permutation_intvars_handle,
                                            sorted_intvars_handle, k)
        return Constraint(constraint_handle, self)

    def knapsack(self, occurrences: List[IntVar], weight_sum: IntVar, energy_sum: IntVar, weight: List[int],
                 energy: List[int]):
        """
        Creates a knapsack constraint.

        Ensures that :

            - occurrences[i] * weight[i] = weight_sum
            - occurrences[i] * energy[i] = energy_sum
            - and maximizing the value of energy_sum.

        A knapsack constraint <a href="http://en.wikipedia.org/wiki/Knapsack_problem">wikipedia</a>:<br/>

        "Given a set of items, each with a weight and an energy value,
        determine the count of each item to include in a collection so that
        the total weight is less than or equal to a given limit and the total value is as large as possible.
        It derives its name from the problem faced by someone who is constrained by a fixed-size knapsack
        and must fill it with the most useful items."

        The limit over weightSum has to be specified either in its domain or with an additional constraint:

            model.arithm(weight_sum, "<=", limit).post()

        :param occurrences: A list of IntVars.
        :param weight_sum: An IntVar.
        :param energy_sum: An IntVar.
        :param weight: A list of ints.
        :param energy: A list of ints.
        :return: A knapsack constraint.
        """
        occ_handle = make_intvar_array(occurrences)
        weight_handle = make_int_array(weight)
        energy_handle = make_int_array(energy)
        constraint_handle = backend.knapsack(self._handle, occ_handle, weight_sum._handle, energy_sum._handle,
                                             weight_handle, energy_handle)
        return Constraint(constraint_handle, self)

    def lex_chain_less(self, *intvars: List[IntVar]):
        """
        Creates a lex_chain_less constraint.
        For each pair of consecutive vectors intvars<sub>i</sub> and intvars<sub>i+1</sub> of the intvars collection
        intvars<sub>i</sub> is lexicographically strictly less than intvars<sub>i+1</sub>

        :param intvars: A 2D list of IntVars.
        :return: A lex_chain_less constraint.
        """
        if len(intvars) == 1 and isinstance(intvars[0], list):
            vars = intvars[0]
        else:
            vars = intvars
        intvars_handle = make_intvar_2d_array(vars)
        constraint_handle = backend.lex_chain_less(self._handle, intvars_handle)
        return Constraint(constraint_handle, self)

    def lex_chain_less_eq(self, *intvars: List[IntVar]):
        """
        Creates a lex_chain_less_eq constraint.
        For each pair of consecutive vectors intvars<sub>i</sub> and intvars<sub>i+1</sub> of the intvars collection
        intvars<sub>i</sub> is lexicographically less or equal than intvars<sub>i+1</sub>

        :param intvars: A 2D list of IntVars.
        :return: A lex_chain_less_eq constraint.
        """
        if len(intvars) == 1 and isinstance(intvars[0], list):
            vars = intvars[0]
        else:
            vars = intvars
        intvars_handle = make_intvar_2d_array(vars)
        constraint_handle = backend.lex_chain_less_eq(self._handle, intvars_handle)
        return Constraint(constraint_handle, self)

    def lex_less(self, intvars1: List[IntVar], intvars2: List[IntVar]):
        """
        Creates a lex_less constraint.
        Ensures that intvars1 is lexicographically strictly less than intvars2.

        :param intvars1: A list of IntVars.
        :param intvars2: A list of IntVars.
        :return: A lex_less constraint.
        """
        intvars_handle1 = make_intvar_array(intvars1)
        intvars_handle2 = make_intvar_array(intvars2)
        constraint_handle = backend.lex_less(self._handle, intvars_handle1, intvars_handle2)
        return Constraint(constraint_handle, self)

    def lex_less_eq(self, intvars1: List[IntVar], intvars2: List[IntVar]):
        """
        Creates a lex_less_eq constraint.
        Ensures that intvars1 is lexicographically strictly less or equal than intvars2.

        :param intvars1: A list of IntVars.
        :param intvars2: A list of IntVars.
        :return: A lex_less_eq constraint.
        """
        intvars_handle1 = make_intvar_array(intvars1)
        intvars_handle2 = make_intvar_array(intvars2)
        constraint_handle = backend.lex_less_eq(self._handle, intvars_handle1, intvars_handle2)
        return Constraint(constraint_handle, self)

    def argmax(self, intvar: IntVar, offset: int, intvars: List[IntVar]):
        """
        Creates an argmax constraint.
        intvar is the index of the maximum value of the collection of domain variables intvars.

        :param intvar: An IntVar.
        :param offset: an int.
        :param intvars: A list of IntVars.
        :return: An argmax constraint.
        """
        intvars_handle = make_intvar_array(intvars)
        constraint_handle = backend.argmax(self._handle, intvar._handle, offset, intvars_handle)
        return Constraint(constraint_handle, self)

    def argmin(self, intvar: IntVar, offset: int, intvars: List[IntVar]):
        """
        Creates an argmin constraint.
        intvar is the index of the minimum value of the collection of domain variables intvars.

        :param intvar: An IntVar.
        :param offset: an int.
        :param intvars: A list of IntVars.
        :return: An argmin constraint.
        """
        intvars_handle = make_intvar_array(intvars)
        constraint_handle = backend.argmin(self._handle, intvar._handle, offset, intvars_handle)
        return Constraint(constraint_handle, self)

    def n_values(self, intvars: List[IntVar], n_values: IntVar):
        """
        Creates an n_values constraint.
        Let N be the number of distinct values assigned to the variables of the intvars collection.
        Enforce condition N = n_values to hold.

        :param intvars: A list of IntVars.
        :param n_values: An IntVar.
        :return: An n_values constraint.
        """
        intvars_handle = make_intvar_array(intvars)
        constraint_handle = backend.n_values(self._handle, intvars_handle, n_values._handle)
        return Constraint(constraint_handle, self)

    def or_(self, bools_or_constraints: Union[List[BoolVar], List[Constraint]]):
        """
        Creates a or constraint that is satisfied if at least one boolean variable or constraint in
        `bools_or_constraints` is respectively true or satisfied.

        :param bools_or_constraints: Either a list of BoolVars or a list of Constraints.
        :return: An or constraint.
        """
        assert len(bools_or_constraints) >= 1, "[or_] bools_or_constraint must not be empty"
        if isinstance(bools_or_constraints[0], BoolVar):
            vars_array = make_boolvar_array(bools_or_constraints)
            constraint_handle = backend.or_bv_bv(self._handle, vars_array)
        else:
            cons_array = make_constraint_array(bools_or_constraints)
            constraint_handle = backend.or_cs_cs(self._handle, cons_array)
        return Constraint(constraint_handle, self)

    def path(self, intvars: List[IntVar], start: IntVar, end: IntVar, offset: int = 0):
        """
        Creates a path constraint which ensures that

            - the elements of intvars define a covering path from start to end
            - where intvars[i] = j means that j is the successor of i.
            - Moreover, intvars[end] = | intvars |
            - Requires : | intvars | > 0

        Filtering algorithms: see circuit constraint

        :param intvars: A list of IntVars.
        :param start: An IntVar.
        :param end: An IntVar.
        :param offset: An int.
        :return: A path constraint.
        """
        intvars_handle = make_intvar_array(intvars)
        constraint_handle = backend.path(self._handle, intvars_handle, start._handle, end._handle, offset)
        return Constraint(constraint_handle, self)

    def regular(self, intvars: List[IntVar], automaton: FiniteAutomaton):
        """
        Creates a regular constraint.
        Enforces the sequence of vars to be a word
        recognized by the deterministic finite automaton.
        For example regexp = "(1|2)(3*)(4|5)";
        The same dfa can be used for different propagators.

        :param intvars: IntVars.
        :param automaton: A finite automaton.
        :return: A regular constraint.
        """
        intvars_handle = make_intvar_array(intvars)
        constraint_handle = backend.regular(self._handle, intvars_handle, automaton._handle)
        return Constraint(constraint_handle, self)

    def scalar(self, intvars: List[IntVar], coeffs: List[int], operator: str, scalar: Union[int, IntVar]):
        """
        Creates a scalar constraint which ensures that Sum(intvars[i] * coeffs[i]) operator scalar.

        :param intvars: A list of IntVars.
        :param coeffs: A list of ints, such that | intvars | = | coeffs | .
        :param operator: A str in ["=", "!=", ">","<",">=","<="].
        :param scalar: An int or an IntVar.
        :return: A scalar constraint.
        """
        assert len(intvars) == len(coeffs), "[scalar] intvars and coeffs must have the same length"
        assert operator in ["=", "!=", ">", "<", ">=",
                            "<="], "[scalar] operator must be in ['=', '!=', '>', '<', '>=', '<=']"
        intvars_handle = make_intvar_array(intvars)
        coeffs_handle = make_int_array(coeffs)
        if isinstance(scalar, IntVar):
            constraint_handle = backend.scalar_iv(self._handle, intvars_handle, coeffs_handle, operator, scalar._handle)
        else:
            constraint_handle = backend.scalar_i(self._handle, intvars_handle, coeffs_handle, operator, scalar)
        return Constraint(constraint_handle, self)

    def sort(self, intvars: List[IntVar], sorted_intvars: List[IntVar]):
        """
        Creates a sort constraint which ensures that the variables of sorted_intvars correspond to the variables
        of intvars according to a permutation. The variables of sorted_intvars are also sorted in increasing order.

        For example:

            - X= (4,2,1,3)
            - Y= (1,2,3,4)

        :param intvars: A list of IntVars.
        :param sorted_intvars: A list of IntVars.
        :return: A sort constraint.
        """
        intvars_handle = make_intvar_array(intvars)
        sorted_intvars_handle = make_intvar_array(sorted_intvars)
        constraint_handle = backend.sort(self._handle, intvars_handle, sorted_intvars_handle)
        return Constraint(constraint_handle, self)

    def sub_circuit(self, intvars: List[IntVar], offset: int, sub_circuit_length: IntVar):
        """
        Creates a sub_circuit constraint which ensures that:

            - the elements of intvars define a single circuit of sub_circuit_length nodes where
            - intvars[i] = offset + j means that j is the successor of i.
            - and intvars[i] = offset + i means that i is not part of the circuit

        the constraint ensures that | {intvars[i] =/= offset + i} | = sub_circuit_length

        Filtering algorithms:

            - subtour elimination : Caseau & Laburthe (ICLP'97)
            - allDifferent GAC algorithm: R&eacute;gin (AAAI'94)
            - dominator-based filtering: Fages & Lorca (CP'11) (adaptive scheme by default, see implementation)

        :param intvars: A list of IntVars.
        :param offset: An int.
        :param sub_circuit_length: An IntVar.
        :return: A sub_circuit constraint.
        """
        intvars_handle = make_intvar_array(intvars)
        constraint_handle = backend.sub_circuit(self._handle, intvars_handle, offset, sub_circuit_length._handle)
        return Constraint(constraint_handle, self)

    def sub_path(self, intvars: List[IntVar], start: IntVar, end: IntVar, offset: int, sub_path_length: IntVar):
        """
        Creates a sub_path constraint which ensures that:

            - the elements of intvars define a path of sub_path_length vertices, leading from start to end
            - where intvars[i] = offset + j means that j is the successor of i.
            - where intvars[i] = offset + i means that vertex i is excluded from the path.
            - Moreover, intvars[end - offset] = | intvars | + offset

        Requires : | intvars | > 0

        Filtering algorithms: see subCircuit constraint

        :param intvars: A list of IntVars.
        :param start: An IntVar.
        :param end: An IntVar.
        :param offset: An int.
        :param sub_path_length: An IntVar.
        :return: A sub_path constraint.
        """
        assert len(intvars) > 0, "[sub_path] intvars must not be empty"
        intvars_handle = make_intvar_array(intvars)
        constraint_handle = backend.sub_path(self._handle, intvars_handle, start._handle, end._handle, offset,
                                             sub_path_length._handle)
        return Constraint(constraint_handle, self)

    def sum(self, intvars_or_boolvars: Union[List[IntVar], List[BoolVar]], operator: str,
            sum_result: Union[int, IntVar, List[IntVar]]):
        """
        Creates a sum constraint.
        Enforces that Sum<sub>i in | intvars_or_boolvars | </sub>intvars_or_boolvars<sub>i</sub> operator sum_result.

        :param intvars_or_boolvars: Either a list of IntVars or a list of BoolVars.
        :param operator: A str in ["=", "!=", ">","<",">=","<="].
        :param sum_result: Either an int, an IntVar, or a list of IntVars.
        :return: A sum constraint.
        """
        assert len(intvars_or_boolvars) > 0, "[sum] intvars_or_boolvars must not be empty"
        assert operator in ["=", "!=", ">", "<", ">=",
                            "<="], "[sum] operator must be in ['=', '!=', '>', '<', '>=', '<=']"
        if isinstance(intvars_or_boolvars[0], IntVar):
            vars_handle = make_intvar_array(intvars_or_boolvars)
            if isinstance(sum_result, int):
                constraint_handle = backend.sum_iv_i(self._handle, vars_handle, operator, sum_result)
            elif isinstance(sum_result, IntVar):
                constraint_handle = backend.sum_iv_iv(self._handle, vars_handle, operator, sum_result._handle)
            else:
                sum_result_handle = make_intvar_array(sum_result)
                constraint_handle = backend.sum_ivarray_ivarray(self._handle, vars_handle, operator, sum_result_handle)
        else:
            vars_handle = make_boolvar_array(intvars_or_boolvars)
            if isinstance(sum_result, int):
                constraint_handle = backend.sum_bv_i(self._handle, vars_handle, operator, sum_result)
            elif isinstance(sum_result, IntVar):
                constraint_handle = backend.sum_bv_iv(self._handle, vars_handle, operator, sum_result._handle)
            else:
                sum_result_handle = make_intvar_array(sum_result)
                constraint_handle = backend.sum_ivarray_ivarray(self._handle, vars_handle, operator, sum_result_handle)
        return Constraint(constraint_handle, self)

    def tree(self, successors: List[IntVar], nb_trees: IntVar, offset: int = 0):
        """
        Creates a tree constraint.
        Partition successors variables into nb_trees (anti) arborescence.

            - successors[i] = offset + j means that j is the successor of i.
            - and successors[i] = offset + i means that i is a root.

        Dominator-based filtering: Fages & Lorca (CP'11).
        However, the filtering over nbTrees is quite light here.

        :param successors: A list of IntVars.
        :param nb_trees: An IntVar.
        :param offset: An int.
        :return: A tree constraint.
        """
        successors_handle = make_intvar_array(successors)
        constraint_handle = backend.tree(self._handle, successors_handle, nb_trees._handle, offset)
        return Constraint(constraint_handle, self)
