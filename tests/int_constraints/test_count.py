import unittest

from pychoco.model import Model


class TestCount(unittest.TestCase):

    def testCount1(self):
        m = Model()
        intvars = m.intvars(5, 0, 5)
        count = m.intvar(0, 3)
        m.count(1, intvars, count).post()
        while m.get_solver().solve():
            s = sum([1 for v in intvars if v.get_value() == 1])
            self.assertEqual(s, count.get_value())
            self.assertTrue(0 <= s <= 3)

    def testCount2(self):
        m = Model()
        intvars = m.intvars(5, 0, 5)
        count = m.intvar(0, 3)
        value = m.intvar(0, 5)
        m.count(value, intvars, count).post()
        while m.get_solver().solve():
            s = sum([1 for v in intvars if v.get_value() == value.get_value()])
            self.assertEqual(s, count.get_value())
            self.assertTrue(0 <= s <= 3)

    def testCountFail(self):
        m = Model()
        intvars = [m.intvar(0, 5), m.intvar(1), m.intvar(1), m.intvar(1, 3)]
        count = m.intvar(2, 3)
        m.count(4, intvars, count).post()
        self.assertFalse(m.get_solver().solve())
