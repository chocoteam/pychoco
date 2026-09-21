import unittest

from pychoco import Model
from pychoco.exceptions import Contradiction


class TestPythonPropagator(unittest.TestCase):

    def test_upper_bound_filtering(self):
        """Propagator enforces x <= y by filtering UB of x."""
        model = Model()
        x = model.intvar(0, 10, "x")
        y = model.intvar(0, 5, "y")

        def prop(x, y):
            x.update_ub(y.get_ub())

        model.python_propagator([x, y], prop).post()
        solutions = []
        while model.get_solver().solve():
            solutions.append((x.get_value(), y.get_value()))
        self.assertTrue(len(solutions) > 0)
        for vx, vy in solutions:
            self.assertLessEqual(vx, vy)

    def test_lower_bound_filtering(self):
        """Propagator enforces x >= y by filtering LB of x."""
        model = Model()
        x = model.intvar(0, 10, "x")
        y = model.intvar(5, 10, "y")

        def prop(x, y):
            x.update_lb(y.get_lb())

        model.python_propagator([x, y], prop).post()
        solutions = []
        while model.get_solver().solve():
            solutions.append((x.get_value(), y.get_value()))
        self.assertTrue(len(solutions) > 0)
        for vx, vy in solutions:
            self.assertGreaterEqual(vx, vy)

    def test_remove_value(self):
        """Propagator removes a specific value from x's domain."""
        model = Model()
        x = model.intvar(0, 5, "x")

        def prop(x):
            x.remove_value(3)

        model.python_propagator([x], prop).post()
        while model.get_solver().solve():
            self.assertNotEqual(x.get_value(), 3)

    def test_contradiction_explicit(self):
        """Raising Contradiction inside propagator — no solution found."""
        model = Model()
        x = model.intvar(0, 5, "x")

        def always_fail(x):
            raise Contradiction()

        model.python_propagator([x], always_fail).post()
        self.assertFalse(model.get_solver().solve())

    def test_contradiction_via_empty_domain(self):
        """Filtering that empties domain raises Contradiction automatically."""
        model = Model()
        x = model.intvar(3, 5, "x")

        def prop(x):
            x.update_ub(2)  # forces domain empty → raises Contradiction

        model.python_propagator([x], prop).post()
        self.assertFalse(model.get_solver().solve())

    def test_multiple_propagators(self):
        """Multiple Python propagators can coexist in the same model."""
        model = Model()
        x = model.intvar(0, 10)
        y = model.intvar(0, 10)
        z = model.intvar(0, 10)

        def prop_xy(x, y):
            x.update_ub(y.get_ub())

        def prop_yz(y, z):
            y.update_ub(z.get_ub())

        model.python_propagator([x, y], prop_xy).post()
        model.python_propagator([y, z], prop_yz).post()
        self.assertTrue(model.get_solver().solve())
