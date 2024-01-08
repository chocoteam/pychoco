import unittest

from pychoco.model import Model


class TestReify(unittest.TestCase):

    def testReify1(self):
        m = Model()
        a = m.intvar(0, 10)
        b = m.intvar(0, 10)

        cons = m.arithm(a, "+", b, '=', 10)
        bv = cons.reify()

        solutions = m.get_solver().find_all_solutions()
        for s in solutions:
            self.assertEqual(s.get_int_val(a) + s.get_int_val(b) == 10, s.get_int_val(bv))

    def testReifyWith1(self):
        m = Model()
        a = m.intvar(0, 10)
        b = m.intvar(0, 10)
        bv = m.boolvar()

        cons = m.arithm(a, "+", b, '=', 10)
        cons.reify_with(bv)

        solutions = m.get_solver().find_all_solutions()
        for s in solutions:
            self.assertEqual(s.get_int_val(a) + s.get_int_val(b) == 10, s.get_int_val(bv))

