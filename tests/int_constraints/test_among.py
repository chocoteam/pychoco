import unittest

from pychoco.model import Model


class TestAmong(unittest.TestCase):

    def testAmong1(self):
        m = Model()
        variables = m.intvars(4, 0, 10)
        values = [1, 2, 3]
        nb_var = m.intvar(2, 3)
        m.among(nb_var, variables, values).post()
        while m.get_solver().solve():
            nb_in = 0
            for v in variables:
                if v.get_value() in values:
                    nb_in += 1
            self.assertTrue(2 <= nb_in <= 3)
            self.assertEqual(nb_in, nb_var.get_value())

    def testAmongFail(self):
        m = Model()
        variables = m.intvars(4, 0, 10)
        values = [11, 12, 13]
        nb_var = m.intvar(2, 3)
        m.among(nb_var, variables, values).post()
        self.assertFalse(m.get_solver().solve())
