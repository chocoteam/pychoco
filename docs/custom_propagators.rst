.. _custom_propagators:

Custom propagators
==================

PyChoco allows you to write custom constraint propagators directly in Python.
A propagator is the filtering algorithm behind a constraint: it is called by
the solver during search and removes values from variable domains that cannot
lead to a solution.

When to use a custom propagator
--------------------------------

Custom propagators are useful when:

* you need a constraint that is not available in PyChoco's built-in set;
* you want to prototype a new filtering rule quickly before implementing it in Java;
* you are teaching or experimenting with constraint programming.

.. note::

   Each call to a Python propagator crosses the Python/C/Java boundary.
   For performance-critical models, prefer built-in constraints or implement
   the propagator in Java and expose it via the C API.

Basic usage
-----------

A custom propagator is defined as a plain Python function whose parameters
are the :class:`~pychoco.variables.intvar.IntVar` objects it operates on,
in the same order as the list passed to
:func:`~pychoco.constraints.int_constraint_factory.IntConstraintFactory.custom_constraint`.

.. code-block:: python

    from pychoco import Model

    model = Model()
    x = model.intvar(0, 10, "x")
    y = model.intvar(0, 10, "y")

    def propagator(x, y):
        # Enforce x <= y by filtering the upper bound of x
        x.update_ub(y.get_ub())

    model.custom_constraint([x, y], propagator).post()

    solver = model.get_solver()
    while solver.solve():
        print(x.get_value(), "<=", y.get_value())

The propagator is called automatically by the solver whenever the domains of
the listed variables change.

Filtering methods on IntVar
---------------------------

Inside a propagator, you can read and reduce variable domains using the
following methods on :class:`~pychoco.variables.intvar.IntVar`:

+---------------------------+----------------------------------------------------+
| Method                    | Effect                                             |
+===========================+====================================================+
| ``x.get_lb()``            | Returns the current lower bound of ``x``.          |
+---------------------------+----------------------------------------------------+
| ``x.get_ub()``            | Returns the current upper bound of ``x``.          |
+---------------------------+----------------------------------------------------+
| ``x.update_lb(v)``        | Tightens the lower bound of ``x`` to ``v``.        |
+---------------------------+----------------------------------------------------+
| ``x.update_ub(v)``        | Tightens the upper bound of ``x`` to ``v``.        |
+---------------------------+----------------------------------------------------+
| ``x.instantiate_to(v)``   | Fixes ``x`` to the single value ``v``.             |
+---------------------------+----------------------------------------------------+
| ``x.remove_value(v)``     | Removes the value ``v`` from the domain of ``x``.  |
+---------------------------+----------------------------------------------------+

All filtering methods raise :class:`~pychoco.exceptions.Contradiction`
automatically if the operation would empty the domain.

Signalling a contradiction
--------------------------

The solver backtracks automatically when a domain becomes empty.  You can also
trigger backtracking explicitly by raising
:class:`~pychoco.exceptions.Contradiction`:

.. code-block:: python

    from pychoco.exceptions import Contradiction

    def propagator(x, y):
        if x.get_lb() > y.get_ub():
            raise Contradiction()

Full example — partial sum filtering
-------------------------------------

The following propagator enforces ``z <= x + y`` and ``z >= x + y`` (i.e.
``z = x + y``) using only bound filtering:

.. code-block:: python

    from pychoco import Model

    model = Model()
    x = model.intvar(0, 5, "x")
    y = model.intvar(0, 5, "y")
    z = model.intvar(0, 10, "z")

    def sum_prop(x, y, z):
        z.update_ub(x.get_ub() + y.get_ub())
        z.update_lb(x.get_lb() + y.get_lb())
        x.update_ub(z.get_ub() - y.get_lb())
        x.update_lb(z.get_lb() - y.get_ub())
        y.update_ub(z.get_ub() - x.get_lb())
        y.update_lb(z.get_lb() - x.get_ub())

    model.custom_constraint([x, y, z], sum_prop).post()

    solver = model.get_solver()
    if solver.solve():
        print(x.get_value(), "+", y.get_value(), "=", z.get_value())

Maintaining state across the search tree
-----------------------------------------

A plain Python closure variable is **not** backtracked when the solver
backtracks.  If your propagator needs a counter or flag that stays consistent
with the current search node, use a
:ref:`backtrackable state object <backtrackable_state>`:

.. code-block:: python

    counter = model.make_state_int(0)  # reset automatically on backtrack

    def propagator(x, y):
        counter.add(1)
        x.update_ub(y.get_ub())

    model.custom_constraint([x, y], propagator).post()

See :doc:`backtrackable_state` for the full API.

API reference
-------------

.. py:currentmodule:: pychoco.constraints.int_constraint_factory.IntConstraintFactory

.. autofunction:: custom_constraint
   :noindex:

.. autoclass:: pychoco.exceptions.Contradiction
   :members:
   :noindex:
