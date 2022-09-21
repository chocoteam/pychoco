import unittest

from pychoco.model import Model


class TestTimes(unittest.TestCase):

    def testTimes1(self):
        m = Model()
        x = m.intvar(-10, 10)
        y = m.intvar(4, 8)
        z = m.intvar(-3, 12)
        m.times(x, y, z).post()
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            self.assertEqual(s.get_int_val(x) * s.get_int_val(y), s.get_int_val(z))

    def testTimes2(self):
        m = Model()
        x = m.intvar(-10, 10)
        y = m.intvar(4, 8)
        m.times(x, y, -6).post()
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            self.assertEqual(s.get_int_val(x) * s.get_int_val(y), -6)

    def testTimes3(self):
        m = Model()
        x = m.intvar(-10, 10)
        z = m.intvar(-3, 12)
        m.times(x, 3, z).post()
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            self.assertEqual(s.get_int_val(x) * 3, s.get_int_val(z))
