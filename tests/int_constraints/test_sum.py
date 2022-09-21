import unittest

from pychoco.model import Model


class TestSum(unittest.TestCase):

    def testSum1(self):
        model = Model()
        intvars = model.intvars(5, 0, 5)
        sumvar = model.intvar(15, 20)
        model.sum(intvars, "=", sumvar).post()
        nb_sol = self._check_solutions("=", intvars, sumvar)
        # compare to scalar
        coeffs = [1, 1, 1, 1, 1]
        model = Model()
        intvars = model.intvars(5, 0, 5)
        sumvar = model.intvar(15, 20)
        model.scalar(intvars, coeffs, "=", sumvar).post()
        nb_sol2 = 0;
        while model.get_solver().solve():
            nb_sol2 += 1
        self.assertEqual(nb_sol, nb_sol2)

    def testSumFail(self):
        model = Model()
        intvars = model.intvars(5, 0, 5)
        sumvar = model.intvar(26, 30)
        model.sum(intvars, "=", sumvar).post()
        self.assertFalse(model.get_solver().solve())

    def _check_solutions(self, operator, intvars, sumvar):
        model = sumvar.model
        nb_sol = 0
        while model.get_solver().solve():
            nb_sol += 1
            computed = sum([v.get_value() for v in intvars])
            if operator == "=":
                self.assertEqual(computed, sumvar.get_value())
            elif operator == ">=":
                self.assertTrue(computed >= sumvar.get_value())
            elif operator == "<=":
                self.assertTrue(computed <= sumvar.getValue())
        self.assertTrue(nb_sol > 0)
        return nb_sol
