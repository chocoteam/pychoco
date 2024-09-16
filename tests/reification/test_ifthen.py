import unittest

from pychoco.model import Model


class TestIfThen(unittest.TestCase):

    def testIfThen1(self):
        m = Model()

        x = m.intvar(0,10)
        y = m.intvar(0,100)

        m.if_then(m.arithm(x, "<", 10),
                  m.arithm(y, ">", 42))

        solutions = m.get_solver().find_all_solutions()
        for s in solutions:
            if_cond = s.get_int_val(x) < 10
            then_cond = s.get_int_val(y) > 42
            self.assertTrue(~if_cond or then_cond)


    def testImplies(self):
        m = Model()

        x = m.intvar(0,10)
        b = m.boolvar()

        cons = m.arithm(x, "<", 10)
        cons.implies(b)

        solutions = m.get_solver().find_all_solutions()
        for s in solutions:
            if_cond = s.get_int_val(x) < 10
            then_cond = bool(s.get_int_val(b))
            self.assertTrue(~if_cond or then_cond)


    def testImpliedBy(self):
        m = Model()

        x = m.intvar(0, 10)
        b = m.boolvar()

        cons = m.arithm(x, "<", 10)
        cons.implied_by(b)

        solutions = m.get_solver().find_all_solutions()
        for s in solutions:
            if_cond = bool(s.get_int_val(b))
            then_cond = s.get_int_val(x) < 10
            self.assertTrue(~if_cond or then_cond)