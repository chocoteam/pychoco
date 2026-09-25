from pychoco import backend
from pychoco._handle_wrapper import _HandleWrapper


class StateInt(_HandleWrapper):
    """
    A backtrackable integer whose value is automatically restored on backtrack.

    Created via :meth:`~pychoco.model.Model.make_state_int`.  Useful inside
    custom propagators and search strategies to accumulate counters or flags
    that must be consistent with the current search node.

    Example::

        model = Model()
        x = model.intvar(0, 5)
        counter = model.make_state_int(0)

        def propagate(vars_handle, nvars):
            counter.set(counter.get() + 1)
            return 0

        model.custom_constraint([x], propagate).post()
    """

    def __init__(self, handle, model):
        super().__init__(handle)
        self._model = model

    def get(self) -> int:
        """Return the current value."""
        return backend.state_int_get(self._handle)

    def set(self, value: int) -> None:
        """Set the value (backtrackable)."""
        backend.state_int_set(self._handle, value)

    def add(self, delta: int) -> int:
        """Add *delta* to the current value and return the new value (backtrackable)."""
        return backend.state_int_add(self._handle, delta)

    @property
    def value(self) -> int:
        """Current value (readable and writable)."""
        return self.get()

    @value.setter
    def value(self, v: int) -> None:
        self.set(v)

    def __repr__(self) -> str:
        return f"StateInt({self.get()})"


class StateBool(_HandleWrapper):
    """
    A backtrackable boolean whose value is automatically restored on backtrack.

    Created via :meth:`~pychoco.model.Model.make_state_bool`.

    Example::

        model = Model()
        x = model.intvar(0, 5)
        flag = model.make_state_bool(False)

        def propagate(vars_handle, nvars):
            flag.set(True)
            return 0

        model.custom_constraint([x], propagate).post()
    """

    def __init__(self, handle, model):
        super().__init__(handle)
        self._model = model

    def get(self) -> bool:
        """Return the current value."""
        return bool(backend.state_bool_get(self._handle))

    def set(self, value: bool) -> None:
        """Set the value (backtrackable)."""
        backend.state_bool_set(self._handle, int(value))

    @property
    def value(self) -> bool:
        """Current value (readable and writable)."""
        return self.get()

    @value.setter
    def value(self, v: bool) -> None:
        self.set(v)

    def __repr__(self) -> str:
        return f"StateBool({self.get()})"
