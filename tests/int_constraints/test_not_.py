import unittest

from pychoco.model import Model


class TestNot(unittest.TestCase):

    def testNot1(self):
        m = Model()
        a = m.intvar(0, 10)
        b = m.intvar(0, 10)
        c = m.arithm(a, ">", b)
        m.not_(c).post()
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            self.assertTrue(s.get_int_val(a) <= s.get_int_val(b))
