import unittest

from pychoco.model import Model


class TestDistance(unittest.TestCase):

    def testDistance1(self):
        m = Model()
        a = m.intvar(0, 10)
        b = m.intvar(0, 20)
        m.distance(a, b, ">", 10).post()
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            self.assertTrue(abs(s.get_int_val(a) - s.get_int_val(b)) >= 10)

    def testDistance2(self):
        m = Model()
        a = m.intvar(0, 10)
        b = m.intvar(0, 20)
        c = m.intvar(0, 20)
        m.distance(a, b, "=", c).post()
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            self.assertEqual(abs(s.get_int_val(a) - s.get_int_val(b)), s.get_int_val(c))

    def testDistance3(self):
        m = Model()
        a = m.intvar(0, 10)
        b = m.intvar(0, 20)
        c = m.intvar(0, 20)
        m.distance(a, b, ">", c).post()
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            self.assertTrue(abs(s.get_int_val(a) - s.get_int_val(b)) > s.get_int_val(c))

    def testDistanceError(self):
        m = Model()
        a = m.intvar(0, 10)
        b = m.intvar(0, 20)
        c = m.intvar(0, 20)
        self.assertRaises(AssertionError, m.distance, *[a, b, "!=", c])
        self.assertRaises(AssertionError, m.distance, *[a, b, ">=", 10])
        self.assertRaises(AssertionError, m.distance, *[a, b, "pp", c])
        self.assertRaises(AssertionError, m.distance, *[a, b, "pp", 2])
