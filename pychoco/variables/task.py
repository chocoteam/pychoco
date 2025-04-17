from typing import Union

from pychoco import backend
from pychoco._handle_wrapper import _HandleWrapper
from pychoco.variables.intvar import IntVar


class Task(_HandleWrapper):
    """
    Container representing a task:
    It ensures that: start + duration = end
    """

    def __init__(self, model: "_Model", start: "IntVar", duration: Union[int, "IntVar"],
                 end: Union[None, "IntVar"] = None):
        """
        Task constructor. Based on a starting time `start`, a duration `duration`, and
        optionally an ending time `end`, such that: `start` + `duration` = `end`.

        A call to ensure_bound_consistency() is required before launching the resolution,
        this will not be done automatically.

        Warning: it is recommended to instantiate variables through a Model object.

        :param model: A Choco Model.
        :param start: The starting time (IntVar).
        :param duration: The duration (int or IntVar).
        :param end: The ending time (IntVar, or None).
        """
        self._has_monitor = True
        self._start = start
        self._duration = duration
        if end is None:
            if isinstance(duration, IntVar):
                self._end = model.intvar(start.get_lb() + duration.get_lb(), start.get_ub() + duration.get_ub())
                handle = backend.create_task_iv_iv_iv(start._handle, duration._handle, self._end._handle)
            else:
                handle = backend.create_task_iv_i(start._handle, duration)
                self._has_monitor = False
                self._end = IntVar(backend.task_get_end(handle), model)
                self._duration = IntVar(backend.task_get_duration(handle), model)
        else:
            self._end = end
            if isinstance(duration, IntVar):
                handle = backend.create_task_iv_iv_iv(start._handle, duration._handle, end._handle)
            else:
                handle = backend.create_task_iv_i_iv(start._handle, duration, end._handle)
                self._duration = IntVar(backend.task_get_duration(handle), model)
        self._model = model
        super().__init__(handle)

    @property
    def start(self):
        """
        :return: The integer variable corresponding to the start of this task.
        """
        return self._start

    @property
    def end(self):
        """
        :return: The integer variable corresponding to the end of this task.
        """
        return self._end

    @property
    def duration(self):
        """
        :return: The integer variable corresponding to the duration of this task.
        """
        return self._duration

    def ensure_bound_consistency(self):
        """
        Apply supplementary filtering to ensure bound consistency.
        """
        if self._has_monitor:
            backend.task_ensure_bound_consistency(self._handle)
