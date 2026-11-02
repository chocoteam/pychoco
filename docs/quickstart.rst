.. _quickstart:

Quickstart
==========

Pychoco's API is quite close to Choco's Java API. The first thing to do is to import the
library and create a model object:

.. code-block:: python

    from pychoco import Model

    model = Model("My Choco Model")

Then, you can use this model object to create variables:

.. code-block:: python

    intvars = model.intvars(10, 0, 10)
    sum_var = model.intvar(0, 100)


You can also create views from this Model object:

.. code-block:: python

    b6 = model.int_ge_view(intvars[6], 6)


Create and post (or reify) constraints:

.. code-block:: python

    model.all_different(intvars).post()
    model.sum(intvars, "=", sum_var).post()
    b7 = model.arithm(intvars[7], ">=", 7).reify()

Solve your problem:

.. code-block:: python

    model.get_solver().solve()


And retrieve the solution:

.. code-block:: python

    print("intvars = {}".format([i.get_value() for i in intvars]))
    print("sum = {}".format(sum_var.get_value()))
    print("intvar[6] >= 6 ? {}".format(b6.get_value()))
    print("intvar[7] >= 7 ? {}".format(b7.get_value()))

    > "intvars = [3, 5, 9, 6, 7, 2, 0, 1, 4, 8]"
    > "sum = 45"
    > "intvar[6] >= 6 ? False"
    > "intvar[7] >= 7 ? False"

Note that the solver keeps its search state between two resolutions: a new call to ``solve()``
or to one of the ``find_*()`` methods resumes the search where the previous one stopped (for
instance, a second ``find_optimal_solution()`` returns ``None``). Call ``reset()`` to run an
independent resolution, or ``hard_reset()`` to also discard the search strategy, the restart policy,
the hints and the search monitors:

.. code-block:: python

    solver = model.get_solver()
    s1 = solver.find_optimal_solution(sum_var, False)
    solver.reset()
    s2 = solver.find_optimal_solution(sum_var, False)  # same optimum as s1
