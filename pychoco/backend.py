# This file was automatically generated by SWIG (http://www.swig.org).
# Version 4.0.2
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.

from sys import version_info as _swig_python_version_info
if _swig_python_version_info < (2, 7, 0):
    raise RuntimeError("Python 2.7 or later required")

# Import the low-level C/C++ module
if __package__ or "." in __name__:
    from . import _backend
else:
    import _backend

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)


def _swig_setattr_nondynamic_instance_variable(set):
    def set_instance_attr(self, name, value):
        if name == "thisown":
            self.this.own(value)
        elif name == "this":
            set(self, name, value)
        elif hasattr(self, name) and isinstance(getattr(type(self), name), property):
            set(self, name, value)
        else:
            raise AttributeError("You cannot add instance attributes to %s" % self)
    return set_instance_attr


def _swig_setattr_nondynamic_class_variable(set):
    def set_class_attr(cls, name, value):
        if hasattr(cls, name) and not isinstance(getattr(cls, name), property):
            set(cls, name, value)
        else:
            raise AttributeError("You cannot add class attributes to %s" % cls)
    return set_class_attr


def _swig_add_metaclass(metaclass):
    """Class decorator for adding a metaclass to a SWIG wrapped class - a slimmed down version of six.add_metaclass"""
    def wrapper(cls):
        return metaclass(cls.__name__, cls.__bases__, cls.__dict__.copy())
    return wrapper


class _SwigNonDynamicMeta(type):
    """Meta class to enforce nondynamic attributes (no new attributes) for a class"""
    __setattr__ = _swig_setattr_nondynamic_class_variable(type.__setattr__)



def chocosolver_init():
    return _backend.chocosolver_init()

def chocosolver_cleanup():
    return _backend.chocosolver_cleanup()

def chocosolver_is_initialized():
    return _backend.chocosolver_is_initialized()

def create_model():
    return _backend.create_model()

def create_model_s(arg1):
    return _backend.create_model_s(arg1)

def get_model_name(arg1):
    return _backend.get_model_name(arg1)

def get_solver(arg1):
    return _backend.get_solver(arg1)

def solve(arg1, arg2):
    return _backend.solve(arg1, arg2)

def find_solution(arg1, arg2):
    return _backend.find_solution(arg1, arg2)

def find_all_solutions(arg1, arg2):
    return _backend.find_all_solutions(arg1, arg2)

def find_optimal_solution(arg1, arg2, arg3, arg4):
    return _backend.find_optimal_solution(arg1, arg2, arg3, arg4)

def find_all_optimal_solutions(arg1, arg2, arg3, arg4):
    return _backend.find_all_optimal_solutions(arg1, arg2, arg3, arg4)

def show_statistics(arg1):
    return _backend.show_statistics(arg1)

def show_short_statistics(arg1):
    return _backend.show_short_statistics(arg1)

def get_solution_count(arg1):
    return _backend.get_solution_count(arg1)

def time_counter(arg1, arg2):
    return _backend.time_counter(arg1, arg2)

def solution_counter(arg1, arg2):
    return _backend.solution_counter(arg1, arg2)

def node_counter(arg1, arg2):
    return _backend.node_counter(arg1, arg2)

def fail_counter(arg1, arg2):
    return _backend.fail_counter(arg1, arg2)

def restart_counter(arg1, arg2):
    return _backend.restart_counter(arg1, arg2)

def backtrack_counter(arg1, arg2):
    return _backend.backtrack_counter(arg1, arg2)

def get_int_val(arg1, arg2):
    return _backend.get_int_val(arg1, arg2)

def get_variable_name(arg1):
    return _backend.get_variable_name(arg1)

def is_instantiated(arg1):
    return _backend.is_instantiated(arg1)

def intvar_sii(arg1, arg2, arg3, arg4):
    return _backend.intvar_sii(arg1, arg2, arg3, arg4)

def intvar_ii(arg1, arg2, arg3):
    return _backend.intvar_ii(arg1, arg2, arg3)

def intvar_i(arg1, arg2):
    return _backend.intvar_i(arg1, arg2)

def intvar_si(arg1, arg2, arg3):
    return _backend.intvar_si(arg1, arg2, arg3)

def get_intvar_name(arg1):
    return _backend.get_intvar_name(arg1)

def get_intvar_lb(arg1):
    return _backend.get_intvar_lb(arg1)

def get_intvar_ub(arg1):
    return _backend.get_intvar_ub(arg1)

def get_intvar_value(arg1):
    return _backend.get_intvar_value(arg1)

def boolvar_s(arg1, arg2):
    return _backend.boolvar_s(arg1, arg2)

def boolvar(arg1):
    return _backend.boolvar(arg1)

def boolvar_b(arg1, arg2):
    return _backend.boolvar_b(arg1, arg2)

def boolvar_sb(arg1, arg2, arg3):
    return _backend.boolvar_sb(arg1, arg2, arg3)

def get_constraint_name(arg1):
    return _backend.get_constraint_name(arg1)

def post(arg1):
    return _backend.post(arg1)

def reify(arg1):
    return _backend.reify(arg1)

def is_satisfied(arg1):
    return _backend.is_satisfied(arg1)

def arithm_iv_cst(arg1, arg2, arg3, arg4):
    return _backend.arithm_iv_cst(arg1, arg2, arg3, arg4)

def arithm_iv_iv(arg1, arg2, arg3, arg4):
    return _backend.arithm_iv_iv(arg1, arg2, arg3, arg4)

def arithm_iv_iv_cst(arg1, arg2, arg3, arg4, arg5, arg6):
    return _backend.arithm_iv_iv_cst(arg1, arg2, arg3, arg4, arg5, arg6)

def arithm_iv_iv_iv(arg1, arg2, arg3, arg4, arg5, arg6):
    return _backend.arithm_iv_iv_iv(arg1, arg2, arg3, arg4, arg5, arg6)

def member_iv_iarray(arg1, arg2, arg3):
    return _backend.member_iv_iarray(arg1, arg2, arg3)

def member_iv_i_i(arg1, arg2, arg3, arg4):
    return _backend.member_iv_i_i(arg1, arg2, arg3, arg4)

def mod_iv_i_i(arg1, arg2, arg3, arg4):
    return _backend.mod_iv_i_i(arg1, arg2, arg3, arg4)

def mod_iv_i_iv(arg1, arg2, arg3, arg4):
    return _backend.mod_iv_i_iv(arg1, arg2, arg3, arg4)

def mod_iv_iv_iv(arg1, arg2, arg3, arg4):
    return _backend.mod_iv_iv_iv(arg1, arg2, arg3, arg4)

def not_(arg1, arg2):
    return _backend.not_(arg1, arg2)

def not_member_iv_iarray(arg1, arg2, arg3):
    return _backend.not_member_iv_iarray(arg1, arg2, arg3)

def not_member_iv_i_i(arg1, arg2, arg3, arg4):
    return _backend.not_member_iv_i_i(arg1, arg2, arg3, arg4)

def absolute(arg1, arg2, arg3):
    return _backend.absolute(arg1, arg2, arg3)

def distance_iv_iv_i(arg1, arg2, arg3, arg4, arg5):
    return _backend.distance_iv_iv_i(arg1, arg2, arg3, arg4, arg5)

def distance_iv_iv_iv(arg1, arg2, arg3, arg4, arg5):
    return _backend.distance_iv_iv_iv(arg1, arg2, arg3, arg4, arg5)

def element_iv_iarray_iv_i(arg1, arg2, arg3, arg4, arg5):
    return _backend.element_iv_iarray_iv_i(arg1, arg2, arg3, arg4, arg5)

def element_iv_ivarray_iv_i(arg1, arg2, arg3, arg4, arg5):
    return _backend.element_iv_ivarray_iv_i(arg1, arg2, arg3, arg4, arg5)

def square(arg1, arg2, arg3):
    return _backend.square(arg1, arg2, arg3)

def table(arg1, arg2, arg3, arg4, arg5):
    return _backend.table(arg1, arg2, arg3, arg4, arg5)

def times_iv_i_iv(arg1, arg2, arg3, arg4):
    return _backend.times_iv_i_iv(arg1, arg2, arg3, arg4)

def times_iv_iv_i(arg1, arg2, arg3, arg4):
    return _backend.times_iv_iv_i(arg1, arg2, arg3, arg4)

def times_iv_iv_iv(arg1, arg2, arg3, arg4):
    return _backend.times_iv_iv_iv(arg1, arg2, arg3, arg4)

def pow_(arg1, arg2, arg3, arg4):
    return _backend.pow_(arg1, arg2, arg3, arg4)

def div_(arg1, arg2, arg3, arg4):
    return _backend.div_(arg1, arg2, arg3, arg4)

def max_iv_iv_iv(arg1, arg2, arg3, arg4):
    return _backend.max_iv_iv_iv(arg1, arg2, arg3, arg4)

def max_iv_ivarray(arg1, arg2, arg3):
    return _backend.max_iv_ivarray(arg1, arg2, arg3)

def min_iv_iv_iv(arg1, arg2, arg3, arg4):
    return _backend.min_iv_iv_iv(arg1, arg2, arg3, arg4)

def min_iv_ivarray(arg1, arg2, arg3):
    return _backend.min_iv_ivarray(arg1, arg2, arg3)

def all_different(arg1, arg2):
    return _backend.all_different(arg1, arg2)

def all_equal(arg1, arg2):
    return _backend.all_equal(arg1, arg2)

def not_all_equal(arg1, arg2):
    return _backend.not_all_equal(arg1, arg2)

def among(arg1, arg2, arg3, arg4):
    return _backend.among(arg1, arg2, arg3, arg4)

def and_bv_bv(arg1, arg2):
    return _backend.and_bv_bv(arg1, arg2)

def and_cs_cs(arg1, arg2):
    return _backend.and_cs_cs(arg1, arg2)

def at_least_n_values(arg1, arg2, arg3, arg4):
    return _backend.at_least_n_values(arg1, arg2, arg3, arg4)

def at_most_n_values(arg1, arg2, arg3, arg4):
    return _backend.at_most_n_values(arg1, arg2, arg3, arg4)

def bin_packing(arg1, arg2, arg3, arg4, arg5):
    return _backend.bin_packing(arg1, arg2, arg3, arg4, arg5)

def bools_int_channeling(arg1, arg2, arg3, arg4):
    return _backend.bools_int_channeling(arg1, arg2, arg3, arg4)

def bits_int_channeling(arg1, arg2, arg3):
    return _backend.bits_int_channeling(arg1, arg2, arg3)

def clauses_int_channeling(arg1, arg2, arg3, arg4):
    return _backend.clauses_int_channeling(arg1, arg2, arg3, arg4)

def circuit(arg1, arg2, arg3, arg4):
    return _backend.circuit(arg1, arg2, arg3, arg4)

def count_i(arg1, arg2, arg3, arg4):
    return _backend.count_i(arg1, arg2, arg3, arg4)

def count_iv(arg1, arg2, arg3, arg4):
    return _backend.count_iv(arg1, arg2, arg3, arg4)

def diff_n(arg1, arg2, arg3, arg4, arg5, arg6):
    return _backend.diff_n(arg1, arg2, arg3, arg4, arg5, arg6)

def decreasing(arg1, arg2, arg3):
    return _backend.decreasing(arg1, arg2, arg3)

def increasing(arg1, arg2, arg3):
    return _backend.increasing(arg1, arg2, arg3)

def global_cardinality(arg1, arg2, arg3, arg4, arg5):
    return _backend.global_cardinality(arg1, arg2, arg3, arg4, arg5)

def inverse_channeling(arg1, arg2, arg3, arg4, arg5, arg6):
    return _backend.inverse_channeling(arg1, arg2, arg3, arg4, arg5, arg6)

def int_value_precede_chain(arg1, arg2, arg3):
    return _backend.int_value_precede_chain(arg1, arg2, arg3)

def knapsack(arg1, arg2, arg3, arg4, arg5, arg6):
    return _backend.knapsack(arg1, arg2, arg3, arg4, arg5, arg6)

def lex_chain_less(arg1, arg2):
    return _backend.lex_chain_less(arg1, arg2)

def lex_chain_less_eq(arg1, arg2):
    return _backend.lex_chain_less_eq(arg1, arg2)

def lex_less(arg1, arg2, arg3):
    return _backend.lex_less(arg1, arg2, arg3)

def lex_less_eq(arg1, arg2, arg3):
    return _backend.lex_less_eq(arg1, arg2, arg3)

def argmax(arg1, arg2, arg3, arg4):
    return _backend.argmax(arg1, arg2, arg3, arg4)

def argmin(arg1, arg2, arg3, arg4):
    return _backend.argmin(arg1, arg2, arg3, arg4)

def n_values(arg1, arg2, arg3):
    return _backend.n_values(arg1, arg2, arg3)

def or_bv_bv(arg1, arg2):
    return _backend.or_bv_bv(arg1, arg2)

def or_cs_cs(arg1, arg2):
    return _backend.or_cs_cs(arg1, arg2)

def path(arg1, arg2, arg3, arg4, arg5):
    return _backend.path(arg1, arg2, arg3, arg4, arg5)

def scalar_i(arg1, arg2, arg3, arg4, arg5):
    return _backend.scalar_i(arg1, arg2, arg3, arg4, arg5)

def scalar_iv(arg1, arg2, arg3, arg4, arg5):
    return _backend.scalar_iv(arg1, arg2, arg3, arg4, arg5)

def sort(arg1, arg2, arg3):
    return _backend.sort(arg1, arg2, arg3)

def sub_circuit(arg1, arg2, arg3, arg4):
    return _backend.sub_circuit(arg1, arg2, arg3, arg4)

def sub_path(arg1, arg2, arg3, arg4, arg5, arg6):
    return _backend.sub_path(arg1, arg2, arg3, arg4, arg5, arg6)

def sum_iv_i(arg1, arg2, arg3, arg4):
    return _backend.sum_iv_i(arg1, arg2, arg3, arg4)

def sum_iv_iv(arg1, arg2, arg3, arg4):
    return _backend.sum_iv_iv(arg1, arg2, arg3, arg4)

def sum_ivarray_ivarray(arg1, arg2, arg3, arg4):
    return _backend.sum_ivarray_ivarray(arg1, arg2, arg3, arg4)

def sum_bv_i(arg1, arg2, arg3, arg4):
    return _backend.sum_bv_i(arg1, arg2, arg3, arg4)

def sum_bv_iv(arg1, arg2, arg3, arg4):
    return _backend.sum_bv_iv(arg1, arg2, arg3, arg4)

def tree(arg1, arg2, arg3, arg4):
    return _backend.tree(arg1, arg2, arg3, arg4)

def create_intvar_array(arg1):
    return _backend.create_intvar_array(arg1)

def intvar_array_length(arg1):
    return _backend.intvar_array_length(arg1)

def intvar_array_set(arg1, arg2, arg3):
    return _backend.intvar_array_set(arg1, arg2, arg3)

def create_boolvar_array(arg1):
    return _backend.create_boolvar_array(arg1)

def boolvar_array_set(arg1, arg2, arg3):
    return _backend.boolvar_array_set(arg1, arg2, arg3)

def create_constraint_array(arg1):
    return _backend.create_constraint_array(arg1)

def constraint_array_set(arg1, arg2, arg3):
    return _backend.constraint_array_set(arg1, arg2, arg3)

def create_int_array(arg1):
    return _backend.create_int_array(arg1)

def int_array_length(arg1):
    return _backend.int_array_length(arg1)

def int_array_set(arg1, arg2, arg3):
    return _backend.int_array_set(arg1, arg2, arg3)

def create_int_array_array(arg1):
    return _backend.create_int_array_array(arg1)

def int_array_array_length(arg1):
    return _backend.int_array_array_length(arg1)

def int_array_array_set(arg1, arg2, arg3):
    return _backend.int_array_array_set(arg1, arg2, arg3)

def create_int_array_array_array(arg1):
    return _backend.create_int_array_array_array(arg1)

def int_array_array_array_length(arg1):
    return _backend.int_array_array_array_length(arg1)

def int_array_array_array_set(arg1, arg2, arg3):
    return _backend.int_array_array_array_set(arg1, arg2, arg3)

def create_criterion_array(arg1):
    return _backend.create_criterion_array(arg1)

def criterion_array_set(arg1, arg2, arg3):
    return _backend.criterion_array_set(arg1, arg2, arg3)

def array_length(arg1):
    return _backend.array_length(arg1)

def list_size(arg1):
    return _backend.list_size(arg1)

def list_solution_get(arg1, arg2):
    return _backend.list_solution_get(arg1, arg2)

def set_random_search(arg1, arg2, arg3):
    return _backend.set_random_search(arg1, arg2, arg3)

def set_dom_over_w_deg_search(arg1, arg2):
    return _backend.set_dom_over_w_deg_search(arg1, arg2)

def set_dom_over_w_deg_ref_search(arg1, arg2):
    return _backend.set_dom_over_w_deg_ref_search(arg1, arg2)

def set_activity_based_search(arg1, arg2):
    return _backend.set_activity_based_search(arg1, arg2)

def set_min_dom_lb_search(arg1, arg2):
    return _backend.set_min_dom_lb_search(arg1, arg2)

def set_min_dom_ub_search(arg1, arg2):
    return _backend.set_min_dom_ub_search(arg1, arg2)

def set_conflict_history_search(arg1, arg2):
    return _backend.set_conflict_history_search(arg1, arg2)

def set_default_search(arg1):
    return _backend.set_default_search(arg1)

def set_input_order_lb_search(arg1, arg2):
    return _backend.set_input_order_lb_search(arg1, arg2)

def set_input_order_ub_search(arg1, arg2):
    return _backend.set_input_order_ub_search(arg1, arg2)

def set_failure_length_based_search(arg1, arg2):
    return _backend.set_failure_length_based_search(arg1, arg2)

def set_failure_rate_based_search(arg1, arg2):
    return _backend.set_failure_rate_based_search(arg1, arg2)

def create_fa():
    return _backend.create_fa()

def create_fa_regexp(arg1):
    return _backend.create_fa_regexp(arg1)

def create_fa_regexp_min_max(arg1, arg2, arg3):
    return _backend.create_fa_regexp_min_max(arg1, arg2, arg3)

def create_cost_fa():
    return _backend.create_cost_fa()

def create_cost_fa_from_fa(arg1):
    return _backend.create_cost_fa_from_fa(arg1)

def get_nb_states(arg1):
    return _backend.get_nb_states(arg1)

def get_nb_symbols(arg1):
    return _backend.get_nb_symbols(arg1)

def add_state(arg1):
    return _backend.add_state(arg1)

def remove_symbol(arg1, arg2):
    return _backend.remove_symbol(arg1, arg2)

def add_transition(arg1, arg2, arg3, arg4):
    return _backend.add_transition(arg1, arg2, arg3, arg4)

def delete_transition(arg1, arg2, arg3, arg4):
    return _backend.delete_transition(arg1, arg2, arg3, arg4)

def get_initial_state(arg1):
    return _backend.get_initial_state(arg1)

def is_final(arg1, arg2):
    return _backend.is_final(arg1, arg2)

def set_initial_state(arg1, arg2):
    return _backend.set_initial_state(arg1, arg2)

def set_final(arg1, arg2):
    return _backend.set_final(arg1, arg2)

def set_non_final(arg1, arg2):
    return _backend.set_non_final(arg1, arg2)

def cost_fa_add_counter(arg1, arg2):
    return _backend.cost_fa_add_counter(arg1, arg2)

def fa_union(arg1, arg2):
    return _backend.fa_union(arg1, arg2)

def fa_minimize(arg1):
    return _backend.fa_minimize(arg1)

def fa_complement(arg1):
    return _backend.fa_complement(arg1)

def create_counter_state(arg1, arg2, arg3):
    return _backend.create_counter_state(arg1, arg2, arg3)

def chocosolver_handles_destroy(arg1):
    return _backend.chocosolver_handles_destroy(arg1)


