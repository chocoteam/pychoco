import unittest

from pychoco.model import Model


class TestAllDifferent(unittest.TestCase):

    def testAllDifferent1(self):
        m = Model()
        variables = m.intvars(3, 0, 2)
        m.all_different(variables).post()
        solutions = m.get_solver().find_all_solutions()
        self.assertEqual(len(solutions), 6)
        for s in solutions:
            self.assertNotEqual(s.get_int_val(variables[0]), s.get_int_val(variables[1]))
            self.assertNotEqual(s.get_int_val(variables[0]), s.get_int_val(variables[2]))
            self.assertNotEqual(s.get_int_val(variables[1]), s.get_int_val(variables[2]))

    def testAllDifferentAC(self):
        m = Model()
        x, y, z = m.intvar([0,1, 2], name="x"), m.intvar([0, 2], name= "y"), m.intvar([0, 2], name= "z"), 
        variables = [x, y, z]
        m.all_different(variables, "AC").post()
        m.get_solver()._propagate()
        self.assertEqual(x.get_domain_values(), [1])

    def testAllDifferentBC1(self):
        m = Model()
        x, y, z = m.intvar([0, 1, 2], name="x"), m.intvar([0, 2], name= "y"), m.intvar([0, 2], name= "z"), 
        variables = [x, y, z]
        m.all_different(variables, "BC").post()
        m.get_solver()._propagate()
        self.assertEqual(x.get_domain_values(), [0,1,2])

    def testAllDifferentBC2(self):
        m = Model()
        x, y, z = m.intvar([0, 1, 2], name="x"), m.intvar([1, 2], name= "y"), m.intvar([1, 2], name= "z"), 
        variables = [x, y, z]
        m.all_different(variables, "BC").post()
        m.get_solver()._propagate()
        self.assertEqual(x.get_domain_values(), [0])

    def testAllDifferentFail(self):
        m = Model()
        variables = m.intvars(3, 0, 1)
        m.all_different(variables).post()
        solution = m.get_solver().find_solution()
        self.assertIsNone(solution)
