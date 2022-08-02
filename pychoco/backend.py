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



def chocosolver_init() -> "void":
    return _backend.chocosolver_init()

def chocosolver_cleanup() -> "void":
    return _backend.chocosolver_cleanup()

def chocosolver_is_initialized() -> "int":
    return _backend.chocosolver_is_initialized()

def create_model(arg1: "char *") -> "void *":
    return _backend.create_model(arg1)

def get_model_name(arg1: "void *") -> "char *":
    return _backend.get_model_name(arg1)

def get_solver(arg1: "void *") -> "void *":
    return _backend.get_solver(arg1)

def find_solution(arg1: "void *", arg2: "void *") -> "void *":
    return _backend.find_solution(arg1, arg2)

def find_all_solutions(arg1: "void *", arg2: "void *") -> "void *":
    return _backend.find_all_solutions(arg1, arg2)

def find_optimal_solution(arg1: "void *", arg2: "void *", arg3: "_Bool", arg4: "void *") -> "void *":
    return _backend.find_optimal_solution(arg1, arg2, arg3, arg4)

def find_all_optimal_solutions(arg1: "void *", arg2: "void *", arg3: "_Bool", arg4: "void *") -> "void *":
    return _backend.find_all_optimal_solutions(arg1, arg2, arg3, arg4)

def show_statistics(arg1: "void *") -> "void":
    return _backend.show_statistics(arg1)

def show_short_statistics(arg1: "void *") -> "void":
    return _backend.show_short_statistics(arg1)

def time_counter(arg1: "void *", arg2: "long") -> "void *":
    return _backend.time_counter(arg1, arg2)

def solution_counter(arg1: "void *", arg2: "long") -> "void *":
    return _backend.solution_counter(arg1, arg2)

def node_counter(arg1: "void *", arg2: "long") -> "void *":
    return _backend.node_counter(arg1, arg2)

def fail_counter(arg1: "void *", arg2: "long") -> "void *":
    return _backend.fail_counter(arg1, arg2)

def restart_counter(arg1: "void *", arg2: "long") -> "void *":
    return _backend.restart_counter(arg1, arg2)

def backtrack_counter(arg1: "void *", arg2: "long") -> "void *":
    return _backend.backtrack_counter(arg1, arg2)

def get_int_val(arg1: "void *", arg2: "void *") -> "int":
    return _backend.get_int_val(arg1, arg2)

def intvar_sii(arg1: "void *", arg2: "char *", arg3: "int", arg4: "int") -> "void *":
    return _backend.intvar_sii(arg1, arg2, arg3, arg4)

def intvar_ii(arg1: "void *", arg2: "int", arg3: "int") -> "void *":
    return _backend.intvar_ii(arg1, arg2, arg3)

def get_intvar_name(arg1: "void *") -> "char *":
    return _backend.get_intvar_name(arg1)

def get_intvar_lb(arg1: "void *") -> "int":
    return _backend.get_intvar_lb(arg1)

def get_intvar_ub(arg1: "void *") -> "int":
    return _backend.get_intvar_ub(arg1)

def boolvar_s(arg1: "void *", arg2: "char *") -> "void *":
    return _backend.boolvar_s(arg1, arg2)

def boolvar(arg1: "void *") -> "void *":
    return _backend.boolvar(arg1)

def boolvar_b(arg1: "void *", arg2: "_Bool") -> "void *":
    return _backend.boolvar_b(arg1, arg2)

def boolvar_sb(arg1: "void *", arg2: "char *", arg3: "_Bool") -> "void *":
    return _backend.boolvar_sb(arg1, arg2, arg3)

def get_constraint_name(arg1: "void *") -> "char *":
    return _backend.get_constraint_name(arg1)

def post(arg1: "void *") -> "void":
    return _backend.post(arg1)

def reify(arg1: "void *") -> "void *":
    return _backend.reify(arg1)

def is_satisfied(arg1: "void *") -> "int":
    return _backend.is_satisfied(arg1)

def arithm_iv_cst(arg1: "void *", arg2: "void *", arg3: "char *", arg4: "int") -> "void *":
    return _backend.arithm_iv_cst(arg1, arg2, arg3, arg4)

def arithm_iv_iv(arg1: "void *", arg2: "void *", arg3: "char *", arg4: "void *") -> "void *":
    return _backend.arithm_iv_iv(arg1, arg2, arg3, arg4)

def arithm_iv_iv_cst(arg1: "void *", arg2: "void *", arg3: "char *", arg4: "void *", arg5: "char *", arg6: "int") -> "void *":
    return _backend.arithm_iv_iv_cst(arg1, arg2, arg3, arg4, arg5, arg6)

def arithm_iv_iv_iv(arg1: "void *", arg2: "void *", arg3: "char *", arg4: "void *", arg5: "char *", arg6: "void *") -> "void *":
    return _backend.arithm_iv_iv_iv(arg1, arg2, arg3, arg4, arg5, arg6)

def member_iv_iarray(arg1: "void *", arg2: "void *", arg3: "void *") -> "void *":
    return _backend.member_iv_iarray(arg1, arg2, arg3)

def member_iv_i_i(arg1: "void *", arg2: "void *", arg3: "int", arg4: "int") -> "void *":
    return _backend.member_iv_i_i(arg1, arg2, arg3, arg4)

def mod_iv_i_i(arg1: "void *", arg2: "void *", arg3: "int", arg4: "int") -> "void *":
    return _backend.mod_iv_i_i(arg1, arg2, arg3, arg4)

def mod_iv_i_iv(arg1: "void *", arg2: "void *", arg3: "int", arg4: "void *") -> "void *":
    return _backend.mod_iv_i_iv(arg1, arg2, arg3, arg4)

def mod_iv_iv_iv(arg1: "void *", arg2: "void *", arg3: "void *", arg4: "void *") -> "void *":
    return _backend.mod_iv_iv_iv(arg1, arg2, arg3, arg4)

def _not(arg1: "void *", arg2: "void *") -> "void *":
    return _backend._not(arg1, arg2)

def not_member_iv_iarray(arg1: "void *", arg2: "void *", arg3: "void *") -> "void *":
    return _backend.not_member_iv_iarray(arg1, arg2, arg3)

def not_member_iv_i_i(arg1: "void *", arg2: "void *", arg3: "int", arg4: "int") -> "void *":
    return _backend.not_member_iv_i_i(arg1, arg2, arg3, arg4)

def absolute(arg1: "void *", arg2: "void *", arg3: "void *") -> "void *":
    return _backend.absolute(arg1, arg2, arg3)

def distance_iv_iv_i(arg1: "void *", arg2: "void *", arg3: "void *", arg4: "char *", arg5: "int") -> "void *":
    return _backend.distance_iv_iv_i(arg1, arg2, arg3, arg4, arg5)

def distance_iv_iv_iv(arg1: "void *", arg2: "void *", arg3: "void *", arg4: "char *", arg5: "void *") -> "void *":
    return _backend.distance_iv_iv_iv(arg1, arg2, arg3, arg4, arg5)

def element_iv_iarray_iv_i(arg1: "void *", arg2: "void *", arg3: "void *", arg4: "void *", arg5: "int") -> "void *":
    return _backend.element_iv_iarray_iv_i(arg1, arg2, arg3, arg4, arg5)

def element_iv_ivarray_iv_i(arg1: "void *", arg2: "void *", arg3: "void *", arg4: "void *", arg5: "int") -> "void *":
    return _backend.element_iv_ivarray_iv_i(arg1, arg2, arg3, arg4, arg5)

def square(arg1: "void *", arg2: "void *", arg3: "void *") -> "void *":
    return _backend.square(arg1, arg2, arg3)

def times_iv_i_iv(arg1: "void *", arg2: "void *", arg3: "int", arg4: "void *") -> "void *":
    return _backend.times_iv_i_iv(arg1, arg2, arg3, arg4)

def times_iv_iv_i(arg1: "void *", arg2: "void *", arg3: "void *", arg4: "int") -> "void *":
    return _backend.times_iv_iv_i(arg1, arg2, arg3, arg4)

def times_iv_iv_iv(arg1: "void *", arg2: "void *", arg3: "void *", arg4: "void *") -> "void *":
    return _backend.times_iv_iv_iv(arg1, arg2, arg3, arg4)

def div_(arg1: "void *", arg2: "void *", arg3: "void *", arg4: "void *") -> "void *":
    return _backend.div_(arg1, arg2, arg3, arg4)

def max_iv_iv_iv(arg1: "void *", arg2: "void *", arg3: "void *", arg4: "void *") -> "void *":
    return _backend.max_iv_iv_iv(arg1, arg2, arg3, arg4)

def max_iv_ivarray(arg1: "void *", arg2: "void *", arg3: "void *") -> "void *":
    return _backend.max_iv_ivarray(arg1, arg2, arg3)

def min_iv_iv_iv(arg1: "void *", arg2: "void *", arg3: "void *", arg4: "void *") -> "void *":
    return _backend.min_iv_iv_iv(arg1, arg2, arg3, arg4)

def min_iv_ivarray(arg1: "void *", arg2: "void *", arg3: "void *") -> "void *":
    return _backend.min_iv_ivarray(arg1, arg2, arg3)

def all_different(arg1: "void *", arg2: "void *") -> "void *":
    return _backend.all_different(arg1, arg2)

def create_intvar_array(arg1: "int") -> "void *":
    return _backend.create_intvar_array(arg1)

def intvar_array_length(arg1: "void *") -> "int":
    return _backend.intvar_array_length(arg1)

def intvar_array_set(arg1: "void *", arg2: "void *", arg3: "int") -> "void":
    return _backend.intvar_array_set(arg1, arg2, arg3)

def create_int_array(arg1: "int") -> "void *":
    return _backend.create_int_array(arg1)

def int_array_length(arg1: "void *") -> "int":
    return _backend.int_array_length(arg1)

def int_array_set(arg1: "void *", arg2: "int", arg3: "int") -> "void":
    return _backend.int_array_set(arg1, arg2, arg3)

def create_criterion_array(arg1: "int") -> "void *":
    return _backend.create_criterion_array(arg1)

def criterion_array_set(arg1: "void *", arg2: "void *", arg3: "int") -> "void":
    return _backend.criterion_array_set(arg1, arg2, arg3)

def array_length(arg1: "void *") -> "int":
    return _backend.array_length(arg1)

def list_size(arg1: "void *") -> "int":
    return _backend.list_size(arg1)

def list_solution_get(arg1: "void *", arg2: "int") -> "void *":
    return _backend.list_solution_get(arg1, arg2)

def set_random_search(arg1: "void *", arg2: "void *", arg3: "long") -> "void":
    return _backend.set_random_search(arg1, arg2, arg3)

def set_dom_over_w_deg_search(arg1: "void *", arg2: "void *") -> "void":
    return _backend.set_dom_over_w_deg_search(arg1, arg2)

def set_dom_over_w_deg_ref_search(arg1: "void *", arg2: "void *") -> "void":
    return _backend.set_dom_over_w_deg_ref_search(arg1, arg2)

def set_activity_based_search(arg1: "void *", arg2: "void *") -> "void":
    return _backend.set_activity_based_search(arg1, arg2)

def set_min_dom_lb_search(arg1: "void *", arg2: "void *") -> "void":
    return _backend.set_min_dom_lb_search(arg1, arg2)

def set_min_dom_ub_search(arg1: "void *", arg2: "void *") -> "void":
    return _backend.set_min_dom_ub_search(arg1, arg2)

def set_conflict_history_search(arg1: "void *", arg2: "void *") -> "void":
    return _backend.set_conflict_history_search(arg1, arg2)

def set_default_search(arg1: "void *") -> "void":
    return _backend.set_default_search(arg1)

def set_input_order_lb_search(arg1: "void *", arg2: "void *") -> "void":
    return _backend.set_input_order_lb_search(arg1, arg2)

def set_input_order_ub_search(arg1: "void *", arg2: "void *") -> "void":
    return _backend.set_input_order_ub_search(arg1, arg2)

def set_failure_length_based_search(arg1: "void *", arg2: "void *") -> "void":
    return _backend.set_failure_length_based_search(arg1, arg2)

def set_failure_rate_based_search(arg1: "void *", arg2: "void *") -> "void":
    return _backend.set_failure_rate_based_search(arg1, arg2)

def chocosolver_handles_destroy(arg1: "void *") -> "void":
    return _backend.chocosolver_handles_destroy(arg1)


