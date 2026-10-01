.. _custom_search:

Custom search strategies
========================

PyChoco lets you define your own search strategy directly in Python.
A search strategy is made of two components:

* a **variable selector** that chooses which variable to branch on next;
* a **value selector** that chooses which value to try first for that variable.

When to use a custom search strategy
-------------------------------------

Custom search strategies are useful when:

* none of the built-in heuristics (``set_min_dom_lb_search``,
  ``set_input_order_lb_search``, etc.) fit your problem structure;
* you want to exploit domain-specific knowledge to guide the search;
* you are experimenting with new branching rules.

.. note::

   Each call to a Python selector crosses the Python/C/Java boundary.
   For performance-critical models, prefer built-in strategies.

.. tip::

   If your selectors need to maintain a counter or flag that is reset on
   backtrack, use a :ref:`backtrackable state object <backtrackable_state>`
   created with :meth:`~pychoco.model.Model.make_state_int` or
   :meth:`~pychoco.model.Model.make_state_bool`.

Basic usage
-----------

Call :func:`~pychoco.solver.Solver.set_custom_search` on the solver object,
passing the list of variables to branch on, a variable selector, and a value
selector:

.. code-block:: python

    from pychoco import Model

    model = Model()
    x = model.intvar(0, 10, "x")
    y = model.intvar(0, 10, "y")

    def var_selector(variables):
        # Pick the variable with the smallest current domain
        unfix = [v for v in variables if v.get_lb() != v.get_ub()]
        return min(unfix, key=lambda v: v.get_ub() - v.get_lb()) if unfix else None

    def val_selector(var):
        # Try the lower bound first
        return var.get_lb()

    solver = model.get_solver()
    solver.set_custom_search([x, y], var_selector, val_selector)
    while solver.solve():
        print(x.get_value(), y.get_value())

Variable selector
-----------------

The variable selector has signature:

.. code-block:: python

    def var_selector(variables: List[IntVar]) -> Optional[IntVar]

* ``variables`` is the list passed to ``set_custom_search`` (always the full
  original list, live Java references whose domains reflect the current search
  state).
* Return one of the variables from the list to branch on it next.
* Return ``None`` when all variables are already fixed; the solver will then
  declare the current assignment a solution.

Checking whether a variable is already fixed:

.. code-block:: python

    def var_selector(variables):
        unfix = [v for v in variables if v.get_lb() != v.get_ub()]
        return unfix[0] if unfix else None

Value selector
--------------

The value selector has signature:

.. code-block:: python

    def val_selector(var: IntVar) -> int

* ``var`` is the variable chosen by the variable selector.
* Return the integer value to try first (the left branch will be ``var == value``).

.. note::

   Use :ref:`filtering methods <filtering_methods>` (``get_lb()``, ``get_ub()``)
   to query the current domain of any variable inside the selectors.

.. _filtering_methods:

Domain query methods on IntVar
------------------------------

Both selectors can call the following methods on any
:class:`~pychoco.variables.intvar.IntVar`:

**Read-only (domain inspection)**

+------------------------------+--------------------------------------------------------------+
| Method                       | Description                                                  |
+==============================+==============================================================+
| ``x.get_lb()``               | Current lower bound of ``x``.                                |
+------------------------------+--------------------------------------------------------------+
| ``x.get_ub()``               | Current upper bound of ``x``.                                |
+------------------------------+--------------------------------------------------------------+
| ``x.get_value()``            | Value of ``x`` — only call when ``x`` is instantiated        |
|                              | (i.e. ``x.get_lb() == x.get_ub()``).                        |
+------------------------------+--------------------------------------------------------------+
| ``x.has_enumerated_domain()``| ``True`` if the domain is stored as an enumeration.          |
+------------------------------+--------------------------------------------------------------+
| ``x.get_domain_values()``    | List of all values in the domain (only for enumerated        |
|                              | domains).                                                    |
+------------------------------+--------------------------------------------------------------+

**Testing whether a variable is fixed**

A variable is fixed when its lower bound equals its upper bound:

.. code-block:: python

    def is_fixed(v):
        return v.get_lb() == v.get_ub()

.. warning::

   Do **not** use Python's ``==`` operator directly between two
   :class:`~pychoco.variables.intvar.IntVar` objects — it returns a
   :class:`~pychoco.variables.boolvar.BoolVar` (a reification of the
   equality constraint), not a Python ``bool``.  Use ``is`` for
   identity comparisons and ``get_lb()`` / ``get_ub()`` for domain
   queries.

Full example — n-queens with smallest-domain heuristic
-------------------------------------------------------

.. code-block:: python

    from pychoco import Model

    n = 8
    model = Model()
    queens = [model.intvar(0, n - 1, f"q{i}") for i in range(n)]
    model.all_different(queens).post()
    for i in range(n):
        for j in range(i + 1, n):
            model.arithm(queens[i], "!=", queens[j], "+", j - i).post()
            model.arithm(queens[i], "!=", queens[j], "-", j - i).post()

    def var_selector(variables):
        unfix = [v for v in variables if v.get_lb() != v.get_ub()]
        return min(unfix, key=lambda v: v.get_ub() - v.get_lb()) if unfix else None

    def val_selector(var):
        return var.get_lb()

    solver = model.get_solver()
    solver.set_custom_search(queens, var_selector, val_selector)
    if solver.solve():
        print([q.get_value() for q in queens])

API reference
-------------

.. py:currentmodule:: pychoco.solver

.. automethod:: Solver.set_custom_search
   :noindex:
