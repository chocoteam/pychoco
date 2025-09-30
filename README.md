# pychoco

[![ubuntu_build](https://github.com/chocoteam/pychoco/actions/workflows/ubuntu.yml/badge.svg)](https://github.com/chocoteam/pychoco/actions)
[![macos_build](https://github.com/chocoteam/pychoco/actions/workflows/macos.yml/badge.svg)](https://github.com/chocoteam/pychoco/actions)
[![windows_build](https://github.com/chocoteam/pychoco/actions/workflows/windows.yml/badge.svg)](https://github.com/chocoteam/pychoco/actions)
[![codecov](https://codecov.io/gh/chocoteam/pychoco/branch/master/graph/badge.svg?token=JRW8NQG8I7)](https://codecov.io/gh/chocoteam/pychoco)
[![PyPI version](https://badge.fury.io/py/pychoco.svg)](https://pypi.org/project/pychoco/)
[![Documentation Status](https://readthedocs.org/projects/pychoco/badge/?version=latest)](https://pychoco.readthedocs.io/en/latest/?badge=latest)
[![PyPI Downloads](https://static.pepy.tech/badge/pychoco)](https://pepy.tech/projects/pychoco)
[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/license/bsd-3-clause)
[![DOI](https://joss.theoj.org/papers/10.21105/joss.08847/status.svg)](https://doi.org/10.21105/joss.08847)

*Current choco-solver version: 4.10.18*

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
https://choco-solver.org/tutos/ for a quick introduction to CP and to Choco-solver features.
The tutorial in this website includes both Java and Python examples.
For this Python API, we also provide an API documentation which is available online at https://pychoco.readthedocs.io/.

You can also have a look at the **pychoco Cheat Sheet** : [pychoco cheat sheet](./docs/pychoco-cheatsheet.pdf)

Finally, we designed a few **notebooks examples** that you can find in the `examples` directory.

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

## Configuring search

### Generic search strategies

Currently, the main limitation of pychoco is the customization of search strategies, which is not as
advanced as the Java version. This is mainly due to the fact that pychoco's need to rely on a compiled C
entrypoint to Choco-solver, which does not allow Python routines to be injected into the solving procedure.
One possible solution would be to implement a parsing system to define custom search strategy in Choco-solver,
and rely on this system in pychoco. However, this represents a considerable amount of work that we cannot commit to
in the short term. **Note:** please do not hesitate to let us know, or open a pull request if you want to implement
this feature, or suggest an alternative solution.

However, it is possible to rely on the generic search heuristics available in Choco-solver, through the
Solver object. Currently available search strategies are: `default_search`, `dom_over_w_deg_search`,
`dom_over_w_deg_ref_search`, `activity_based_search`, `min_dom_lb_search`, `min_dom_ub_search`,
`random_search`, `conflict_history_search`, `input_order_lb_search`, `input_order_ub_search`,
`failure_length_based_search`, `failure_rate_based_search`, `pick_on_dom_search`, `pick_on_fil_search`.

Example:

```python
solver.set_dom_over_w_deg_search(decision_variables)
```

### Hints

Hints can improve the search procedure by defining a partial solution and drive the search
toward a solution. Hints apply on integer variables, and consist of couples of (variable, value).

Example:

```python
solver.add_hint(cost, min_cost)
```

### Parallel portfolio

The parallel portfolio is a powerful feature of Choco-solver which allows to solve a problem
in parallel with different search strategies. Each solving thread can inform other when he
finds a solution, leading them to update their bounds in case of an optimization process.
To set up a parallel portfolio, it is necessary to construct as many identical models as
the number of threads. This feature can very efficient to boost the optimization procedure.

Example:

```python
from pychoco.model import Model
from pychoco.parallel_portfolio import ParallelPortfolio

pf = ParallelPortfolio()
pf.steal_nogoods_on_restarts()
for i in range(0, 5):
    m = Model()
    vars = m.intvars(10, 0, 100)
    nv = m.intvar(3, 4)
    m.n_values(vars, nv).post()
    s = m.intvar(0, 1000)
    m.sum(vars, "=", s).post()
    m.set_objective(s, True)
    pf.add_model(m)
sol = pf.find_best_solution()
```

## Build from source

The following system dependencies are required to build pychoco from sources:

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

Justeau-Allaire D, Prud’homme C (2025). pychoco: all-inclusive Python bindings for the Choco-solver constraint programming library. Journal of Open Source Software, 10(113), 8847, https://doi.org/10.21105/joss.08847

## Getting help or contribute

We do our best to maintain pychoco and keep it up-to-date with choco-solver. However, if you see missing
features, if you have any questions about using the library, suggestions for improvements, or if you
detect a bug, please [open an issue](https://github.com/chocoteam/pychoco/issues/new/choose).
