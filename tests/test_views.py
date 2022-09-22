import unittest

from pychoco.model import Model
from pychoco.variables.boolvar import BoolVar


class TestViews(unittest.TestCase):

    def test_bool_not_view(self):
        m = Model()
        b = m.boolvar()
        not_b = m.bool_not_view(b)
        self.assertTrue(not_b.is_view())
        while m.get_solver().solve():
            self.assertFalse(b.get_value() and not_b.get_value())
            self.assertTrue(b.get_value() or not_b.get_value())

    def test_set_bool_view(self):
        m = Model()
        setvar = m.setvar([], range(0, 10))
        b = m.set_bool_view(setvar, 5)
        self.assertTrue(b.is_view())
        while m.get_solver().solve():
            self.assertEqual(b.get_value(), 5 in setvar.get_value())

    def test_set_bools_view(self):
        m = Model()
        setvar = m.setvar([], range(0, 10))
        bools = m.set_bools_view(setvar, 10)
        [self.assertTrue(b.is_view()) for b in bools]
        while m.get_solver().solve():
            for i in range(0, 10):
                self.assertEqual(i in setvar.get_value(), bools[i].get_value())

    def test_int_offset_view(self):
        m = Model()
        intvar = m.intvar(0, 10)
        int_offset = m.int_offset_view(intvar, 2)
        self.assertTrue(int_offset.is_view())
        while m.get_solver().solve():
            self.assertEqual(intvar.get_value(), int_offset.get_value() - 2)

    def test_minus_view(self):
        m = Model()
        intvar = m.intvar(0, 10)
        int_minus = m.int_minus_view(intvar)
        self.assertTrue(int_minus.is_view())
        while m.get_solver().solve():
            self.assertEqual(intvar.get_value(), -int_minus.get_value())

    def test_int_scale_view(self):
        m = Model()
        intvar = m.intvar(0, 10)
        int_scale = m.int_scale_view(intvar, 2)
        self.assertTrue(int_scale.is_view())
        while m.get_solver().solve():
            self.assertEqual(intvar.get_value() * 2, int_scale.get_value())

    def test_int_abs_view(self):
        m = Model()
        intvar = m.intvar(-10, 10)
        int_abs = m.int_abs_view(intvar)
        while m.get_solver().solve():
            self.assertEqual(abs(intvar.get_value()), int_abs.get_value())

    def test_int_affine_view(self):
        m = Model()
        intvar = m.intvar(0, 10)
        affine_view = m.int_affine_view(2, intvar, 1)
        self.assertTrue(affine_view.is_view())
        while m.get_solver().solve():
            self.assertEqual(2 * intvar.get_value() + 1, affine_view.get_value())

    def test_int_eq_view(self):
        m = Model()
        intvar = m.intvar(0, 10)
        b = m.int_eq_view(intvar, 2)
        self.assertTrue(b.is_view())
        self.assertTrue(isinstance(b, BoolVar))
        while m.get_solver().solve():
            self.assertEqual(intvar.get_value() == 2, b.get_value())

    def test_int_ne_view(self):
        m = Model()
        intvar = m.intvar(0, 10)
        b = m.int_ne_view(intvar, 2)
        self.assertTrue(b.is_view())
        self.assertTrue(isinstance(b, BoolVar))
        while m.get_solver().solve():
            self.assertEqual(intvar.get_value() != 2, b.get_value())

    def test_int_le_view(self):
        m = Model()
        intvar = m.intvar(0, 10)
        b = m.int_le_view(intvar, 2)
        self.assertTrue(b.is_view())
        self.assertTrue(isinstance(b, BoolVar))
        while m.get_solver().solve():
            self.assertEqual(intvar.get_value() <= 2, b.get_value())

    def test_int_ge_view(self):
        m = Model()
        intvar = m.intvar(0, 10)
        b = m.int_ge_view(intvar, 2)
        self.assertTrue(b.is_view())
        self.assertTrue(isinstance(b, BoolVar))
        while m.get_solver().solve():
            self.assertEqual(intvar.get_value() >= 2, b.get_value())

    def test_bools_set_view(self):
        m = Model()
        boolvars = m.boolvars(10)
        set_view = m.bools_set_view(boolvars, offset=2)
        self.assertTrue(set_view.is_view())
        while m.get_solver().solve():
            for i in range(0, 10):
                if boolvars[i].get_value():
                    self.assertTrue(i + 2 in set_view.get_value())
                else:
                    self.assertFalse(i + 2 in set_view.get_value())

    def test_ints_set_view(self):
        m = Model()
        intvars = m.intvars(5, 0, 5)
        v = range(0, 5)
        set_view = m.ints_set_view(intvars, v)
        self.assertTrue(set_view.is_view())
        while m.get_solver().solve():
            for i in range(0, 5):
                self.assertEqual(intvars[i].get_value() == v[i], i in set_view.get_value())

    def test_set_union_view(self):
        m = Model()
        a = m.setvar(set([]), set(range(0, 5)))
        b = m.setvar(set([]), set(range(5, 10)))
        c = m.setvar(set([]), set(range(10, 15)))
        union = m.set_union_view([a, b, c])
        self.assertTrue(union.is_view())
        while m.get_solver().solve():
            self.assertSetEqual(
                a.get_value().union(b.get_value().union(c.get_value())),
                union.get_value()
            )

    def test_set_intersection_view(self):
        m = Model()
        a = m.setvar(set([]), set(range(0, 5)))
        b = m.setvar(set([]), set(range(5, 10)))
        c = m.setvar(set([]), set(range(10, 15)))
        intersection = m.set_intersection_view([a, b, c])
        self.assertTrue(intersection.is_view())
        while m.get_solver().solve():
            self.assertSetEqual(
                a.get_value().intersection(b.get_value().intersection(c.get_value())),
                intersection.get_value()
            )

    def test_set_difference_view(self):
        m = Model()
        a = m.setvar([], range(0, 5))
        b = m.setvar([], range(0, 7))
        diff = m.set_difference_view(a, b)
        self.assertTrue(diff.is_view())
        while m.get_solver().solve():
            self.assertSetEqual(
                a.get_value().difference(b.get_value()),
                diff.get_value()
            )
