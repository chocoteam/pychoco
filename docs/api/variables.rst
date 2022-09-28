.. _variables:

Variables
=========

A variable is an unknown, mathematically speaking. The goal of a resolution is to assign a value to each variable.
The domain of a variable –set of values it may take– must be defined in the model. Currently, PyChoco supports boolean
variables (BoolVar), integer variables (IntVar), and set variables (SetVar). Variables are created using a `Model`
object (see :ref:`model`). When creating a variable, the user can specify a name to help reading the output.

Variable
--------

The `Variable` class is the superclass of all classes, it contains generic methods and property
that are common to all types of variables.

.. autoclass:: pychoco.variables.variable.Variable
   :members:
   :undoc-members:
   :noindex:

IntVar
------

Integer variables represent a integer value, and can be created from a Model object using the following methods:

.. autofunction:: pychoco.variables.variable_factory.VariableFactory.intvar
   :noindex:

.. autofunction:: pychoco.variables.variable_factory.VariableFactory.intvars
   :noindex:

Integer variables also include additional parameters and methods to the generic Variable class:

.. autoclass:: pychoco.variables.intvar.IntVar
   :members:
   :undoc-members:
   :noindex:

Operations between IntVars
^^^^^^^^^^^^^^^^^^^^^^^^^^

We took advantage of operators overloading in Python to provide some shortcuts in pychoco, so you can use the
following operators between IntVars and ints.

- `c = a + b`: c is and IntVar constrained to be equal to a + b (see `arithm` constraint in :ref:`constraints`).
- `c = a - b`: c is and IntVar constrained to be equal to a - b (see `arithm` constraint in :ref:`constraints`).
- `c = a * b`: c is and IntVar constrained to be equal to a * b (see `arithm` constraint in :ref:`constraints`).
- `c = a / b`: c is and IntVar constrained to be equal to a / b (see `arithm` constraint in :ref:`constraints`).
- `c = -a`: c is an `int_minus_view` (see ref:`views`)
- `c = a % b`: c is the result rest of the integer division betwen a and b (see `mod` constraint in :ref:`constraints`).
- `c = a ** c` c is equal to pow(a, c), c must be an int (see `pow` constraint in :ref:`constraints`).
- `c = a == b` c is a BoolVar, which is True only if a == b.
- `c = a <= b` c is a BoolVar, which is True only if a <= b.
- `c = a < b` c is a BoolVar, which is True only if a < b.
- `c = a >= b` c is a BoolVar, which is True only if a >= b.
- `c = a > b` c is a BoolVar, which is True only if a > b.
- `c = a != b` c is a BoolVar, which is True only if a != b.

BoolVar
-------

Boolean variables represent a boolean value (0/1 or False/True). They are a special case of integer variables where the
domain is restricted to [0, 1], and can be created from a Model object using the following methods:

.. autofunction:: pychoco.variables.variable_factory.VariableFactory.boolvar
   :noindex:

.. autofunction:: pychoco.variables.variable_factory.VariableFactory.boolvars
   :noindex:

Boolean variables also include additional parameters and methods to the generic Variable class:

.. autoclass:: pychoco.variables.boolvar.BoolVar
   :members:
   :inherited-members:
   :undoc-members:
   :noindex:

Operations between BoolVars
^^^^^^^^^^^^^^^^^^^^^^^^^^^

We took advantage of operators overloading in Python to provide some shortcuts in pychoco, so you can use the
following operators between BoolVars and bools.

- `b = b1 & b2`: b is a BoolVar which is True only if b1 and b2 are True (see `and_` constraint in :ref:`constraints`).
- `b = b1 | b2`: b is a BoolVar which is True only if b1 or b2 is True (see `or_` constraint in :ref:`constraints`).
- `b = ~b1`: b is a `bool_not_view` over b1 (see :ref:`views`).
- `b = b1 == b2` is a BoolVar which is True only if `b1 == b2`.
- `b = b1 != b2` is a BoolVar which is True only if `b1 != b2`.

SetVar
------

Set variables represent a set of integers, which value must belong to a set interval [lb, ub].
The lower bound lb is the set of mandatory values (or kernel) for any instantiation of the variable,
while the upper bound ub is the set of potential values (or envelope) for any instantiation of the
variable. Set variables can be created from a model object using the following method:

.. autofunction:: pychoco.variables.variable_factory.VariableFactory.setvar
   :noindex:

Set variables also include additional parameters and methods the generic Variable class:

.. autoclass:: pychoco.variables.setvar.SetVar
   :members:
   :inherited-members:
   :undoc-members:
   :noindex:

GraphVar
--------

Graph variables represent a graph (directed or undirected), which value must belong to a graph interval [lb, ub].
The lower bound lb (or kernel) is a graph that must be included in any instantiation of the variable,
while the upper bound ub (or envelope) is such that any instantiation of the
variable is a subgraph of it.

The bounds of a graph variable must be created using the graph API of pychoco (see below).

Undirected Graph variables can be created from a model object using the following methods:

.. autofunction:: pychoco.variables.variable_factory.VariableFactory.graphvar
   :noindex:

.. autofunction:: pychoco.variables.variable_factory.VariableFactory.node_induced_graphvar
   :noindex:

Undirected variables also include additional parameters and methods the generic Variable class:

.. autoclass:: pychoco.variables.undirected_graphvar.UndirectedGraphVar
   :members:
   :inherited-members:
   :undoc-members:
   :noindex:

Directed Graph variables can be created from a model object using the following methods:

.. autofunction:: pychoco.variables.variable_factory.VariableFactory.digraphvar
   :noindex:

.. autofunction:: pychoco.variables.variable_factory.VariableFactory.node_induced_digraphvar
   :noindex:

Directed variables also include additional parameters and methods the generic Variable class:

.. autoclass:: pychoco.variables.directed_graphvar.DirectedGraphVar
   :members:
   :inherited-members:
   :undoc-members:
   :noindex:

UndirectedGraph API
^^^^^^^^^^^^^^^^^^^

The `create_undirected_graph` factory function allows to instantiate a directed graph
from a list of nodes and a list of edges:

.. autofunction:: pychoco.objects.graphs.undirected_graph.create_undirected_graph
   :noindex:

This function returns an `UndirectedGraph` object:

.. autoclass:: pychoco.objects.graphs.undirected_graph.UndirectedGraph
   :members:
   :inherited-members:
   :undoc-members:
   :noindex:

DirectedGraph API
^^^^^^^^^^^^^^^^^^^

The `create_directed_graph` factory function allows to instantiate a directed graph
from a list of nodes and a list of edges:

.. autofunction:: pychoco.objects.graphs.directed_graph.create_directed_graph
   :noindex:

This function returns a `DirectedGraph` object:

.. autoclass:: pychoco.objects.graphs.directed_graph.DirectedGraph
   :members:
   :inherited-members:
   :undoc-members:
   :noindex: