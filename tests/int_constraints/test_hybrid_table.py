import unittest

from pychoco.constraints.extension.hybrid.supportable import *
from pychoco.model import Model


class TestHybridTable(unittest.TestCase):

    def testHTable1(self):
        m = Model()
        intvars = m.intvars(3, 0, 5)
        htuples = [
            [eq(1), gt(2), le(col(0))],
            [eq(2), le(2), ne(col(1))],
            [eq(3), eq(0), any_val()],
            [eq(4), ne(0), eq(col(1))]
        ]
        htable_constraint = m.hybrid_table(intvars, htuples)
        htable_constraint.post()
        sols = m.get_solver().find_all_solutions()
        self.assertTrue(len(sols) > 4)
        for s in sols:
            if s.get_int_val(intvars[0]) == 1:
                self.assertTrue(s.get_int_val(intvars[1]) > 2)
                self.assertTrue(s.get_int_val(intvars[2]) <= s.get_int_val(intvars[0]))
            elif s.get_int_val(intvars[0]) == 2:
                self.assertTrue(s.get_int_val(intvars[1]) <= 2)
                self.assertTrue(s.get_int_val(intvars[2]) != s.get_int_val(intvars[1]))
            elif s.get_int_val(intvars[0]) == 3:
                self.assertTrue(s.get_int_val(intvars[1]) == 0)
            elif s.get_int_val(intvars[0]) == 4:
                self.assertTrue(s.get_int_val(intvars[1]) != 0)
                self.assertTrue(s.get_int_val(intvars[2]) == s.get_int_val(intvars[1]))
