import unittest

from pychoco import create_model


class TestElement(unittest.TestCase):

    def genericTest(self, model, x, index, values, offset, nb_sols):
        model.element(x, values, index, offset=offset).post()
        solutions = model.get_solver().find_all_solutions()
        self.assertEqual(len(solutions), nb_sols)

    def testAllSame(self):
        m = create_model("m")
        values = [1, 1, 1, 1]
        x = m.intvar(0, 1)
        index = m.intvar(20, 22)
        self.genericTest(m, x, index, values, 20, 3)

    def test1(self):
        m = create_model("m")
        values = [1, 2, 0, 4, 3]
        index = m.intvar(-3, 10)
        var = m.intvar(-20, 20)
        self.genericTest(m, var, index, values, 0, 5)
