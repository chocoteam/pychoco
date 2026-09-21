import unittest

from pychoco import Model
from pychoco import backend


class TestPythonPropagator(unittest.TestCase):

    def test_upper_bound_filtering(self):
        """Propagator filters UB of x according to UB of y."""
        model = Model()
        x = model.intvar(0, 10, "x")
        y = model.intvar(0, 5, "y")

        def prop(vars_handle, nvars):
            h_x = backend.intvar_array_get(vars_handle, 0)
            h_y = backend.intvar_array_get(vars_handle, 1)
            ub_y = backend.get_intvar_ub(h_y)
            result = backend.update_intvar_ub(h_x, ub_y)
            return 0 if result >= 0 else -1

        model.python_propagator([x, y], prop).post()
        solutions = []
        while model.get_solver().solve():
            solutions.append((x.get_value(), y.get_value()))
        self.assertTrue(len(solutions) > 0)
        for vx, vy in solutions:
            self.assertLessEqual(vx, vy)

    def test_contradiction(self):
        """Returning -1 triggers backtracking — no solution found."""
        model = Model()
        x = model.intvar(0, 5, "x")

        def always_fail(vars_handle, nvars):
            return -1

        model.python_propagator([x], always_fail).post()
        self.assertFalse(model.get_solver().solve())

    def test_multiple_propagators(self):
        """Multiple Python propagators can coexist in the same model."""
        model = Model()
        x = model.intvar(0, 10)
        y = model.intvar(0, 10)
        z = model.intvar(0, 10)

        def prop_xy(h, n):  # enforce x <= y
            hx = backend.intvar_array_get(h, 0)
            hy = backend.intvar_array_get(h, 1)
            r = backend.update_intvar_ub(hx, backend.get_intvar_ub(hy))
            return 0 if r >= 0 else -1

        def prop_yz(h, n):  # enforce y <= z
            hy = backend.intvar_array_get(h, 0)
            hz = backend.intvar_array_get(h, 1)
            r = backend.update_intvar_ub(hy, backend.get_intvar_ub(hz))
            return 0 if r >= 0 else -1

        model.python_propagator([x, y], prop_xy).post()
        model.python_propagator([y, z], prop_yz).post()
        self.assertTrue(model.get_solver().solve())
