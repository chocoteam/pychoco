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
        model = Model()
        a = model.intvar(0, 10)
        b = model.intvar(0, 5)
        c = model.intvar(2, 7)
        d = model.intvar(1, 2)
        e = model.intvar(0, 20)
        model.all_different([a, b, c, d, e]).post()
        model.square(a, d).post()
        solver = model.get_solver()
        solver.show_restarts()
        solutions = solver.find_all_solutions(solution_limit=10)
        self.assertEqual(len(solutions), 10)

    def test_time_limit(self):
        model = Model("MyModel")
        a = model.intvar(0, 10)
        b = model.intvar(0, 10)
        c = model.intvar(0, 10)
        d = model.intvar(0, 10)
        e = model.intvar(0, 10)
        model.all_different([a, b, c, d, e]).post()
        model.square(a, d).post()
        solver = model.get_solver()
        solver.show_statistics()
        solver.find_all_solutions(time_limit="2s")

    def test_find_all_optimal_solutions(self):
        model = Model()
        x = model.intvars(4, 0, 3)
        n = model.intvar(0, 10)
        model.n_values(x, n).post()
        solver = model.get_solver()
        solver.show_short_statistics()
        solver.find_all_optimal_solutions(n, True)

    def test_find_optimal_solutions(self):
        model = Model()
        x = model.intvars(4, 0, 3)
        n = model.intvar(0, 10)
        model.n_values(x, n).post()
        solver = model.get_solver()
        solver.show_short_statistics()
        solver.find_optimal_solution(n, True)
        self.assertTrue(solver.is_objective_optimal())

    def test_add_rem_hints(self):
        model = Model()
        x = model.intvars(4, 0, 3)
        n = model.intvar(0, 10)
        model.n_values(x, n).post()
        solver = model.get_solver()
        solver.add_hint(x[0], 0)
        solver.add_hint(x[1], 1)
        solver.add_hint(x[2], 2)
        solver.add_hint(x[3], 3)
        solver.show_short_statistics()
        solver.find_optimal_solution(n, True)
        solver.rem_hints()

    def test_propagate_push_pop_state(self):
        model = Model()
        x = model.intvars(4, 0, 3)
        n = model.intvar(0, 10)
        model.n_values(x, n).post()
        solver = model.get_solver()
        solver._propagate()
        solver._push_state()
        solver._pop_state()

    def test_getters(self):
        model = Model("MyModel")
        a = model.intvar(0, 10)
        b = model.intvar(0, 10)
        c = model.intvar(0, 10)
        d = model.intvar(0, 10)
        e = model.intvar(0, 10)
        model.all_different([a, b, c, d, e]).post()
        model.square(a, d).post()
        solver = model.get_solver()
        solver.show_statistics()
        solver.find_all_solutions(time_limit="2s")
        self.assertLessEqual(solver.get_time_count(), 2)
        self.assertEqual(solver.get_search_state(), "TERMINATED")
        solver.get_node_count()
        solver.get_backtrack_count()
        solver.get_fail_count()
        solver.get_restart_count()

