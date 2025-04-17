from abc import ABC, abstractmethod
from typing import Union, List

from pychoco import backend
from pychoco._utils import make_intvar_array, make_setvar_array, make_int_array, make_boolvar_array
from pychoco.constraints.constraint import Constraint
from pychoco.variables.boolvar import BoolVar
from pychoco.variables.intvar import IntVar
from pychoco.variables.setvar import SetVar


class SetConstraintFactory(ABC):
    """
    Constraints over set variables.
    """

    @property
    @abstractmethod
    def _handle(self):
        pass

    def set_union(self, intvars_or_setvars: Union[List[IntVar], List[SetVar]], union: SetVar):
        """
        Creates a constraint which ensures that the union of intvars_or_setvars is equal to union.

        :param intvars_or_setvars: Either a list of intvars or setvars.
        :param union: A SetVar.
        :return: A union constraint.
        """
        assert len(intvars_or_setvars) > 0
        if isinstance(intvars_or_setvars[0], IntVar):
            vars_handle = make_intvar_array(intvars_or_setvars)
            constraint_handle = backend.set_union_ints(self._handle, vars_handle, union._handle)
        else:
            vars_handle = make_setvar_array(intvars_or_setvars)
            constraint_handle = backend.set_union(self._handle, vars_handle, union._handle)
        return Constraint(constraint_handle, self)

    def set_union_indices(self, setvars: List[SetVar], indices: SetVar, union: SetVar, i_offset: int = 0):
        """
        Creates a constraint which ensures that the union of setvars_i, where i in indices,
        is equal to union.

        :param setvars: A list of SetVars.
        :param indices: A SetVar.
        :param union: A SetVar.
        :param i_offset: Indices offset.
        :return: A union_indices constraint.
        """
        min_index = min(indices.get_ub())
        max_index = max(indices.get_ub())
        assert min_index >= 0 - i_offset and max_index < len(setvars) - i_offset, \
            "[set_union_indices] Values of the 'indices' setvar are out of bound with 'setvars'"
        setvars_handle = make_setvar_array(setvars)
        constraint_handle = backend.set_union_indices(self._handle, setvars_handle, indices._handle, union._handle,
                                                      i_offset)
        return Constraint(constraint_handle, self)

    def set_intersection(self, setvars: List[SetVar], intersection: SetVar, bc: bool = False):
        """
        Creates a constraint which ensures that the intersection of setvars is equal to intersection.

        :param setvars: A list of SetVars.
        :param intersection: A SetVar.
        :param bc: If True, add a propagator to guarantee bound consistency.
        :return: A set intersection constraint.
        """
        setvars_handle = make_setvar_array(setvars)
        constraint_handle = backend.set_intersection(self._handle, setvars_handle, intersection._handle, bc)
        return Constraint(constraint_handle, self)

    def set_subset_eq(self, setvars: List[SetVar]):
        """
        Creates a constraint establishing that setvars [ i ] is a subset of setvars [ j ] if i < j

        :param setvars: A list of SetVars.
        :return: A subset_eq constraint.
        """
        setvars_handle = make_setvar_array(setvars)
        constraint_handle = backend.set_subset_eq(self._handle, setvars_handle)
        return Constraint(constraint_handle, self)

    def set_nb_empty(self, setvars: List[SetVar], nb_empty: Union[IntVar, int]):
        """
        Creates a constraint counting the number of empty sets.

        :param setvars: A list of SetVars.
        :param nb_empty: An IntVar or an int.
        :return: An nb_empty set constraint.
        """
        setvars_handle = make_setvar_array(setvars)
        constraint_handle = backend.set_nb_empty(self._handle, setvars_handle, nb_empty._handle)
        return Constraint(constraint_handle, self)

    def set_offset(self, setvar_1: SetVar, setvar_2: SetVar, offset: int):
        """
        Creates a constraint linking setvar_1 and setvar_2 with an offset :
        x in setvar_1 <=> x + offset in setvar_2.

        :param setvar_1: A SetVar.
        :param setvar_2: A SetVar.
        :param offset: An int.
        :return: A set_offset constraint.
        """
        constraint_handle = backend.set_offset(self._handle, setvar_1._handle, setvar_2._handle, offset)
        return Constraint(constraint_handle, self)

    def set_not_empty(self, setvar: SetVar):
        """
        Creates a constraint preventing setvar to be empty.

        :param setvar: A SetVar.
        :return: A set_not_empty constraint.
        """
        constraint_handle = backend.set_not_empty(self._handle, setvar._handle)
        return Constraint(constraint_handle, self)

    def set_sum(self, setvar: SetVar, sum_var: IntVar):
        """
        Creates a constraint summing elements of setvar sum { i | i in setvar } = sum_var

        :param setvar: A SetVar.
        :param sum_var: An IntVar.
        :return: A set_sum constraint.
        """
        constraint_handle = backend.set_sum(self._handle, setvar._handle, sum_var._handle)
        return Constraint(constraint_handle, self)

    def set_sum_element(self, indices: SetVar, weights: List[int], sum_var: IntVar, offset: int = 0):
        """
        Creates a constraint summing weights given by a set of indices:
        sum { weights [ i - offset ] | i in indices } = sum_var
        Also ensures that elements in indices belong to [ offset, offset + len(weights) - 1 ]

        :param indices: A SetVar.
        :param weights: A list of ints.
        :param sum_var: An IntVar.
        :param offset: index offset.
        :return: A set_sum_element constraint.
        """
        weights_handle = make_int_array(weights)
        constraint_handle = backend.set_sum_elements(self._handle, indices._handle, weights_handle, offset,
                                                     sum_var._handle)
        return Constraint(constraint_handle, self)

    def set_max(self, setvar: SetVar, max_var: IntVar, not_empty: bool):
        """
        Creates a constraint over the maximum element in a set: max { i | i in setvar } = max_var

        :param setvar: A SetVar.
        :param max_var: An IntVar.
        :param not_empty: If True, setvar cannot be empty.
        :return: A set_max constraint.
        """
        constraint_handle = backend.set_max(self._handle, setvar._handle, max_var._handle, not_empty)
        return Constraint(constraint_handle, self)

    def set_max_indices(self, indices: SetVar, weights: List[int], max_var: IntVar, not_empty: bool, offset: int = 0):
        """
        Creates a constraint over the maximum element induces by a set:
        max { weights [ i - offset ] | i in indices } = max_var.

        :param indices: A SetVar.
        :param weights: A list of ints.
        :param max_var: An IntVar.
        :param not_empty: If True, indices cannot be empty.
        :param offset:
        :return: A set_max_indices constraint.
        """
        min_index = min(indices.get_ub())
        max_index = max(indices.get_ub())
        assert min_index >= 0 - offset and max_index < len(weights) - offset, \
            "[set_max_indices] Values of the 'indices' setvar are out of bound with 'weights'"
        weights_handle = make_int_array(weights)
        constraint_handle = backend.set_max_indices(self._handle, indices._handle, weights_handle, offset, max_var._handle,
                                                    not_empty)
        return Constraint(constraint_handle, self)

    def set_min(self, setvar: SetVar, min_var: IntVar, not_empty: bool):
        """
        Creates a constraint over the minimum element in a set: min { i | i in setvar } = min_var

        :param setvar: A SetVar.
        :param min_var: An IntVar.
        :param not_empty: If True, setvar cannot be empty.
        :return: A set_min constraint.
        """
        constraint_handle = backend.set_min(self._handle, setvar._handle, min_var._handle, not_empty)
        return Constraint(constraint_handle, self)

    def set_min_indices(self, indices: SetVar, weights: List[int], min_var: IntVar, not_empty: bool, offset: int = 0):
        """
        Creates a constraint over the minimum element induces by a set:
        max { weights [ i - offset ] | i in indices } = min_var.

        :param indices: A SetVar.
        :param weights: A list of ints.
        :param min_var: An IntVar.
        :param not_empty: If True, indices cannot be empty.
        :param offset:
        :return: A set_min_indices constraint.
        """
        min_index = min(indices.get_ub())
        max_index = max(indices.get_ub())
        assert min_index >= 0 - offset and max_index < len(weights) - offset, \
            "[set_min_indices] Values of the 'indices' setvar are out of bound with 'weights'"
        weights_handle = make_int_array(weights)
        constraint_handle = backend.set_min_indices(self._handle, indices._handle, weights_handle, offset, min_var._handle,
                                                    not_empty)
        return Constraint(constraint_handle, self)

    def set_bools_channeling(self, boolvars: List[BoolVar], setvar: SetVar, offset: int = 0):
        """
        Creates a constraint channeling a set variable with boolean variables :
        i in setvar <=> boolvars [ i - offset ] = True.

        :param boolvars: A list of BoolVars.
        :param setvar: A SetVar.
        :param offset: An int.
        :return: A set_bools_channeling constraint.
        """
        boolvars_handle = make_boolvar_array(boolvars)
        constraint_handle = backend.set_bools_channeling(self._handle, boolvars_handle, setvar._handle, offset)
        return Constraint(constraint_handle, self)

    def set_ints_channeling(self, setvars: List[SetVar], intvars: List[IntVar], offset_1: int = 0, offset_2: int = 0):
        """
        Creates a constraint channeling set variables and integer variables :
        x in setvars [ y - offset_1 ] <=> intvars [ x- offset_2 ] = y.

        :param setvars: A list of SetVars.
        :param intvars: A list of IntVars.
        :param offset_1: An int.
        :param offset_2: An int.
        :return: A set_ints_channeling
        """
        setvars_handle = make_setvar_array(setvars)
        intvars_handle = make_intvar_array(intvars)
        constraint_handle = backend.set_ints_channeling(self._handle, setvars_handle, intvars_handle, offset_1, offset_2)
        return Constraint(constraint_handle, self)

    def set_disjoint(self, setvar_1: SetVar, setvar_2: SetVar):
        """
        Creates a constraint stating that the intersection of setvar_1 and setvar_2 should be empty.
        Note that they can be both empty.

        :param setvar_1: A SetVar.
        :param setvar_2: A SetVar.
        :return: A set_disjoint constraint.
        """
        constraint_handle = backend.set_disjoint(self._handle, setvar_1._handle, setvar_2._handle)
        return Constraint(constraint_handle, self)

    def set_all_disjoint(self, setvars: List[SetVar]):
        """
        Creates a constraint stating that the intersection of setvar should be empty.
        Note that there can be multiple empty sets.

        :param setvars: A list of SetVars.
        :return: A set_all_disjoint constraint.
        """
        setvars_handle = make_setvar_array(setvars)
        constraint_handle = backend.set_all_disjoint(self._handle, setvars_handle)
        return Constraint(constraint_handle, self)

    def set_all_different(self, setvars: List[SetVar]):
        """
        Creates a constraint stating that setvars should all be different (not necessarily disjoint).
        Note that there cannot be more than one empty set.

        :param setvars: A list of SetVars.
        :return: A set_all_different constraint.
        """
        setvars_handle = make_setvar_array(setvars)
        constraint_handle = backend.set_all_different(self._handle, setvars_handle)
        return Constraint(constraint_handle, self)

    def set_all_equal(self, setvars: List[SetVar]):
        """
        Creates a constraint stating that setvars should be all equal.

        :param setvars: A list of SetVars.
        :return: A set_all_equal constraint.
        """
        setvars_handle = make_setvar_array(setvars)
        constraint_handle = backend.set_all_equal(self._handle, setvars_handle)
        return Constraint(constraint_handle, self)

    def set_partition(self, setvars: List[SetVar], universe: SetVar):
        """
        Creates a constraint stating that partitions universe< into setvars:
        union( setvars ) = universe AND intersection( setvars ) = {}.

        :param setvars: A list of SetVars.
        :param universe: A SetVar.
        :return: A set_partition constraint.
        """
        setvars_handle = make_setvar_array(setvars)
        constraint_handle = backend.set_partition(self._handle, setvars_handle, universe._handle)
        return Constraint(constraint_handle, self)

    def set_inverse_set(self, setvars: List[SetVar], inverse_setvars: List[SetVar], offset_1: int = 0,
                        offset_2: int = 0):
        """
        Creates a constraint stating that : x in setvars [ y - offset_1 ] <=> y in inverse_setvars [ x - offset_2]

        :param setvars: A list of SetVars.
        :param inverse_setvars: A list of SetVars.
        :param offset_1: An int.
        :param offset_2: An int.
        :return: A set_inverse_set constraint.
        """
        setvars_handle = make_setvar_array(setvars)
        inv_setvars_handle = make_setvar_array(inverse_setvars)
        constraint_handle = backend.set_inverse_set(self._handle, setvars_handle, inv_setvars_handle, offset_1, offset_2)
        return Constraint(constraint_handle, self)

    def set_symmetric(self, setvars: List[SetVar], offset: int = 0):
        """
        Creates a constraint stating that setvars are symmetric sets:
        x in setvars [ y - offset] <=> y in setvars [ x - offset ] .

        :param setvars: A list of SetVars.
        :param offset: An int.
        :return: A set_symmetric constraints.
        """
        setvars_handle = make_setvar_array(setvars)
        constraint_handle = backend.set_symmetric(self._handle, setvars_handle, offset)
        return Constraint(constraint_handle, self)

    def set_element(self, index: IntVar, setvars: List[SetVar], setvar: SetVar, offset: int = 0):
        """
        Creates a constraint enabling to retrieve an element setvar in setvars:
        setvars [ index - offset ] = setvar.

        :param index: An IntVar.
        :param setvars: A list of SetVars.
        :param setvar: A SetVar.
        :param offset: An int.
        :return: A set_element constraint.
        """
        setvars_handle = make_setvar_array(setvars)
        constraint_handle = backend.set_element(self._handle, index._handle, setvars_handle, offset, setvar._handle)
        return Constraint(constraint_handle, self)

    def set_member_set(self, setvars: List[SetVar], setvar: SetVar):
        """
        Creates a member constraint stating that setvar belongs to setvars.

        :param setvars: A list of SetVars.
        :param setvar: A SetVar.
        :return: A set_member_set constraint.
        """
        setvars_handle = make_setvar_array(setvars)
        constraint_handle = backend.set_member_set(self._handle, setvars_handle, setvar._handle)
        return Constraint(constraint_handle, self)

    def set_member_int(self, intvar: Union[IntVar, int], setvar: SetVar):
        """
        Creates a member constraint stating that the value of intvar is in setvar.

        :param intvar: An IntVar or an int.
        :param setvar: A SetVars.
        :return: A set_member_int constraint.
        """
        iv = intvar
        if isinstance(intvar, int):
            iv = self.intvar(intvar)
        constraint_handle = backend.set_member_int(self._handle, iv._handle, setvar._handle)
        return Constraint(constraint_handle, self)

    def set_not_member_int(self, intvar: Union[IntVar, int], setvar: SetVar):
        """
        Creates a not member constraint stating that the value of intvar is not in setvar.

        :param intvar: An IntVar or an int.
        :param setvar: A SetVar.
        :return: A set_not_member_int constraint.
        """
        iv = intvar
        if isinstance(intvar, int):
            iv = self.intvar(intvar)
        constraint_handle = backend.set_not_member_int(self._handle, iv._handle, setvar._handle)
        return Constraint(constraint_handle, self)

    def set_le(self, setvar_1: SetVar, setvar_2: SetVar):
        """
        Creates a "less or equal" constraint stating that setvar_1 <= setvar_2.
        Lexicographic order of the sorted lists of elements.

        :param setvar_1: A SetVar.
        :param setvar_2: A SetVar.
        :return: A set_le constraint.
        """
        constraint_handle = backend.set_le(self._handle, setvar_1._handle, setvar_2._handle)
        return Constraint(constraint_handle, self)

    def set_lt(self, setvar_1: SetVar, setvar_2: SetVar):
        """
        Creates a "strictly less" constraint stating that setvar_1 < setvar_2.
        Lexicographic order of the sorted lists of elements.

        :param setvar_1: A SetVar.
        :param setvar_2: A SetVar.
        :return: A set_lt constraint.
        """
        constraint_handle = backend.set_lt(self._handle, setvar_1._handle, setvar_2._handle)
        return Constraint(constraint_handle, self)
