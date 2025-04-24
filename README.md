# pychoco

[![ubuntu_build](https://github.com/chocoteam/pychoco/actions/workflows/ubuntu.yml/badge.svg)](https://github.com/chocoteam/pychoco/actions)
[![macos_build](https://github.com/chocoteam/pychoco/actions/workflows/macos.yml/badge.svg)](https://github.com/chocoteam/pychoco/actions)
[![windows_build](https://github.com/chocoteam/pychoco/actions/workflows/windows.yml/badge.svg)](https://github.com/chocoteam/pychoco/actions)
[![codecov](https://codecov.io/gh/chocoteam/pychoco/branch/master/graph/badge.svg?token=JRW8NQG8I7)](https://codecov.io/gh/chocoteam/pychoco)
[![PyPI version](https://badge.fury.io/py/pychoco.svg)](https://pypi.org/project/pychoco/)
[![Documentation Status](https://readthedocs.org/projects/pychoco/badge/?version=latest)](https://pychoco.readthedocs.io/en/latest/?badge=latest)
[![PyPI Downloads](https://static.pepy.tech/badge/pychoco)](https://pepy.tech/projects/pychoco)
[![License](https://img.shields.io/badge/License-BSD_4--Clause-blue.svg)](https://directory.fsf.org/wiki/License:BSD-4-Clause)

*Current choco-solver version: 4.10.17*

Python bindings for the Choco Constraint programming solver (https://choco-solver.org/).

Choco-solver is an open-source Java library for Constraint Programming (see https://choco-solver.org/).
It comes with many features such as various types of variables, various state-of-the-art constraint,
various search strategies, etc.

The pychoco library uses a *native-build* of the original Java Choco-solver library, in the form
of a shared library, which means that it can be used without any JVM. This native-build is created
with [GraalVM](https://www.graalvm.org/) native-image tool.

We heavily relied on [JGraphT Python bindings](https://python-jgrapht.readthedocs.io/) source code to
understand how such a thing could be achieved, so many thanks to JGraphT authors!

## Installation

We automatically build 64-bit wheels for Python versions >= 3.6 on Linux, Windows and
MacOSX. They can be directly downloaded from PyPI (https://pypi.org/project/pychoco/) or using pip:

    pip install pychoco

## Documentation

If you do not have any knowledge about Constraint Programming (CP) and Choco-solver, you can have a look at 
https://choco-solver.org/tutos/ for a quick introduction to CP and to Choco-solver features. For this Python API,
we also provide an API documentation which is available online at https://pychoco.readthedocs.io/ .

You can also have a look at the **pychoco Cheat Sheet** : [pychoco cheat sheet](./docs/pychoco-cheatsheet.pdf)

## Quickstart

pychoco's API is quite close to Choco's Java API. The first thing to do is to import the
library and create a model object:

```python
from pychoco import Model

model = Model("My Choco Model")
```

Then, you can use this model object to create variables:

```python
intvars = model.intvars(10, 0, 10)
sum_var = model.intvar(0, 100)
```

You can also create views from this Model object:

```python
b6 = model.int_ge_view(intvars[6], 6)
```

Create and post (or reify) constraints:

```python
model.all_different(intvars).post()
model.sum(intvars, "=", sum_var).post()
b7 = model.arithm(intvars[7], ">=", 7).reify()
```

Solve your problem:

```python
model.get_solver().solve()
```

And retrieve the solution:

```python
print("intvars = {}".format([i.get_value() for i in intvars]))
print("sum = {}".format(sum_var.get_value()))
print("intvar[6] >= 6 ? {}".format(b6.get_value()))
print("intvar[7] >= 7 ? {}".format(b7.get_value()))
```

```
> intvars = [3, 5, 9, 6, 7, 2, 0, 1, 4, 8]
> sum = 45
> intvar[6] >= 6 ? False
> intvar[7] >= 7 ? False
```

## Build from source

The following system dependencies are required to build PyChco from sources:

- GraalVM >= 22 (see https://www.graalvm.org/)
- Native Image component for GraalVM (see https://www.graalvm.org/22.1/reference-manual/native-image/)
- Apache Maven (see https://maven.apache.org/)
- Python >= 3.6 (see https://www.python.org/)
- SWIG >= 3 (see https://www.swig.org/)

Once these dependencies are satisfied, clone the current repository:

    git clone --recurse-submodules https://github.com/chocoteam/pychoco.git

The `--recurse-submodules` is necessary as the `choco-solver-capi` is a separate git project included
as a submodule (see https://github.com/chocoteam/choco-solver-capi). It contains all the necessary
to compile Choco-solver as a shared native library using GraalVM native-image.

Ensure that the `$JAVA_HOME` environment variable is pointing to GraalVM, and from the cloned repository
execute the following command:

    sh build.sh

This command will compile Choco-solver into a shared native library and compile the Python bindings
to this native API using SWIG.

Finally, run:

    pip install .

And voilà !

## Citation

Coming soon.

## Getting help or contribute

We do our best to maintain pychoco and keep it up-to-date with choco-solver. However, if you see missing
features, if you have any questions about using the library, suggestions for improvements, or if you
detect a bug, please [open an issue](https://github.com/chocoteam/pychoco/issues/new/choose).
