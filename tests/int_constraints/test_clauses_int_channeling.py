import unittest

from pychoco.model import Model


class TestAllDifferent(unittest.TestCase):

    def testClausesIntChanneling1(self):
        model = Model()
        iv = model.intvar(1, 50)
        eqs = model.boolvars(50)
        lqs = model.boolvars(50)
        model.clauses_int_channeling(iv, eqs, lqs).post()
        s = model.get_solver()
        while model.get_solver().solve():
            pass
        self.assertEqual(s.get_solution_count(), 50)
