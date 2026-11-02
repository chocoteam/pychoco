import unittest

from pychoco.model import Model


class TestSolverReset(unittest.TestCase):

    def test_find_solution_resumes_without_reset(self):
        model = Model()
        x = model.intvar(1, 2, "x")
        values = []
        for _ in range(3):
            sol = model.get_solver().find_solution()
            values.append(None if sol is None else sol.get_int_val(x))
        self.assertEqual(values, [1, 2, None])

    def test_find_solution_with_reset(self):
        # Second scenario of issue #47
        model = Model()
        x = model.intvar(1, 2, "x")
        for _ in range(3):
            solver = model.get_solver()
            solver.reset()
            sol = solver.find_solution()
            self.assertIsNotNone(sol)
            self.assertEqual(sol.get_int_val(x), 1)

    def test_find_optimal_solution_with_reset(self):
        # First scenario of issue #47
        model = Model()
        x = model.intvar(1, 10, "x")
        sol1 = model.get_solver().find_optimal_solution(objective=x, maximize=False)
        self.assertIsNotNone(sol1)
        self.assertEqual(sol1.get_int_val(x), 1)
        model.get_solver().reset()
        sol2 = model.get_solver().find_optimal_solution(objective=x, maximize=False)
        self.assertIsNotNone(sol2)
        self.assertEqual(sol2.get_int_val(x), 1)

    def test_find_all_optimal_solutions_after_find_all_solutions(self):
        model = Model()
        x = model.intvar(1, 5, "x")
        solver = model.get_solver()
        self.assertEqual(len(solver.find_all_solutions()), 5)
        solver.reset()
        sols = solver.find_all_optimal_solutions(x, False)
        self.assertEqual(len(sols), 1)
        self.assertEqual(sols[0].get_int_val(x), 1)

    def test_reset_measures(self):
        model = Model()
        x = model.intvar(1, 5, "x")
        solver = model.get_solver()
        solver.find_all_solutions()
        self.assertEqual(solver.get_solution_count(), 5)
        solver.reset()
        self.assertEqual(solver.get_solution_count(), 0)
        self.assertEqual(len(solver.find_all_solutions()), 5)

    def test_reset_keeps_search_strategy(self):
        model = Model()
        x = model.intvar(1, 5, "x")
        solver = model.get_solver()
        solver.set_input_order_ub_search(x)
        self.assertEqual(solver.find_solution().get_int_val(x), 5)
        solver.reset()
        self.assertEqual(solver.find_solution().get_int_val(x), 5)

    def test_hard_reset(self):
        model = Model()
        x = model.intvar(1, 5, "x")
        solver = model.get_solver()
        solver.set_input_order_ub_search(x)
        self.assertEqual(solver.find_solution().get_int_val(x), 5)
        solver.hard_reset()
        self.assertEqual(solver.get_solution_count(), 0)
        # The declared strategy is dropped: the default search picks the lower bound first
        self.assertEqual(solver.find_solution().get_int_val(x), 1)

    def test_hard_reset_optimization(self):
        model = Model()
        x = model.intvar(1, 10, "x")
        solver = model.get_solver()
        self.assertEqual(solver.find_optimal_solution(x, True).get_int_val(x), 10)
        self.assertIsNone(solver.find_optimal_solution(x, True))
        solver.hard_reset()
        self.assertEqual(solver.find_optimal_solution(x, True).get_int_val(x), 10)
