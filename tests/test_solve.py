import math
import unittest

from pychoco.model import Model


class TestSolver(unittest.TestCase):

    def test_find_solution(self):
        model = Model("MyModel")
        a = model.intvar(0, 10)
        b = model.intvar(0, 5)
        c = model.intvar(2, 7)
        d = model.intvar(1, 2)
        e = model.intvar(0, 20)
        model.all_different([a, b, c, d, e]).post()
        model.square(a, d).post()
        model.arithm(c, "+", e, "<=", a).post()
        solver = model.get_solver()
        solution = solver.find_solution()
        self.assertNotEqual(solution.get_int_val(a), solution.get_int_val(b))
        self.assertNotEqual(solution.get_int_val(a), solution.get_int_val(c))
        self.assertNotEqual(solution.get_int_val(a), solution.get_int_val(d))
        self.assertNotEqual(solution.get_int_val(a), solution.get_int_val(e))
        self.assertNotEqual(solution.get_int_val(b), solution.get_int_val(c))
        self.assertNotEqual(solution.get_int_val(c), solution.get_int_val(d))
        self.assertNotEqual(solution.get_int_val(d), solution.get_int_val(e))
        self.assertEqual(solution.get_int_val(a), math.pow(solution.get_int_val(d), 2))
        self.assertTrue(solution.get_int_val(c) + solution.get_int_val(e) <= solution.get_int_val(a))

    def test_find_10_solutions(self):
        model = Model("MyModel")
        a = model.intvar(0, 10)
        b = model.intvar(0, 5)
        c = model.intvar(2, 7)
        d = model.intvar(1, 2)
        e = model.intvar(0, 20)
        model.all_different([a, b, c, d, e]).post()
        model.square(a, d).post()
        solver = model.get_solver()
        solutions = solver.find_all_solutions(solution_limit=10)
        self.assertEqual(len(solutions), 10)
