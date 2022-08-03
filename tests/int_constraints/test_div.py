import unittest

from pychoco import create_model


class TestDiv(unittest.TestCase):

    def testDiv1(self):
        m = create_model()
        a = m.intvar(0, 10)
        b = m.intvar(-10, 40)
        c = m.intvar(-1, 12)
        m.div(a, b, c).post()
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            self.assertEqual(int(s.get_int_val(a) / s.get_int_val(b)), s.get_int_val(c))
