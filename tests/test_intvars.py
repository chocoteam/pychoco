import unittest

from pychoco.model import Model


class TestIntVar(unittest.TestCase):

    def test_create_intvar(self):
        model = Model("MyModel")
        a = model.intvar(0, 10, "a")
        b = model.intvar(1, 2)
        self.assertEqual(a.name, "a")
        self.assertEqual(a.get_lb(), 0)
        self.assertEqual(a.get_ub(), 10)
        self.assertEqual(b.get_lb(), 1)
        self.assertEqual(b.get_ub(), 2)

    def test_add(self):
        m = Model()
        a = m.intvar(-10, 10)
        b = m.intvar(-10, 10)
        c = a + b
        d = a + 2
        while m.get_solver().solve():
            self.assertEqual(a.get_value() + b.get_value(), c.get_value())
            self.assertEqual(a.get_value() + 2, d.get_value())

    def test_sub(self):
        m = Model()
        a = m.intvar(-10, 10)
        b = m.intvar(-10, 10)
        c = a - b
        d = a - 2
        while m.get_solver().solve():
            self.assertEqual(a.get_value() - b.get_value(), c.get_value())
            self.assertEqual(a.get_value() - 2, d.get_value())

    def test_neg(self):
        m = Model()
        a = m.intvar(-10, 10)
        b = -a
        while m.get_solver().solve():
            self.assertEqual(a.get_value(), -b.get_value())

    def test_mul(self):
        m = Model()
        a = m.intvar(-10, 10)
        b = m.intvar(-10, 10)
        c = a * b
        d = a * 2
        while m.get_solver().solve():
            self.assertEqual(a.get_value() * b.get_value(), c.get_value())
            self.assertEqual(a.get_value() * 2, d.get_value())

    def test_div(self):
        m = Model()
        a = m.intvar(-10, 10)
        b = m.intvar(-10, 10)
        c = a / b
        d = a / 2
        while m.get_solver().solve():
            self.assertEqual(int(a.get_value() / b.get_value()), c.get_value())
            self.assertEqual(int(a.get_value() / 2), d.get_value())

    def test_mod(self):
        m = Model()
        a = m.intvar(-10, 10)
        b = m.intvar(-10, 10)
        c = a % b
        d = a % 2
        while m.get_solver().solve():
            self.assertEqual(a.get_value() % b.get_value(), c.get_value())
            self.assertEqual(a.get_value() % 2, d.get_value())

    def test_pow(self):
        m = Model()
        a = m.intvar(-10, 10)
        c = a ** 2
        while m.get_solver().solve():
            self.assertEqual(a.get_value() ** 2, c.get_value())

    def test_eq(self):
        m = Model()
        a = m.intvar(-10, 10)
        b = m.intvar(-10, 10)
        c = a == 2
        d = a == b
        while m.get_solver().solve():
            self.assertEqual(a.get_value() == 2, c.get_value())
            self.assertEqual(a.get_value() == b.get_value(), d.get_value())

    def test_neq(self):
        m = Model()
        a = m.intvar(-10, 10)
        b = m.intvar(-10, 10)
        c = a != 2
        d = a != b
        while m.get_solver().solve():
            self.assertEqual(a.get_value() != 2, c.get_value())
            self.assertEqual(a.get_value() != b.get_value(), d.get_value())

    def test_le(self):
        m = Model()
        a = m.intvar(-10, 10)
        b = m.intvar(-10, 10)
        c = a <= 2
        d = a <= b
        while m.get_solver().solve():
            self.assertEqual(a.get_value() <= 2, c.get_value())
            self.assertEqual(a.get_value() <= b.get_value(), d.get_value())

    def test_ge(self):
        m = Model()
        a = m.intvar(-10, 10)
        b = m.intvar(-10, 10)
        c = a >= 2
        d = a >= b
        while m.get_solver().solve():
            self.assertEqual(a.get_value() >= 2, c.get_value())
            self.assertEqual(a.get_value() >= b.get_value(), d.get_value())

    def test_lt(self):
        m = Model()
        a = m.intvar(-10, 10)
        b = m.intvar(-10, 10)
        c = a < 2
        d = a < b
        while m.get_solver().solve():
            self.assertEqual(a.get_value() < 2, c.get_value())
            self.assertEqual(a.get_value() < b.get_value(), d.get_value())

    def test_gt(self):
        m = Model()
        a = m.intvar(-10, 10)
        b = m.intvar(-10, 10)
        c = a > 2
        d = a > b
        while m.get_solver().solve():
            self.assertEqual(a.get_value() > 2, c.get_value())
            self.assertEqual(a.get_value() > b.get_value(), d.get_value())
