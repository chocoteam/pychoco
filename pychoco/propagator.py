"""
Class-based API for defining custom propagators.

Subclass :class:`Propagator` and override :meth:`propagate` (and optionally
:meth:`is_entailed`) to create a reusable, stateful propagator.

Example::

    from pychoco import Model, Propagator

    class BoundSync(Propagator):
        def __init__(self, x, y):
            super().__init__([x, y])
            self.call_count = 0

        def propagate(self):
            self.call_count += 1
            self.vars[0].update_ub(self.vars[1].get_ub())

    model = Model()
    x = model.intvar(0, 10)
    y = model.intvar(0, 5)
    BoundSync(x, y).post()
"""

import ctypes
from abc import ABC, abstractmethod

from pychoco import backend
from pychoco._utils import make_intvar_array
from pychoco.exceptions import Contradiction

# Re-use the same ctypes function types as IntConstraintFactory.
_PROPAGATE_FN = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_int)
_IS_ENTAILED_FN = ctypes.CFUNCTYPE(ctypes.c_int)


class Propagator(ABC):
    """
    Abstract base class for custom propagators.

    Subclass this class, list the variables in ``__init__`` via
    ``super().__init__(intvars)``, then override :meth:`propagate` and
    optionally :meth:`is_entailed`.

    Call :meth:`post` once to register the propagator with the model.

    :param intvars: list of :class:`~pychoco.variables.intvar.IntVar` this
        propagator operates on.  Accessible as ``self.vars`` inside the
        overridden methods.
    :param priority: scheduling priority (1=UNARY … 7=VERY_SLOW,
        default 4=LINEAR).
    """

    def __init__(self, intvars, priority: int = 4):
        if not intvars:
            raise ValueError("Propagator requires at least one variable.")
        self.vars = list(intvars)
        self.priority = priority
        self._model = intvars[0].model
        # Strong references to ctypes callbacks to prevent GC
        self._c_fn = None
        self._c_entailed_fn = None

    @abstractmethod
    def propagate(self):
        """
        Filtering logic.  Called by the solver whenever domains change.

        Use the filtering methods on ``self.vars`` elements
        (``update_lb``, ``update_ub``, ``instantiate_to``,
        ``remove_value``).  Raise
        :class:`~pychoco.exceptions.Contradiction` to signal a dead-end.
        """

    def is_entailed(self) -> int:
        """
        Entailment check.  Override to provide a smarter check.

        Must return:

        * a **positive** integer — ``ESat.TRUE``: all completions of the
          current domains satisfy the constraint; the solver may deactivate
          the propagator for this branch.
        * ``0`` — ``ESat.UNDEFINED``: cannot determine yet.
        * a **negative** integer — ``ESat.FALSE``: no completion can satisfy
          the constraint (``propagate`` must have already raised
          :class:`~pychoco.exceptions.Contradiction` for the same state).

        The default implementation always returns ``1`` (TRUE), which lets
        Choco deactivate the propagator once all variables are fixed.
        """
        return 1

    def post(self):
        """
        Register this propagator with its model.

        May only be called once per instance.
        """
        if self._c_fn is not None:
            raise RuntimeError("Propagator already posted.")

        # Build ctypes adapters that delegate to self.propagate / self.is_entailed
        # and capture self via closure.
        def _propagate_adapter(_vars_handle_int, _nvars):
            try:
                self.propagate()
                return 0
            except Contradiction:
                return -1

        def _entailed_adapter():
            return self.is_entailed()

        self._c_fn = _PROPAGATE_FN(_propagate_adapter)
        self._c_entailed_fn = _IS_ENTAILED_FN(_entailed_adapter)

        vars_array = make_intvar_array(self.vars)
        handle = backend.create_custom_constraint(
            vars_array,
            ctypes.cast(self._c_fn, ctypes.c_void_p).value,
            ctypes.cast(self._c_entailed_fn, ctypes.c_void_p).value,
            self.priority,
        )

        from pychoco.constraints.constraint import Constraint
        constraint = Constraint(handle, self._model)

        # Keep a strong reference on the model so ctypes callbacks are
        # not GC'd before the model is destroyed.
        if not hasattr(self._model, "_custom_constraints"):
            self._model._custom_constraints = []
        self._model._custom_constraints.append(self)

        backend.post(constraint._handle)
