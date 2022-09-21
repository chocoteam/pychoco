import unittest

from pychoco.model import Model


class TestScalar(unittest.TestCase):

    def testScalar1(self):
        model = Model()
        coeffs = [1, 5, 7, 8]
        intvars = model.intvars(4, 1, 5);
        model.scalar(intvars, coeffs, "=", 35).post()
        self._check_solutions(coeffs, intvars, model.intvar(35), "=")

    def testScalar2(self):
        model = Model()
        coeffs = [5, 6, 7, 9]
        vars = model.intvars(4, -5, 5)
        model.scalar(vars, coeffs, "<=", 0).post()
        self._check_solutions(coeffs, vars, model.intvar(0), "<=")

    def testScalar3(self):
        model = Model()
        coeffs = [1]
        intvars = [model.intvar(1, 100)]
        sumvar = model.intvar(1, 100)
        model.scalar(intvars, coeffs, "=", sumvar).post()
        self.assertEqual(self._check_solutions(coeffs, intvars, sumvar, "="), 100)

    def testScalarFail(self):
        model = Model()
        coeffs = [0]
        intvars = [model.intvar(1, 10)]
        model.scalar(intvars, coeffs, ">=", 1).post()
        self.assertFalse(model.get_solver().solve())

    def _check_solutions(self, coeffs, intvars, sumvar, operator):
        model = intvars[0].model
        nb_sol = 0
        while model.get_solver().solve():
            nb_sol += 1
            computed = 0
            for i in range(0, len(intvars)):
                computed += coeffs[i] * intvars[i].get_value()
            if operator == "=":
                self.assertEqual(sumvar.get_value(), computed)
            elif operator == "<=":
                self.assertTrue(computed <= sumvar.get_value())
        self.assertTrue(nb_sol > 0)
        return nb_sol
