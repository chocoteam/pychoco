import unittest

from pychoco.model import Model
from pychoco.utils import ESat


class TestElement(unittest.TestCase):

    def genericTest(self, model, x, index, values, offset, nb_sols):
        model.element(x, values, index, offset=offset).post()
        solutions = model.get_solver().find_all_solutions()
        self.assertEqual(len(solutions), nb_sols)

    def testAllSame(self):
        m = Model("m")
        values = [1, 1, 1, 1]
        x = m.intvar(0, 1)
        index = m.intvar(20, 22)
        self.genericTest(m, x, index, values, 20, 3)

    def test1(self):
        m = Model("m")
        values = [1, 2, 0, 4, 3]
        index = m.intvar(-3, 10)
        var = m.intvar(-20, 20)
        self.genericTest(m, var, index, values, 0, 5)

    def testNeg(self):
        m = Model("m")
        values = [1, 2, 0, 4, ]
        index = m.intvar(-3, 10)
        var = m.intvar(-20, 20);
        m.element(var, values, index).reify()
        m.get_solver().find_all_solutions()

    def testProp1(self):
        m = Model()
        values = [1, 2, 0, 4, 3]
        index = m.intvar(0)
        var = m.intvar(1)
        c = m.element(var, values, index)
        self.assertEqual(ESat.TRUE, c.is_satisfied())

    def testProp2(self):
        m = Model()
        values = [1, 2, 0, 4, 3]
        index = m.intvar(0)
        var = m.intvar(2)
        c = m.element(var, values, index);
        self.assertEqual(ESat.FALSE, c.is_satisfied())
