.. _backtrackable_state:

Backtrackable state
===================

PyChoco exposes Choco's *backtrackable* state objects: integers and booleans
whose values are automatically restored when the solver backtracks.  They are
useful when you need to maintain counters, flags, or other mutable data inside
a :ref:`custom propagator <custom_propagators>` or a
:ref:`custom search strategy <custom_search>` that must stay consistent with
the current search node.

Creating backtrackable objects
-------------------------------

Both types are created from the model, which ties them to the solver's
environment (the component responsible for undo/redo on backtrack):

.. code-block:: python

    from pychoco import Model

    model = Model()
    counter = model.make_state_int(0)      # backtrackable int, starts at 0
    flag    = model.make_state_bool(False) # backtrackable bool, starts at False

StateInt — backtrackable integer
---------------------------------

.. code-block:: python

    s = model.make_state_int(10)

    s.get()          # → 10
    s.set(42)        # s is now 42
    s.add(8)         # s is now 50, returns 50
    s.value          # property: same as get()
    s.value = 3      # property: same as set(3)

**All mutations are backtracked** when the solver undoes a choice point.

StateBool — backtrackable boolean
----------------------------------

.. code-block:: python

    b = model.make_state_bool(False)

    b.get()          # → False
    b.set(True)      # b is now True
    b.value          # property: same as get()
    b.value = False  # property: same as set(False)

Using backtrackable state in a custom propagator
-------------------------------------------------

The example below counts how many times a propagator is called at each search
node.  Because ``counter`` is backtrackable, it is reset to the value it had
when the solver entered the current node whenever backtracking occurs.

.. code-block:: python

    from pychoco import Model

    model = Model()
    x = model.intvar(0, 5, "x")
    y = model.intvar(0, 5, "y")

    counter = model.make_state_int(0)

    def propagator(x, y):
        calls = counter.add(1)
        # enforce x <= y
        x.update_ub(y.get_ub())
        y.update_lb(x.get_lb())

    model.custom_constraint([x, y], propagator).post()

    solver = model.get_solver()
    while solver.solve():
        print(x.get_value(), y.get_value())

Using backtrackable state in a custom search strategy
------------------------------------------------------

The example below uses a flag to skip variables that have already been
explored in the current branch:

.. code-block:: python

    from pychoco import Model

    model = Model()
    queens = [model.intvar(0, 7, f"q{i}") for i in range(8)]
    model.all_different(queens).post()

    last_choice = model.make_state_int(-1)  # index of last branched variable

    def var_selector(variables):
        unfix = [v for v in variables if v.get_lb() != v.get_ub()]
        return min(unfix, key=lambda v: v.get_ub() - v.get_lb()) if unfix else None

    def val_selector(var):
        return var.get_lb()

    solver = model.get_solver()
    solver.set_custom_search(queens, var_selector, val_selector)
    if solver.solve():
        print([q.get_value() for q in queens])

.. note::

   Backtrackable objects are tied to the model's environment.  They **must**
   not be shared between models or used after the model is garbage-collected.

API reference
-------------

.. autoclass:: pychoco.state.StateInt
   :members:
   :noindex:

.. autoclass:: pychoco.state.StateBool
   :members:
   :noindex:

.. automethod:: pychoco.model.Model.make_state_int
   :noindex:

.. automethod:: pychoco.model.Model.make_state_bool
   :noindex:
