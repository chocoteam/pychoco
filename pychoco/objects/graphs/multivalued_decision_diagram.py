from typing import List

from pychoco import backend
from pychoco._handle_wrapper import _HandleWrapper
from pychoco._utils import make_intvar_array, make_int_2d_array


class MultivaluedDecisionDiagram(_HandleWrapper):
    """
    Multi-valued Decision Diagram (MDD)
    """

    def __init__(self, intvars: List["IntVar"], tuples: List[List[int]], compact: str = "NEVER", sort_tuple=False):
        """
        Create a MDD

        :param intvars: A list of IntVars.
        :param tuples: A List[List[int]] either tuples (allowed).
        :param compact: Either "NEVER", "ONCE", or "EACH".
        :param sort_tuple: A bool.
        :return: A MDD.
        """
        assert len(tuples) > 0
        for r in tuples:
            assert len(r) == len(intvars)
        handle = backend.create_mdd_tuples(
            make_intvar_array(intvars),
            make_int_2d_array(tuples),
            compact,
            sort_tuple
        )
        super().__init__(handle)
