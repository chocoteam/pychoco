import unittest

from pychoco.model import Model


class TestDiv(unittest.TestCase):

    def testDiv1(self):
        m = Model()
        a = m.intvar(0, 10)
        b = m.intvar(-10, 40)
        c = m.intvar(-1, 12)
        m.div(a, b, c).post()
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            self.assertEqual(int(s.get_int_val(a) / s.get_int_val(b)), s.get_int_val(c))
