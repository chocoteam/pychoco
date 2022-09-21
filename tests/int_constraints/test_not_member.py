import unittest

from pychoco.model import Model


class TestNotMember(unittest.TestCase):

    def testMember1(self):
        m = Model()
        x = m.intvar(-1000, 1000)
        m.not_member(x, [0, 1, 3, 5]).post()
        sols = m.get_solver().find_all_solutions()
        self.assertEqual(len(sols), 2001 - 4)
        for s in sols:
            self.assertFalse(s.get_int_val(x) in [0, 1, 3, 5])

    def testMember2(self):
        m = Model()
        x = m.intvar(-1000, 1000)
        m.not_member(x, lb=-10, ub=10).post()
        sols = m.get_solver().find_all_solutions()
        self.assertEqual(len(sols), 2001 - 21)
        for s in sols:
            self.assertFalse(s.get_int_val(x) in range(-10, 11))
