
from abc import ABC, abstractmethod

from pychoco.constraints.constraint import Constraint
from pychoco import backend

class ReificationFactory(ABC):
    """
        Reification of constraints
    """

    @property
    @abstractmethod
    def handle(self):
        pass


    def if_then(self, ifcons: Constraint, thencons: Constraint):
        """
        Creates an if-then constraint: ifcons -> thencons
        :param ifcons: a Constraint
        :param thencons: a Constraint
        """
        return backend.if_then(self.handle, ifcons.handle, thencons.handle)