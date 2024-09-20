import unittest

from pychoco.model import Model


class TestIntVar(unittest.TestCase):

    def test_array_with_name(self):
        m = Model()
        vs = m.intvars(5, -1, 1, name="vs")
        for i in range(0, len(vs)):
            self.assertEqual(vs[i].name, "vs_{}".format(i))

    def test_create_intvar(self):
        model = Model("MyModel")
        a = model.intvar(0, 10, "a")
        b = model.intvar(1, 2)
        self.assertEqual(a.name, "a")
        self.assertEqual(a.get_lb(), 0)
        self.assertEqual(a.get_ub(), 10)
        self.assertEqual(b.get_lb(), 1)
        self.assertEqual(b.get_ub(), 2)

    def test_create_shape(self):
        model = Model()
        vars = model.intvars((3, 4), 0, 10, name="var")
        self.assertTrue(len(vars) == 3)
        self.assertTrue(len(vars[0]) == 4)
        self.assertTrue(vars[1][2].name == "var_1,2")
        vals = [[0, 1, 2],
                [3, 4, 5]]
        others = model.intvars((2, 3), vals)
        self.assertEqual(others[1][1].get_ub(), 4)

    def test_created_enumerated(self):
        m = Model()
        a = m.intvar([0, 1, 4, 5], name="enum_a")
        vals = a.get_domain_values()
        self.assertEqual(vals, [0, 1, 4, 5])
        bb = m.intvars(10, 0, 4)
        self.assertTrue(a.has_enumerated_domain())
        for b in bb:
            self.assertTrue(b.has_enumerated_domain())
        c = m.intvar(0, 10, bounded_domain=True)
        d = m.intvar(0, 10, bounded_domain=False)
        e = m.intvar(0, 10, name="e", bounded_domain=True)
        ff = m.intvars(3, 0, 10, bounded_domain=False)
        self.assertFalse(c.has_enumerated_domain())
        self.assertTrue(d.has_enumerated_domain())
        self.assertFalse(e.has_enumerated_domain())
        for f in ff:
            self.assertTrue(f.has_enumerated_domain())

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
