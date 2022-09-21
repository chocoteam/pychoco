import unittest

from pychoco.model import Model


class TestAbsolute(unittest.TestCase):

    def testAbsolute1(self):
        m = Model()
        x = m.intvar(0, 20)
        y = m.intvar(-10, 10)
        m.absolute(x, y).post()
        solutions = m.get_solver().find_all_solutions()
        for s in solutions:
            self.assertEqual(s.get_int_val(x), abs(s.get_int_val(y)))
        self.assertEqual(len(solutions), 21)

    def testFail(self):
        m = Model()
        x = m.intvar(-10, -4)
        y = m.intvar(-10, 10)
        m.absolute(x, y).post()
        solution = m.get_solver().find_solution()
        self.assertIsNone(solution)
