.. _views:

Views
=====

The concept of views in Constraint Programming is halfway between variables and constraints.
Specifically, a view is a special kind of variable that does not declare any domain, but instead relies on one or
several other variables through a logical relation. From a modelling perspective, a view can be manipulated exactly
as any other variable. In pychoco, the only difference that you will notice is that the `is_view()` method will
return True when a variable is actually a view.

Views are directly declared from a `Model` object (see :ref:`model`).

Boolean views
-------------

All constraints over integer and boolean variables are declared in the `IntConstraintFactory` abstract class,
which is implemented by the `Model` class.

.. py:currentmodule:: pychoco.constraints.int_constraint_factory.IntConstraintFactory

absolute
^^^^^^^^

.. autofunction:: absolute
   :noindex:

Integer views
-------------

All constraints over set variables in the `SetConstraintFactory` abstract class, which is implemented by the `Model`
class. Set constraints have the `set_` prefix, indeed, as several set constraints have the same name as int constraints,
we made the choice to semantically distinguish them, contrarily to the Choco Java API, as method Python does not support
method overloading.

.. py:currentmodule:: pychoco.constraints.set_constraint_factory.SetConstraintFactory

set_all_different
^^^^^^^^^^^^^^^^^

.. autofunction:: set_all_different
   :noindex:


Set views
---------
