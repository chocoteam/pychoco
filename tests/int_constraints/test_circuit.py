import unittest

from pychoco.model import Model


class TestCircuit(unittest.TestCase):

    def testCircuit1(self):
        m = Model()
        intvars = m.intvars(7, 0, 6)
        m.circuit(intvars).post()
        all_diff = m.all_different(intvars)
        while m.get_solver().solve():
            self.assertTrue(all_diff.is_satisfied())
            i = intvars[0].get_value()
            n = 1
            while i != 0 and n < len(intvars):
                i = intvars[i].get_value()
                n += 1
            self.assertTrue(i == 0 and n == len(intvars))

    def testCircuitFail(self):
        m = Model()
        intvars = m.intvars(7, 0, 6)
        m.circuit(intvars).post()
        m.at_most_n_values(intvars, m.intvar(3)).post()
        self.assertFalse(m.get_solver().solve())
