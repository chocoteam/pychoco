from abc import ABC, abstractmethod
from typing import List

from pychoco import backend
from pychoco._utils import make_constraint_array, make_boolvar_array
from pychoco.constraints.cnf.log_op import LogOp
from pychoco.constraints.constraint import Constraint
from pychoco.variables.boolvar import BoolVar


class SatFactory(ABC):
    """
    A Factory dedicated to SAT constraints
    """

    @property
    @abstractmethod
    def _handle(self):
        pass

    def add_clauses_logop(self, tree: LogOp):
        """
        Ensures that the clauses defined in the Boolean logic formula tree are satisfied.
        :param tree: A LogOp
        """
        return backend.add_clauses_logop(self._handle, tree._handle)

    def add_clauses(self, pos_lits: List[BoolVar], neg_lits: List[BoolVar]):
        """
        Ensures that the clause defined by pos_lits and neg_lits is satisfied.
        :param pos_lits: A list of BoolVars.
        :param neg_lits: A list of BoolVar.
        """
        poshandle = make_boolvar_array(pos_lits)
        neghandle = make_boolvar_array(neg_lits)
        return backend.add_clauses(self._handle, poshandle, neghandle)

    def add_clause_true(self, boolvar: BoolVar):
        """
        Add a unit clause stating that boolvar must be true
        :param boolvar: A BoolVar.
        """
        return backend.add_clause_true(self._handle, boolvar._handle)

    def add_clause_false(self, boolvar: BoolVar):
        """
        Add a unit clause stating that boolvar must be false
        :param boolvar: A BoolVar.
        """
        return backend.add_clause_false(self._handle, boolvar._handle)

    def add_clauses_bool_eq(self, left: BoolVar, right: BoolVar):
        """
        Add a clause stating that: LEFT == RIGHT.
        :param left: A BoolVar.
        :param right: A BoolVar.
        """
        return backend.add_clauses_bool_eq(self._handle, left._handle, right._handle)

    def add_clauses_bool_le(self, left: BoolVar, right: BoolVar):
        """
        Add a clause stating that: LEFT <= RIGHT.
        :param left: A BoolVar.
        :param right: A BoolVar.
        """
        return backend.add_clauses_bool_le(self._handle, left._handle, right._handle)

    def add_clauses_bool_lt(self, left: BoolVar, right: BoolVar):
        """
        Add a clause stating that: LEFT < RIGHT.
        :param left: A BoolVar.
        :param right: A BoolVar.
        """
        return backend.add_clauses_bool_lt(self._handle, left._handle, right._handle)

    def add_clauses_bool_not(self, left: BoolVar, right: BoolVar):
        """
        Add a clause stating that: LEFT != RIGHT.
        :param left: A BoolVar.
        :param right: A BoolVar.
        """
        return backend.add_clauses_bool_not(self._handle, left._handle, right._handle)

    def add_clauses_bool_or_array_eq_var(self, boolvars: List[BoolVar], target: BoolVar):
        """
        Add a clause stating that: boolvars_1 OR boolvars_2 OR ... OR boolvars_n <=> TARGET.
        :param boolvars: A list of BoolVars.
        :param target: A BoolVar.
        """
        lhandle = make_boolvar_array(boolvars)
        return backend.add_clauses_bool_or_array_eq_var(self._handle, lhandle, target._handle)

    def add_clauses_bool_and_array_eq_var(self, boolvars: List[BoolVar], target: BoolVar):
        """
        Add a clause stating that: boolvars_1 AND boolvars_2 AND ... AND boolvars_n <=> TARGET.
        :param boolvars: A list of BoolVars.
        :param target: A BoolVar.
        """
        lhandle = make_boolvar_array(boolvars)
        return backend.add_clauses_bool_and_array_eq_var(self._handle, lhandle, target._handle)

    def add_clauses_bool_or_eq_var(self, left: BoolVar, right: BoolVar, target: BoolVar):
        """
        Add a clause stating that: (LEFT OR RIGHT) <=> TARGET.
        :param left: A BoolVar.
        :param right: A BoolVar.
        :param target: A BoolVar.
        """
        return backend.add_clauses_bool_or_eq_var(self._handle, left._handle, right._handle, target._handle)

    def add_clauses_bool_and_eq_var(self, left: BoolVar, right: BoolVar, target: BoolVar):
        """
        Add a clause stating that: (LEFT AND RIGHT) <=> TARGET.
        :param left: A BoolVar.
        :param right: A BoolVar.
        :param target: A BoolVar.
        """
        return backend.add_clauses_bool_and_eq_var(self._handle, left._handle, right._handle, target._handle)

    def add_clauses_bool_xor_eq_var(self, left: BoolVar, right: BoolVar, target: BoolVar):
        """
        Add a clause stating that: (LEFT XOR RIGHT) <=> TARGET.
        :param left: A BoolVar.
        :param right: A BoolVar.
        :param target: A BoolVar.
        """
        return backend.add_clauses_bool_xor_eq_var(self._handle, left._handle, right._handle, target._handle)

    def add_clauses_bool_is_eq_var(self, left: BoolVar, right: BoolVar, target: BoolVar):
        """
        Add a clause stating that: (LEFT = RIGHT) <=> TARGET.
        :param left: A BoolVar.
        :param right: A BoolVar.
        :param target: A BoolVar.
        """
        return backend.add_clauses_bool_is_eq_var(self._handle, left._handle, right._handle, target._handle)

    def add_clauses_bool_is_neq_var(self, left: BoolVar, right: BoolVar, target: BoolVar):
        """
        Add a clause stating that: (LEFT != RIGHT) <=> TARGET.
        :param left: A BoolVar.
        :param right: A BoolVar.
        :param target: A BoolVar.
        """
        return backend.add_clauses_bool_is_neq_var(self._handle, left._handle, right._handle, target._handle)

    def add_clauses_bool_is_le_var(self, left: BoolVar, right: BoolVar, target: BoolVar):
        """
        Add a clause stating that: (LEFT <= RIGHT) <=> TARGET.
        :param left: A BoolVar.
        :param right: A BoolVar.
        :param target: A BoolVar.
        """
        return backend.add_clauses_bool_is_le_var(self._handle, left._handle, right._handle, target._handle)

    def add_clauses_bool_is_lt_var(self, left: BoolVar, right: BoolVar, target: BoolVar):
        """
        Add a clause stating that: (LEFT < RIGHT) <=> TARGET.
        :param left: A BoolVar.
        :param right: A BoolVar.
        :param target: A BoolVar.
        """
        return backend.add_clauses_bool_is_lt_var(self._handle, left._handle, right._handle, target._handle)

    def add_clauses_bool_or_array_equal_true(self, boolvars: List[BoolVar]):
        """
        Add a clause stating that: boolvars_1 OR boolvars_2 OR ... OR boolvars_n is TRUE
        :param boolvars: A list of BoolVars.
        """
        lhandle = make_boolvar_array(boolvars)
        return backend.add_clauses_bool_or_array_equal_true(self._handle, lhandle)

    def add_clauses_bool_and_array_equal_false(self, boolvars: List[BoolVar]):
        """
        Add a clause stating that: boolvars_1 AND boolvars_2 AND ... AND boolvars_n is FALSE
        :param boolvars: A list of BoolVars.
        """
        lhandle = make_boolvar_array(boolvars)
        return backend.add_clauses_bool_and_array_equal_false(self._handle, lhandle)

    def add_clauses_at_most_one(self, boolvars: List[BoolVar]):
        """
        Add a clause stating that: sum(boolvars) <= 1
        :param boolvars: A list of BoolVars.
        """
        lhandle = make_boolvar_array(boolvars)
        return backend.add_clauses_at_most_one(self._handle, lhandle)

    def add_clauses_at_most_n_minus_one(self, boolvars: List[BoolVar]):
        """
        Add a clause stating that: sum(boolvars) <= |boolvars|-1
        :param boolvars: A list of BoolVars.
        """
        lhandle = make_boolvar_array(boolvars)
        return backend.add_clauses_at_most_nminus_one(self._handle, lhandle)

    def add_clauses_sum_bool_array_greater_eq_var(self, boolvars: List[BoolVar], target: BoolVar):
        """
        Add a clause stating that: sum(boolvars) >= target
        :param boolvars: A list of BoolVars.
        :param target: A BoolVar.
        """
        lhandle = make_boolvar_array(boolvars)
        return backend.add_clauses_sum_bool_array_greater_eq_var(self._handle, lhandle, target._handle)

    def add_clauses_max_bool_array_less_eq_var(self, boolvars: List[BoolVar], target: BoolVar):
        """
        Add a clause stating that: max(boolvars) <= target
        :param boolvars: A list of BoolVars.
        :param target: A BoolVar.
        """
        lhandle = make_boolvar_array(boolvars)
        return backend.add_clauses_max_bool_array_less_eq_var(self._handle, lhandle, target._handle)

    def add_clauses_sum_bool_array_less_eq_var(self, boolvars: List[BoolVar], target: BoolVar):
        """
        Add a clause stating that: sum(boolvars) <= target * |boolvars|.
        :param boolvars: A list of BoolVars.
        :param target: A BoolVar.
        """
        lhandle = make_boolvar_array(boolvars)
        return backend.add_clauses_sum_bool_array_less_eq_var(self._handle, lhandle, target._handle)

    def add_constructive_disjunction(self, constraints: List[Constraint]):
        """
        Make a constructive disjunction constraint.
        :params constraints: A list of constraints
        """
        lhandle = make_constraint_array(constraints)
        return backend.add_constructive_disjunction(self._handle, lhandle)
