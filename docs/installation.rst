.. _install:

Installation
============

We are still in the process of implementing and releasing PyChoco. So currently the only way to install
it and try it is to follow the entire build-from-source process. However, we plan to release pre-built
Python wheels for various operating systems. Stay tuned!

Installation from PyPI
----------------------

We automatically build 64-bit wheels for Python versions 3.6, 3.7, 3.8, 3.9, and 3.10 on Linux, Windows and
MacOSX. They can be directly downloaded from PyPI (https://pypi.org/project/pychoco/) or using pip:

    $ pip install pychoco

Build from source
-----------------

The following system dependencies are required to build PyChco from sources:

- GraalVM >= 20 (see https://www.graalvm.org/)
- Native Image component for GraalVM (see https://www.graalvm.org/22.1/reference-manual/native-image/)
- Apache Maven (see https://maven.apache.org/)
- Python >= 3.6 (see https://www.python.org/)
- SWIG >= 3 (see https://www.swig.org/)

Once these dependencies are satisfied, clone the current repository::

    $ git clone --recurse-submodules https://github.com/dimitri-justeau/pychoco.git

The `--recurse-submodules` is necessary as the `choco-solver-capi` is a separate git project included
as a submodule (see https://github.com/dimitri-justeau/choco-solver-capi). It contains all the necessary
to compile Choco-solver as a shared native library using GraalVM native-image.

Ensure that the `$JAVA_HOME` environment variable is pointing to GraalVM, and from the cloned repository
execute the following command::

    $ sh build.sh

This command will compile Choco-solver into a shared native library and compile the Python bindings
to this native API using SWIG.

Finally, run::

    $ pip install .

And voilà !
