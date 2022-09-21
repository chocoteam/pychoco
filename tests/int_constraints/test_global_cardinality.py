import unittest

from pychoco.model import Model


class TestGlobalCardinality(unittest.TestCase):

    def testGlobalCardinality1(self):
        m = Model()
        intvars = m.intvars(5, 0, 5)
        values = [1, 2]
        occurrences = m.intvars(2, 2)
        gcc = m.global_cardinality(intvars, values, occurrences, False)
        gcc.post()
        while m.get_solver().solve():
            self.assertTrue(gcc.is_satisfied())
        self.assertTrue(m.get_solver().get_solution_count() > 0)

    def testGlobalCardinalityFail(self):
        m = Model()
        intvars = m.intvars(5, 3, 5)
        values = [1, 2]
        occurrences = m.intvars(2, 2)
        gcc = m.global_cardinality(intvars, values, occurrences, False)
        gcc.post()
        self.assertFalse(m.get_solver().solve())
