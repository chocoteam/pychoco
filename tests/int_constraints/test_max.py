import unittest

from pychoco.model import Model


class TestMax(unittest.TestCase):

    def testMax1(self):
        m = Model()
        a = m.intvar(0, 5)
        b = m.intvars(5, 0, 5)
        m.max(a, b).post()
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            vals = [s.get_int_val(i) for i in b]
            self.assertEqual(max(vals), s.get_int_val(a))
