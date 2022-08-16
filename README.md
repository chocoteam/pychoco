# PyChoco

[![ubuntu_build](https://github.com/dimitri-justeau/pychoco/actions/workflows/ubuntu.yml/badge.svg)](https://github.com/dimitri-justeau/pychoco/actions)
[![codecov](https://codecov.io/gh/dimitri-justeau/pychoco/branch/master/graph/badge.svg?token=JRW8NQG8I7)](https://codecov.io/gh/dimitri-justeau/pychoco)

Python bindings for the Choco Constraint programming solver (https://choco-solver.org/).

Choco-solver is an open-source Java library for Constraint Programming (see https://choco-solver.org/).
It comes with many features such as various types of variables, various state-of-the-art constraint,
various search strategies, etc.

The PyChoco library uses a *native-build* of the original Java Choco-solver library, in the form
of a shared library, which means that it can be used without any JVM. This native-build is created
with [GraalVM](https://www.graalvm.org/) native-image tool.

We heavily relied on [JGraphT Python bindings](https://python-jgrapht.readthedocs.io/) source code to
understand how such a thing could be achieved, so many thanks to JGraphT authors!

## Installation

We are still in the process of implementing and releasing PyChoco. So currently the only way to install
it and try it is to follow the entire build-from-source process. However, we plan to release pre-built
Python wheels for various operating systems. Stay tuned!

## Build from source

The following system dependencies are required to build PyChco from sources:

- GraalVM >= 20 (see https://www.graalvm.org/)
- Native Image component for GraalVM (see https://www.graalvm.org/22.1/reference-manual/native-image/)
- Apache Maven (see https://maven.apache.org/)
- Python >= 3.6 (see https://www.python.org/)
- SWIG >= 3 (see https://www.swig.org/)

Once these dependencies are satisfied, clone the current repository:

    git clone --recurse-submodules https://github.com/dimitri-justeau/pychoco.git

The `--recurse-submodules` is necessary as the `choco-solver-capi` is a separate git project included
as a submodule (see https://github.com/dimitri-justeau/choco-solver-capi). It contains all the necessary
to compile Choco-solver as a shared native library using GraalVM native-image.

Ensure that the `$JAVA_HOME` environment variable is pointing to GraalVM, and from the cloned repository
execute the following command:

    sh build.sh

This command will compile Choco-solver into a shared native library and compile the Python bindings
to this native API using SWIG.

Finally, run:

    pip install .

And voilà !

## Quickstart

## Citation

## Getting help or contribute