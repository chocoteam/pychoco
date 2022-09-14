from pychoco import backend


class _HandleWrapper:
    """
    A C Object handle wrapper (through SWIG). Keeps a handle to a backend object and
    cleans up on deletion. Inspired from https://github.com/d-michail/python-jgrapht/.
    """

    def __init__(self, handle):
        self._handle = handle

    @property
    def handle(self):
        return self._handle

    def __del__(self):
        if backend.chocosolver_is_initialized():
            if self._handle is not None:
                backend.chocosolver_handles_destroy(self._handle)

    def __repr__(self):
        return "_HandleWrapper(%r)" % self._handle
