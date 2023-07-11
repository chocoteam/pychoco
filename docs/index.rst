Pychoco
=======

Python bindings for the Choco Constraint programming solver (https://choco-solver.org/).

Choco-solver is an open-source Java library for Constraint Programming (see https://choco-solver.org/).
It comes with many features such as various types of variables, various state-of-the-art constraint,
various search strategies, etc.

The PyChoco library uses a *native-build* of the original Java Choco-solver library, in the form
of a shared library, which means that it can be used without any JVM. This native-build is created
with GraalVM (https://www.graalvm.org/) native-image tool.

We heavily relied on JGraphT Python bindings (https://python-jgrapht.readthedocs.io/) source code to
understand how such a thing could be achieved, so many thanks to JGraphT authors!

Documentation
=============

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   api/index

Notebooks
=========

.. nbgallery::
    notebooks/graph_colouring

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
