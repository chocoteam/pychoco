from typing import List

from pychoco import backend
from pychoco._handle_wrapper import _HandleWrapper
from pychoco._utils import make_intvar_array, make_int_2d_array


class MultivaluedDecisionDiagram(_HandleWrapper):
    """
    Multi-valued Decision Diagram (MDD)
    """

    def __init__(
        self,
        intvars: List["IntVar"],
        tuples: List[List[int]],
        compact: str = "NEVER",
        sort_tuple=False,
        uvalue: int = None,
    ):
        """
        Create a MDD

        :param intvars: A list of IntVars.
        :param tuples: A List[List[int]] either tuples (allowed).
        :param compact: Either "NEVER", "ONCE", or "EACH".
        :param sort_tuple: A bool.
        :param uvalue: An int or None. If not None, the MDD will be created without a special value for unassigned variables.
        :return: A MDD.
        """
        assert len(tuples) > 0
        for r in tuples:
            assert len(r) == len(intvars)
        handle = backend.create_mdd_tuples(
            make_intvar_array(intvars), make_int_2d_array(tuples), compact, sort_tuple
        )

        if uvalue is not None:
            assert isinstance(uvalue, int)
            handle = backend.create_mdd_tuples_u(
                make_intvar_array(intvars),
                make_int_2d_array(tuples),
                compact,
                sort_tuple,
                uvalue
            )
        else:
            handle = backend.create_mdd_tuples(
                make_intvar_array(intvars),
                make_int_2d_array(tuples),
                compact,
                sort_tuple
            )
        super().__init__(handle)
