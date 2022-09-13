from abc import ABC, abstractmethod


class Task(ABC):
    """
    Container representing a task:
    It ensures that: start + duration = end
    """

    @property
    @abstractmethod
    def start(self):
        """
        :return: The integer variable corresponding to the start of this task.
        """
        pass

    @property
    @abstractmethod
    def end(self):
        """
        :return: The integer variable corresponding to the end of this task.
        """
        pass

    @property
    @abstractmethod
    def duration(self):
        """
        :return: The integer variable corresponding to the duration of this task.
        """
        pass

    @abstractmethod
    def ensure_bound_consistency(self):
        """
        Apply supplementary filtering to ensure bound consistency.
        """
        pass
