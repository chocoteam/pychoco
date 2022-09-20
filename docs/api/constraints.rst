.. _constraints:

Constraints
===========

A constraint is a logic formula defining allowed combinations of values for a set of variables (see :ref:`variables`),
i.e., restrictions over variables that must be respected in order to get a feasible solution. A constraint is equipped
with a (set of) filtering algorithm(s), named propagator(s). A propagator removes, from the domains of the target
variables, values that cannot correspond to a valid combination of values. A solution of a problem is a variable-value
assignment verifying all the constraints.

Constraints are directly declared from a `Model` object (see :ref:`model`).

Integer and boolean constraints
-------------------------------

All constraints over integer and boolean variables are declared in the `IntConstraintFactory` abstract class,
which is implemented by the `Model` class.

.. py:currentmodule:: pychoco.constraints.int_constraint_factory.IntConstraintFactory

absolute
^^^^^^^^

.. autofunction:: absolute
   :noindex:

all_different
^^^^^^^^^^^^^

.. autofunction:: all_different
   :noindex:

all_different_except_0
^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: all_different_except_0
   :noindex:

all_different_prec
^^^^^^^^^^^^^^^^^^

.. autofunction:: all_different_prec
   :noindex:

all_equal
^^^^^^^^^

.. autofunction:: all_equal
   :noindex:

among
^^^^^

.. autofunction:: among
   :noindex:

and_
^^^^

.. autofunction:: and_
   :noindex:

argmax
^^^^^^

.. autofunction:: argmax
   :noindex:

argmin
^^^^^^

.. autofunction:: argmin
   :noindex:

arithm
^^^^^^

.. autofunction:: arithm
   :noindex:

at_least_n_values
^^^^^^^^^^^^^^^^^

.. autofunction:: at_least_n_values
   :noindex:

at_most_n_values
^^^^^^^^^^^^^^^^

.. autofunction:: at_most_n_values
   :noindex:

bin_packing
^^^^^^^^^^^

.. autofunction:: bin_packing
   :noindex:

bits_int_channeling
^^^^^^^^^^^^^^^^^^^

.. autofunction:: bits_int_channeling
   :noindex:

bools_int_channeling
^^^^^^^^^^^^^^^^^^^^

.. autofunction:: bools_int_channeling
   :noindex:

circuit
^^^^^^^

.. autofunction:: circuit
   :noindex:

clauses_int_channeling
^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: clauses_int_channeling
   :noindex:

cost_regular
^^^^^^^^^^^^

.. autofunction:: cost_regular
   :noindex:

count
^^^^^

.. autofunction:: count
   :noindex:

cumulative
^^^^^^^^^^

.. autofunction:: cumulative
   :noindex:

decreasing
^^^^^^^^^^

.. autofunction:: decreasing
   :noindex:

diff_n
^^^^^^

.. autofunction:: diff_n
   :noindex:

distance
^^^^^^^^

.. autofunction:: distance
   :noindex:

div
^^^

.. autofunction:: div
   :noindex:

element
^^^^^^^

.. autofunction:: element
   :noindex:

global_cardinality
^^^^^^^^^^^^^^^^^^

.. autofunction:: global_cardinality
   :noindex:

increasing
^^^^^^^^^^

.. autofunction:: increasing
   :noindex:

int_value_precede_chain
^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: int_value_precede_chain
   :noindex:

inverse_channeling
^^^^^^^^^^^^^^^^^^

.. autofunction:: inverse_channeling
   :noindex:

keysort
^^^^^^^

.. autofunction:: keysort
   :noindex:

knapsack
^^^^^^^^

.. autofunction:: knapsack
   :noindex:

lex_chain_less
^^^^^^^^^^^^^^

.. autofunction:: lex_chain_less
   :noindex:

lex_chain_less_eq
^^^^^^^^^^^^^^^^^

.. autofunction:: lex_chain_less_eq
   :noindex:

lex_less
^^^^^^^^

.. autofunction:: lex_less
   :noindex:

lex_less_eq
^^^^^^^^^^^

.. autofunction:: lex_less_eq
   :noindex:

max
^^^

.. autofunction:: max
   :noindex:

mddc
^^^^

.. autofunction:: mddc
   :noindex:

member
^^^^^^

.. autofunction:: member
   :noindex:

min
^^^

.. autofunction:: min
   :noindex:

mod
^^^

.. autofunction:: mod
   :noindex:

multi_cost_regular
^^^^^^^^^^^^^^^^^^

.. autofunction:: multi_cost_regular
   :noindex:

n_values
^^^^^^^^

.. autofunction:: n_values
   :noindex:

not_
^^^^

.. autofunction:: not_
   :noindex:

not_all_equal
^^^^^^^^^^^^^

.. autofunction:: not_all_equal
   :noindex:

not_member
^^^^^^^^^^

.. autofunction:: not_member
   :noindex:

or_
^^^

.. autofunction:: or_
   :noindex:

path
^^^^

.. autofunction:: path
   :noindex:

pow
^^^

.. autofunction:: pow
   :noindex:

regular
^^^^^^^

.. autofunction:: regular
   :noindex:

scalar
^^^^^^

.. autofunction:: scalar
   :noindex:

sort
^^^^

.. autofunction:: sort
   :noindex:

square
^^^^^^

.. autofunction:: square
   :noindex:

sub_circuit
^^^^^^^^^^^

.. autofunction:: sub_circuit
   :noindex:

sub_path
^^^^^^^^

.. autofunction:: sub_path
   :noindex:

sum
^^^

.. autofunction:: sum
   :noindex:

table
^^^^^

.. autofunction:: table
   :noindex:

times
^^^^^

.. autofunction:: times
   :noindex:

tree
^^^^

.. autofunction:: tree
   :noindex:


Set constraints
---------------

All constraints over set variables in the `SetConstraintFactory` abstract class, which is implemented by the `Model`
class. Set constraints have the `set_` prefix, indeed, as several set constraints have the same name as int constraints,
we made the choice to semantically distinguish them, contrarily to the Choco Java API, as method Python does not support
method overloading.

.. py:currentmodule:: pychoco.constraints.set_constraint_factory.SetConstraintFactory

set_union
^^^^^^^^^

.. autofunction:: set_union
   :noindex:

set_union_indices
^^^^^^^^^^^^^^^^^

.. autofunction:: set_union_indices
   :noindex:

set_intersection
^^^^^^^^^^^^^^^^

.. autofunction:: set_intersection
   :noindex:

set_subset_eq
^^^^^^^^^^^^^

.. autofunction:: set_subset_eq
   :noindex:

set_nb_empty
^^^^^^^^^^^^

.. autofunction:: set_nb_empty
   :noindex:

set_offset
^^^^^^^^^^

.. autofunction:: set_offset
   :noindex:

set_not_empty
^^^^^^^^^^^^^

.. autofunction:: set_not_empty
   :noindex:

set_sum_element
^^^^^^^^^^^^^^^

.. autofunction:: set_sum_element
   :noindex:

set_max
^^^^^^^

.. autofunction:: set_max
   :noindex:

set_max_indices
^^^^^^^^^^^^^^^

.. autofunction:: set_max_indices
   :noindex:

set_min
^^^^^^^^^^^^^^^^^

.. autofunction:: set_union_indices
   :noindex:

set_min_indices
^^^^^^^^^^^^^^^

.. autofunction:: set_min_indices
   :noindex:

set_bools_channeling
^^^^^^^^^^^^^^^^^^^^

.. autofunction:: set_bools_channeling
   :noindex:

set_ints_channeling
^^^^^^^^^^^^^^^^^^^

.. autofunction:: set_ints_channeling
   :noindex:

set_disjoint
^^^^^^^^^^^^^^^^^

.. autofunction:: set_union_indices
   :noindex:

set_all_disjoint
^^^^^^^^^^^^^^^^

.. autofunction:: set_all_disjoint
   :noindex:

set_all_different
^^^^^^^^^^^^^^^^^

.. autofunction:: set_all_different
   :noindex:

set_all_equal
^^^^^^^^^^^^^

.. autofunction:: set_all_equal
   :noindex:

set_partition
^^^^^^^^^^^^^

.. autofunction:: set_partition
   :noindex:

set_inverse_set
^^^^^^^^^^^^^^^

.. autofunction:: set_inverse_set
   :noindex:

set_symmetric
^^^^^^^^^^^^^

.. autofunction:: set_symmetric
   :noindex:

set_element
^^^^^^^^^^^

.. autofunction:: set_element
   :noindex:

set_member_set
^^^^^^^^^^^^^^

.. autofunction:: set_member_set
   :noindex:

set_member_int
^^^^^^^^^^^^^^

.. autofunction:: set_member_int
   :noindex:

set_not_member_int
^^^^^^^^^^^^^^^^^^

.. autofunction:: set_not_member_int
   :noindex:

set_le
^^^^^^

.. autofunction:: set_le
   :noindex:

set_lt
^^^^^^

.. autofunction:: set_lt
   :noindex:
