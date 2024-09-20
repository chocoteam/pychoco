import unittest

from pychoco.model import Model


class TestIntVar(unittest.TestCase):

    def test_instantiate(self):
        m = Model()
        b1 = m.boolvar()
        b2 = m.boolvar(name="boolvar")
        self.assertEqual(b2.name, "boolvar")
        b3 = m.boolvar(0)
        b4 = m.boolvar(1)
        self.assertEqual(b3.get_value(), 0)
        self.assertEqual(b4.get_value(), 1)
        b5 = m.boolvar(False)
        b6 = m.boolvar(True)
        self.assertEqual(b5.get_value(), False)
        self.assertEqual(b6.get_value(), True)
        s = False
        try:
            b7 = m.boolvar(2)
        except AssertionError:
            s = True
        self.assertTrue(s)
        s = False
        try:
            b8 = m.boolvar(4, name="b8")
        except AssertionError:
            s = True
        self.assertTrue(s)

    def test_instantiate_array(self):
        m = Model()
        b1 = m.boolvars(3)
        self.assertEqual(len(b1), 3)
        b2 = m.boolvars(4, name="b")
        self.assertEqual(len(b2), 4)
        for i in range(0, len(b2)):
            self.assertEqual(b2[i].name, "b_{}".format(i))
        b3 = m.boolvars(3, value=False)
        b4 = m.boolvars(3, value=False, name="b4")
        b4 = m.boolvars(3, value=[0, 1, 0])
        b5 = m.boolvars(3, value=[0, 1, 0], name="b5")
        s = False
        try:
            b6 = m.boolvars(3, 4)
        except AssertionError:
            s = True
        self.assertTrue(s)
        s = False
        try:
            b7 = m.boolvars(4, 4, name="b7")
        except AssertionError:
            s = True
        self.assertTrue(s)
        s = False
        try:
            b8 = m.boolvars(3, value=[0, 2, 1], name="b8")
        except AssertionError:
            s = True
        self.assertTrue(s)
        s = False
        try:
            b9 = m.boolvars(3, value=[0, 1, 1, 1])
        except AssertionError:
            s = True
        self.assertTrue(s)

    def test_create_shape(self):
        model = Model()
        vars = model.boolvars((3, 4), name="var")
        self.assertTrue(len(vars) == 3)
        self.assertTrue(len(vars[0]) == 4)
        self.assertTrue(vars[1][2].name == "var_1,2")
        vals = [[False, False, True],
                [True, True, False]]
        others = model.boolvars((2, 3), vals)
        self.assertEqual(others[1][1].get_value(), True)

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
