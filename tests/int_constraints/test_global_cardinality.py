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

    def testGlobalCardinalityAC(self):
        m = Model()
        x, y, z = m.intvar([0, 1, 2], name="x"), m.intvar([0, 2], name="y"), m.intvar([0, 2], name="z")
        occurrences = m.intvars(3, 0, 1)
        m.global_cardinality([x, y, z], [0, 1, 2], occurrences, False, "AC").post()
        m.get_solver()._propagate()
        self.assertEqual(x.get_domain_values(), [1])

    def testGlobalCardinalityBC1(self):
        m = Model()
        x, y, z = m.intvar([0, 1, 2], name="x"), m.intvar([0, 2], name="y"), m.intvar([0, 2], name="z")
        occurrences = m.intvars(3, 0, 1)
        m.global_cardinality([x, y, z], [0, 1, 2], occurrences, False, "BC").post()
        m.get_solver()._propagate()
        self.assertEqual(x.get_domain_values(), [0, 1, 2])

    def testGlobalCardinalityBC2(self):
        m = Model()
        x, y, z = m.intvar([0, 1, 2], name="x"), m.intvar([1, 2], name="y"), m.intvar([1, 2], name="z")
        occurrences = m.intvars(3, 0, 1)
        m.global_cardinality([x, y, z], [0, 1, 2], occurrences, False, "BC").post()
        m.get_solver()._propagate()
        self.assertEqual(x.get_domain_values(), [0])

    def testGlobalCardinalityDefault(self):
        m = Model()
        x, y, z = m.intvar([0, 1, 2], name="x"), m.intvar([1, 2], name="y"), m.intvar([1, 2], name="z")
        occurrences = m.intvars(3, 0, 1)
        m.global_cardinality([x, y, z], [0, 1, 2], occurrences, False, "DEFAULT").post()
        m.get_solver()._propagate()
        self.assertEqual(x.get_domain_values(), [0, 1, 2])

    def testGlobalCardinalitySameSolutions(self):
        counts = []
        for consistency in ["DEFAULT", "BC", "AC"]:
            m = Model()
            intvars = m.intvars(4, 0, 3)
            occurrences = m.intvars(2, 1, 2)
            m.global_cardinality(intvars, [1, 2], occurrences, False, consistency).post()
            counts.append(len(m.get_solver().find_all_solutions()))
        self.assertTrue(counts[0] > 0)
        self.assertEqual(counts[0], counts[1])
        self.assertEqual(counts[0], counts[2])
