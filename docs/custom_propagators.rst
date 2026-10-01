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

Two styles are available:

* **Functional style** — a plain Python function, concise for simple rules.
* **Class-based style** — a subclass of :class:`~pychoco.propagator.Propagator`,
  recommended when the propagator needs instance attributes or complex logic.

----

Functional style
----------------

Pass a plain Python function to
:func:`~pychoco.constraints.int_constraint_factory.IntConstraintFactory.custom_constraint`.
The function receives the :class:`~pychoco.variables.intvar.IntVar` objects as
positional arguments in the same order as the list:

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

----

Class-based style
-----------------

Subclass :class:`~pychoco.propagator.Propagator`, call
``super().__init__(intvars)`` in ``__init__``, and override
:meth:`~pychoco.propagator.Propagator.propagate`.  Variables are accessible as
``self.vars``.  Instance attributes work normally and persist across propagator
calls (but are **not** backtracked — see :ref:`backtrackable_state` for that).

.. code-block:: python

    from pychoco import Model, Propagator

    class BoundSync(Propagator):
        def __init__(self, x, y):
            super().__init__([x, y])
            self.call_count = 0          # plain Python attribute

        def propagate(self):
            self.call_count += 1
            self.vars[0].update_ub(self.vars[1].get_ub())

    model = Model()
    x = model.intvar(0, 10)
    y = model.intvar(0, 5)
    prop = BoundSync(x, y)
    prop.post()

    solver = model.get_solver()
    while solver.solve():
        print(x.get_value(), "<=", y.get_value())
    print("propagate() was called", prop.call_count, "times")

Call :meth:`~pychoco.propagator.Propagator.post` once to register the propagator
with its model.  Calling it a second time raises ``RuntimeError``.

Propagator priority
~~~~~~~~~~~~~~~~~~~

Both styles accept a ``priority`` parameter (default ``4 = LINEAR``):

.. code-block:: python

    # Functional style
    model.custom_constraint([x, y], fn, priority=2)

    # Class-based style
    class MyProp(Propagator):
        def __init__(self, x, y):
            super().__init__([x, y], priority=2)
        ...

Available priorities:

+----------+-------------+
| Value    | Name        |
+==========+=============+
| ``1``    | UNARY       |
+----------+-------------+
| ``2``    | BINARY      |
+----------+-------------+
| ``3``    | TERNARY     |
+----------+-------------+
| ``4``    | LINEAR      |
+----------+-------------+
| ``5``    | QUADRATIC   |
+----------+-------------+
| ``6``    | CUBIC       |
+----------+-------------+
| ``7``    | VERY_SLOW   |
+----------+-------------+

----

Filtering methods on IntVar
---------------------------

Inside a propagator, use the following methods to read and reduce variable
domains:

+---------------------------+----------------------------------------------------+
| Method                    | Effect                                             |
+===========================+====================================================+
| ``x.get_lb()``            | Returns the current lower bound of ``x``.          |
+---------------------------+----------------------------------------------------+
| ``x.get_ub()``            | Returns the current upper bound of ``x``.          |
+---------------------------+----------------------------------------------------+
| ``x.get_value()``         | Returns the value of ``x`` when it is fixed.       |
+---------------------------+----------------------------------------------------+
| ``x.is_fixed()``          | ``True`` if ``x`` has a single value in domain.    |
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

----

The ``is_entailed`` check
--------------------------

Both styles support an optional entailment check.  The solver uses it to
deactivate the propagator early when the constraint is guaranteed to be
satisfied (or violated):

* **Functional style** — pass a second function ``is_entailed_fn`` to
  :func:`~pychoco.constraints.int_constraint_factory.IntConstraintFactory.custom_constraint`.
* **Class-based style** — override
  :meth:`~pychoco.propagator.Propagator.is_entailed`.

The function / method receives the same variables as ``propagate`` (functional)
or ``self.vars`` (class-based) and must return:

* a **positive** integer — ``ESat.TRUE``
* ``0`` — ``ESat.UNDEFINED``
* a **negative** integer — ``ESat.FALSE``

.. warning::

   ``is_entailed`` must be **consistent** with ``propagate``.  Returning
   ``FALSE`` for a state that ``propagate`` left reachable causes Choco's
   solution validator to raise a fatal error.

.. code-block:: python

    # Class-based example
    class EvenOnly(Propagator):
        def propagate(self):
            for v in [1, 3]:
                if self.vars[0].get_lb() <= v <= self.vars[0].get_ub():
                    self.vars[0].remove_value(v)

        def is_entailed(self):
            x = self.vars[0]
            vals = (x.get_domain_values() if x.has_enumerated_domain()
                    else range(x.get_lb(), x.get_ub() + 1))
            return 1 if all(v % 2 == 0 for v in vals) else 0

----

Maintaining state across the search tree
-----------------------------------------

Instance attributes on a :class:`~pychoco.propagator.Propagator` subclass
(e.g. ``self.count``) are **not** backtracked — they keep their value even
when the solver backtracks to a previous node.  This is fine for counters,
logs, or caches that should accumulate across the whole search.

If you need a value that is **automatically restored on backtrack** (i.e. stays
consistent with the current search node), use a
:ref:`backtrackable state object <backtrackable_state>`:

.. code-block:: python

    class TrackedProp(Propagator):
        def __init__(self, x, y):
            super().__init__([x, y])
            # Backtracked automatically when the solver backtracks
            self._node_calls = x.model.make_state_int(0)

        def propagate(self):
            self._node_calls.add(1)
            self.vars[0].update_ub(self.vars[1].get_ub())

See :doc:`backtrackable_state` for the full API.

----

Full example — partial sum filtering
-------------------------------------

.. code-block:: python

    from pychoco import Model, Propagator

    class SumPropagator(Propagator):
        """Enforces z = x + y using bound filtering."""

        def __init__(self, x, y, z):
            super().__init__([x, y, z])

        def propagate(self):
            x, y, z = self.vars
            z.update_ub(x.get_ub() + y.get_ub())
            z.update_lb(x.get_lb() + y.get_lb())
            x.update_ub(z.get_ub() - y.get_lb())
            x.update_lb(z.get_lb() - y.get_ub())
            y.update_ub(z.get_ub() - x.get_lb())
            y.update_lb(z.get_lb() - x.get_ub())

        def is_entailed(self):
            x, y, z = self.vars
            lo = x.get_lb() + y.get_lb()
            hi = x.get_ub() + y.get_ub()
            if z.get_lb() == z.get_ub() == lo == hi:
                return 1   # TRUE: z is fixed to the only possible sum
            return 0       # UNDEFINED

    model = Model()
    x = model.intvar(0, 5, "x")
    y = model.intvar(0, 5, "y")
    z = model.intvar(0, 10, "z")

    SumPropagator(x, y, z).post()

    solver = model.get_solver()
    if solver.solve():
        print(x.get_value(), "+", y.get_value(), "=", z.get_value())

----

API reference
-------------

.. autoclass:: pychoco.propagator.Propagator
   :members: propagate, is_entailed, post
   :noindex:

.. py:currentmodule:: pychoco.constraints.int_constraint_factory.IntConstraintFactory

.. autofunction:: custom_constraint
   :noindex:

.. autoclass:: pychoco.exceptions.Contradiction
   :members:
   :noindex:
