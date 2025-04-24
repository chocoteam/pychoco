title: 'pychoco: all-inclusive Python bindings for the Choco-solver constraint programming library'
tags:
  - Python
  - bindings
  - native-image
  - constraint programming
  - constraint satisfaction problem
  - constraint optimisation problem
  - decision support
authors:
  - name: Dimitri Justeau-Allaire
    orcid: 0000-0003-4129-0764
    affiliation: 1
  - name: Charles Prud'homme
    orcid: 0000-0002-4546-9027
    affiliation: 2
    corresponding: true
affiliations:
  - name: AMAP, Univ Montpellier, CIRAD, CNRS, INRAE, IRD, Montpellier, France
    index: 1
  - name: TASC, IMT-Atlantique, LS2N-CNRS, Nantes, France
    index: 2
date: 23 April 2025
bibliography: paper.bib
---

# Summary

Constraint Programming (CP) is a well-established and powerful Artificial 
Intelligence (AI) paradigm for modelling and solving complex combinatorial 
problems [@rossi_2006]. Many CP solvers are currently available, and despite
a generally shared common base, each solver exhibits specific features that make
it more or less suited to certain types of problems and tasks. Performance and 
flexibility are important features of CP solvers, this is why most state-of-the-art
solvers rely on statically typed and compiled programming languages, such as Java
or C++. Because of this, CP has long remained a niche field that is difficult for
non-specialists to access. Recently, the emergence of high-level, solver-independent
modelling languages such as MiniZinc [@nethercote_2007], XCSP³ [@audemard_2020], or
CPMpy [@guns_2019] has made CP more accessible by allowing users to seamlessly
use state-of-the-art solvers from user-friendly interpreted languages such as
Python. To make CP even more accessible to a wider audience, we developed pychoco,
a Python library that provides all-inclusive binding to the Java Choco-solver
library [@prudhomme_2022]. By all-inclusive, we mean that pychoco has no external
dependencies and does not require the installation of Choco-solver or Java on
the user's system. The pychoco Python library supports almost all features of
Choco-solver, is regularly updated, and is automatically built and distributed
through PyPI for Linux, Windows, and MacOSX at each release. As a result, 
pychoco can seamlessly integrate into high-level constraint modelling Python
libraries such as CPMpy [@guns_2019] or PyCSP³ [@lecoutre_2024]. Moreover, 
users who need to use features specific to Choco-solver (e.g. graph variables 
and constraints) can now rely on pychoco without prior knowledge of Java 
programming. We believe that along with initiatives such as CPMpy and PyCSP, the
availability of CP technologies in the Python ecosystem will foster new uses and
the appropriation of CP by a wider scientific and industrial public.

# Statement of need

Constraint programming (CP) offers an expressive and flexible modelling paradigm
which has proven efficient and useful in many industrial and academic applications:
production optimization, aircraft scheduling, nurse scheduling [@wallace_1996],
music [@hooker_2016], cryptography [@gerault_2016], bioinformatics [@barahona_2011],
biodiversity conservation [@deleglise_2024], agroecology [@challand_2025], 
wine blending [@vismara_2016], etc. However, most CP solvers are difficult for 
non-specialists to access because they mostly rely on statically typed and
compiled programming languages such as Java or C++. As most data science and AI 
technologies are available in the Python ecosystem, it seems timely to make 
CP technologies more easily accessible in Python. High-level Python modelling 
libraries such as CPMpy [@guns_2019] and PyCSP³ [@lecoutre_2024] have opened up 
many perspectives in this direction, but most backend solvers still require a 
separate installation. For most Python users, this can be an obstacle. It also 
limits direct solver access and the use of specific features and fine-tuning 
options that may not be available in high-level modelling libraries. Making
Choco-solver more accessible to Python users and facilitating its integration
as a backend solver into high-level modelling libraries were the main motivations
for the creation of pychoco. In addition, the widespread use of Python in 
education was also an argument in favour of pychoco's implementation.

# Design

For several years, the main obstacle to implementing Python bindings for 
Choco-solver was the necessity to set up communication between the Python
interpreter and the Java Virtual Machine (JVM). Indeed, we believe that
the main interest of such bindings was to offer Python users a way to use
Choco-solver without installing the JVM. The [GraalVM](https://www.graalvm.org/)
project has removed this obstacle with the ahead-of-time Native image Java
compilation feature. Inspired by the work of [@michail_2020] to make Python
bindings for the JGraphT Java library, we implemented
[choco-solver-capi](https://github.com/chocoteam/choco-solver-capi),
which contains entry points to the Choco-solver library that GraalVM compiles
as a shared C library. This shared library is embedded into pychoco with
the [SWIG](https://github.com/swig/swig) wrapper. pychoco's API relies on
this SWIG interface and has been designed to mirror the main concepts of
the Choco-solver API while simplifying its usage in a Pythonic way.
We implemented pychoco with software quality standards: unit tests, code review,
and continuous integration. We also rely on the 
[cibuildwheel](https://github.com/pypa/cibuildwheel) Python library to automatically
build and publish Python wheels on PyPI for Windows, MacOSX, and Linux, from 
Python 3.6 to Python 3.13.

# Current usages and perspectives

Since its first release in October 2022, pychoco has been downloaded more than 73k times
from PyPI. It is available as a backend solver in the [CPMpy](https://github.com/CPMpy/cpmpy)
high-level modelling library. We also witness academic uses of pychoco that seem to be
made possible or facilitated by the Python ecosystem. For example, the availability of
pychoco in CPMpy seems to facilitate comparative analyses between different solvers 
accessible from Python [@bleukx_2024]. The richness of Python's ecosystem also 
fosters the integration of CP in workflows involving several AI techniques [@hotz_2024]
and the development of new tools based on CP 
(e.g. [pyagroplan](https://github.com/philippevismara/pyagroplan)). Finally, as Python
is increasingly used in teaching and training, it seems natural to teach CP using Python,
especially for non-computer-scientist audiences 
(e.g. ['AI for ecologists' training course](https://ai-ecol.github.io/)).

# Acknowledgement

We acknowledge the developers of python-JGraphT, whose work inspired the development of
pychoco. We also acknowledge xxxxx, who funded the implementation of the first pychoco
version. Finally, we acknowledge contribution from Ignace Bleukx and Titouan Lorieul.