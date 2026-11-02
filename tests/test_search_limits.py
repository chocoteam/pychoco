import unittest

from pychoco.model import Model


def _permutation_model(n=4):
    model = Model()
    x = model.intvars(n, 0, n - 1)
    model.all_different(x).post()
    return model, x


def _pigeonhole_model(pigeons=7):
    # Pairwise disequalities: infeasible, but not detected by propagation alone.
    model = Model()
    x = model.intvars(pigeons, 0, pigeons - 2)
    for i in range(pigeons):
        for j in range(i + 1, pigeons):
            model.arithm(x[i], "!=", x[j]).post()
    return model, x


class TestRestartLimit(unittest.TestCase):

    def test_find_all_solutions_stops_on_restart_limit(self):
        model, _ = _permutation_model()
        solver = model.get_solver()
        solver.set_restart_on_solutions()
        solutions = solver.find_all_solutions(restart_limit=5)
        self.assertEqual(len(solutions), 5)
        self.assertEqual(solver.get_restart_count(), 5)
        self.assertEqual(solver.get_search_state(), "STOPPED")

    def test_solve(self):
        model, _ = _permutation_model()
        solver = model.get_solver()
        self.assertTrue(solver.solve(restart_limit=10))

    def test_find_solution(self):
        model, x = _permutation_model()
        solver = model.get_solver()
        solution = solver.find_solution(restart_limit=10)
        self.assertIsNotNone(solution)
        self.assertEqual(sorted(solution.get_int_val(v) for v in x), [0, 1, 2, 3])

    def test_find_all_solutions(self):
        model, _ = _permutation_model()
        solver = model.get_solver()
        self.assertEqual(len(solver.find_all_solutions(restart_limit=10)), 24)

    def test_find_optimal_solution(self):
        model, x = _permutation_model()
        solver = model.get_solver()
        solution = solver.find_optimal_solution(x[0], True, restart_limit=10)
        self.assertEqual(solution.get_int_val(x[0]), 3)

    def test_find_all_optimal_solutions(self):
        model, x = _permutation_model()
        solver = model.get_solver()
        solutions = solver.find_all_optimal_solutions(x[0], True, restart_limit=10)
        self.assertEqual(len(solutions), 6)
        for s in solutions:
            self.assertEqual(s.get_int_val(x[0]), 3)


class TestBacktrackLimit(unittest.TestCase):
    # The pigeonhole model is infeasible and needs far more than LIMIT backtracks
    # to be refuted: the search must stop exactly on the backtrack limit.
    LIMIT = 10

    def assertStoppedOnBacktrackLimit(self, solver):
        self.assertEqual(solver.get_search_state(), "STOPPED")
        self.assertEqual(solver.get_backtrack_count(), self.LIMIT)

    def test_pigeonhole_needs_more_backtracks_than_limit(self):
        model, _ = _pigeonhole_model()
        solver = model.get_solver()
        self.assertFalse(solver.solve())
        self.assertEqual(solver.get_search_state(), "TERMINATED")
        self.assertGreater(solver.get_backtrack_count(), self.LIMIT)

    def test_solve(self):
        model, _ = _pigeonhole_model()
        solver = model.get_solver()
        self.assertFalse(solver.solve(backtrack_limit=self.LIMIT))
        self.assertStoppedOnBacktrackLimit(solver)

    def test_find_solution(self):
        model, _ = _pigeonhole_model()
        solver = model.get_solver()
        self.assertIsNone(solver.find_solution(backtrack_limit=self.LIMIT))
        self.assertStoppedOnBacktrackLimit(solver)

    def test_find_all_solutions(self):
        model, _ = _pigeonhole_model()
        solver = model.get_solver()
        self.assertEqual(solver.find_all_solutions(backtrack_limit=self.LIMIT), [])
        self.assertStoppedOnBacktrackLimit(solver)

    def test_find_optimal_solution(self):
        model, x = _pigeonhole_model()
        solver = model.get_solver()
        self.assertIsNone(solver.find_optimal_solution(x[0], True, backtrack_limit=self.LIMIT))
        self.assertStoppedOnBacktrackLimit(solver)

    def test_find_all_optimal_solutions(self):
        model, x = _pigeonhole_model()
        solver = model.get_solver()
        self.assertEqual(solver.find_all_optimal_solutions(x[0], True, backtrack_limit=self.LIMIT), [])
        self.assertStoppedOnBacktrackLimit(solver)

    # restart_limit set to a different, non-binding value: the backtrack limit
    # applied must be backtrack_limit, not restart_limit.

    def test_solve_with_restart_limit(self):
        model, _ = _pigeonhole_model()
        solver = model.get_solver()
        self.assertFalse(solver.solve(restart_limit=100000, backtrack_limit=self.LIMIT))
        self.assertStoppedOnBacktrackLimit(solver)

    def test_find_solution_with_restart_limit(self):
        model, _ = _pigeonhole_model()
        solver = model.get_solver()
        self.assertIsNone(solver.find_solution(restart_limit=100000, backtrack_limit=self.LIMIT))
        self.assertStoppedOnBacktrackLimit(solver)

    def test_find_all_solutions_with_restart_limit(self):
        model, _ = _pigeonhole_model()
        solver = model.get_solver()
        self.assertEqual(solver.find_all_solutions(restart_limit=100000, backtrack_limit=self.LIMIT), [])
        self.assertStoppedOnBacktrackLimit(solver)

    def test_find_optimal_solution_with_restart_limit(self):
        model, x = _pigeonhole_model()
        solver = model.get_solver()
        self.assertIsNone(solver.find_optimal_solution(x[0], True, restart_limit=100000,
                                                       backtrack_limit=self.LIMIT))
        self.assertStoppedOnBacktrackLimit(solver)

    def test_find_all_optimal_solutions_with_restart_limit(self):
        model, x = _pigeonhole_model()
        solver = model.get_solver()
        self.assertEqual(solver.find_all_optimal_solutions(x[0], True, restart_limit=100000,
                                                           backtrack_limit=self.LIMIT), [])
        self.assertStoppedOnBacktrackLimit(solver)


if __name__ == '__main__':
    unittest.main()
