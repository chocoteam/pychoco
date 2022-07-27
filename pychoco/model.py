from abc import ABC, abstractmethod


class Model(ABC):
    """
    The Model is the header component of Constraint Programming. It embeds the list of
    Variable (and their Domain), the Constraint's network, and a propagation engine to
    pilot the propagation.
    """

    @abstractmethod
    def get_name(self):
        """
        :return: The name of the model.
        """
        pass

    @abstractmethod
    def get_solver(self):
        """
        :return: The solver associated with this model.
        """
        pass

    def __repr__(self):
        return "Choco Model ('" + self.get_name() + "')"
