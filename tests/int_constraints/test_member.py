import unittest

from pychoco.model import Model


class TestMember(unittest.TestCase):

    def testMember1(self):
        m = Model()
        x = m.intvar(-1000, 1000)
        m.member(x, [0, 1, 3, 5]).post()
        sols = m.get_solver().find_all_solutions()
        self.assertEqual(len(sols), 4)
        for s in sols:
            self.assertTrue(s.get_int_val(x) in [0, 1, 3, 5])

    def testMember2(self):
        m = Model()
        x = m.intvar(-1000, 1000)
        m.member(x, lb=-10, ub=10).post()
        sols = m.get_solver().find_all_solutions()
        self.assertEqual(len(sols), 21)
        for s in sols:
            self.assertTrue(s.get_int_val(x) in range(-10, 11))
