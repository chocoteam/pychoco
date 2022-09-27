.. _views:

Views
=====

The concept of views in Constraint Programming is halfway between variables and constraints.
Specifically, a view is a special kind of variable that does not declare any domain, but instead relies on one or
several other variables through a logical relation. From a modelling perspective, a view can be manipulated exactly
as any other variable. In pychoco, the only difference that you will notice is that the `is_view()` method will
return True when a variable is actually a view.

Views are directly declared from a `Model` object (see :ref:`model`).

.. py:currentmodule:: pychoco.variables.view_factory.ViewFactory

Boolean views
-------------

Boolean view can be declared over several types of variables, and behave as Boolean variables.

bool_not_view
^^^^^^^^^^^^^

.. autofunction:: bool_not_view
   :noindex:

set_bool_view
^^^^^^^^^^^^^

.. autofunction:: set_bool_view
   :noindex:

set_bools_view
^^^^^^^^^^^^^^

.. autofunction:: set_bools_view
   :noindex:

Integer views
-------------

Integer view can be declared over several types of variables, and behave as Integer variables.

int_offset_view
^^^^^^^^^^^^^^^

.. autofunction:: int_offset_view
   :noindex:

int_minus_view
^^^^^^^^^^^^^^

.. autofunction:: int_minus_view
   :noindex:

int_scale_view
^^^^^^^^^^^^^^

.. autofunction:: int_scale_view
   :noindex:

int_abs_view
^^^^^^^^^^^^

.. autofunction:: int_abs_view
   :noindex:

int_affine_view
^^^^^^^^^^^^^^^

.. autofunction:: int_affine_view
   :noindex:

int_eq_view
^^^^^^^^^^^

.. autofunction:: int_eq_view
   :noindex:

int_ne_view
^^^^^^^^^^^

.. autofunction:: int_ne_view
   :noindex:

int_le_view
^^^^^^^^^^^

.. autofunction:: int_le_view
   :noindex:

int_ge_view
^^^^^^^^^^^

.. autofunction:: int_ge_view
   :noindex:

Set views
---------

Set view can be declared over several types of variables, and behave as Set variables.

bools_set_view
^^^^^^^^^^^^^^

.. autofunction:: bools_set_view
   :noindex:


ints_set_view
^^^^^^^^^^^^^

.. autofunction:: ints_set_view
   :noindex:

set_union_view
^^^^^^^^^^^^^^

.. autofunction:: set_union_view
   :noindex:

set_intersection_view
^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: set_intersection_view
   :noindex:

set_difference_view
^^^^^^^^^^^^^^^^^^^

.. autofunction:: set_difference_view
   :noindex:

graph_node_set_view
^^^^^^^^^^^^^^^^^^^

.. autofunction:: graph_node_set_view
   :noindex:

graph_successors_set_view
^^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: graph_successors_set_view
   :noindex:

graph_predecessors_set_view
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: graph_predecessors_set_view
   :noindex:

graph_neighbors_set_view
^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: graph_neighbors_set_view
   :noindex:


Graph views
-----------

node_induced_subgraph_view
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: node_induced_subgraph_view
   :noindex:

edge_induced_subgraph_view
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: edge_induced_subgraph_view
   :noindex:

graph_union_view
^^^^^^^^^^^^^^^^

.. autofunction:: graph_union_view
   :noindex:
