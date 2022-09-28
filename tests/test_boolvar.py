import unittest

from pychoco.model import Model


class TestIntVar(unittest.TestCase):

    def test_and(self):
        m = Model()
        a = m.boolvar()
        b = m.boolvar()
        c = a & b
        d = a & True
        while m.get_solver().solve():
            self.assertEqual(a.get_value() & True, d.get_value())
            self.assertEqual(a.get_value() & b.get_value(), c.get_value())

    def test_or(self):
        m = Model()
        a = m.boolvar()
        b = m.boolvar()
        c = a | b
        while m.get_solver().solve():
            self.assertEqual(a.get_value() | b.get_value(), c.get_value())

    def test_inver(self):
        m = Model()
        a = m.boolvar()
        b = ~a
        while m.get_solver().solve():
            self.assertEqual(a.get_value(), not b.get_value())

    def test_eq(self):
        m = Model()
        a = m.boolvar()
        b = m.boolvar()
        c = a == b
        val = True
        d = a == val
        while m.get_solver().solve():
            self.assertEqual(a.get_value() == b.get_value(), c.get_value())
            self.assertEqual(a.get_value() is True, d.get_value())

    def test_neq(self):
        m = Model()
        a = m.boolvar()
        b = m.boolvar()
        c = a != b
        val = True
        d = a != val
        while m.get_solver().solve():
            self.assertEqual(a.get_value() != b.get_value(), c.get_value())
            self.assertEqual(a.get_value() is not True, d.get_value())
