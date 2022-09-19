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

