from pychoco import backend
from pychoco._internals._handle_wrapper import _HandleWrapper
from pychoco._internals._intvar import _IntVar
from pychoco.variables.task import Task


class _Task(Task, _HandleWrapper):
    """
    Internal class to represent a task.
    """

    def __init__(self, handle, model, has_monitor=True):
        super().__init__(handle)
        self._model = model
        self._has_monitor = has_monitor

    @property
    def start(self):
        var_handle = backend.task_get_start(self.handle)
        return _IntVar(var_handle, self._model)

    @property
    def end(self):
        var_handle = backend.task_get_end(self.handle)
        return _IntVar(var_handle, self._model)

    @property
    def duration(self):
        var_handle = backend.task_get_duration(self.handle)
        return _IntVar(var_handle, self._model)

    def ensure_bound_consistency(self):
        if self._has_monitor:
            backend.task_ensure_bound_consistency(self.handle)
