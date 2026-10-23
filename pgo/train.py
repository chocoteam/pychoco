"""Runs pytest with an instrumented choco-solver-capi library, then makes it dump its PGO
profile (see pgo/train.sh). Arguments are passed to pytest."""
import sys

import pytest

from pychoco import backend

code = pytest.main(["-q", "-p", "no:cacheprovider", *sys.argv[1:]])
# The native exit below bypasses Python's own shutdown, which would flush these
sys.stdout.flush()
sys.stderr.flush()
if code != 0:
    sys.exit(code)  # no profile: train.sh stops
# Never returns: runs the shutdown hooks, which write the profile, and exits
backend.chocosolver_exit_for_profiling()
