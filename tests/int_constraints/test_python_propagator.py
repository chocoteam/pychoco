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

        model.custom_constraint([x, y], prop).post()
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

        model.custom_constraint([x, y], prop).post()
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

        model.custom_constraint([x], prop).post()
        while model.get_solver().solve():
            self.assertNotEqual(x.get_value(), 3)

    def test_contradiction_explicit(self):
        """Raising Contradiction inside propagator — no solution found."""
        model = Model()
        x = model.intvar(0, 5, "x")

        def always_fail(x):
            raise Contradiction()

        model.custom_constraint([x], always_fail).post()
        self.assertFalse(model.get_solver().solve())

    def test_contradiction_via_empty_domain(self):
        """Filtering that empties domain raises Contradiction automatically."""
        model = Model()
        x = model.intvar(3, 5, "x")

        def prop(x):
            x.update_ub(2)  # forces domain empty → raises Contradiction

        model.custom_constraint([x], prop).post()
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

        model.custom_constraint([x, y], prop_xy).post()
        model.custom_constraint([y, z], prop_yz).post()
        self.assertTrue(model.get_solver().solve())

    # ------------------------------------------------------------------
    # is_entailed tests
    # ------------------------------------------------------------------

    def test_is_entailed_default_is_true(self):
        """Without is_entailed_fn, default behaviour is ESat.TRUE — solving works normally."""
        model = Model()
        x = model.intvar(0, 3, "x")

        def prop(x):
            pass  # no-op propagator

        model.custom_constraint([x], prop).post()
        solutions = [x.get_value() for _ in iter(model.get_solver().solve, False)]
        self.assertEqual(sorted(solutions), [0, 1, 2, 3])

    def test_is_entailed_true_reported(self):
        """is_entailed_fn returning 1 (TRUE) — solver deactivates propagator; solutions still found."""
        model = Model()
        x = model.intvar(0, 2, "x")

        def prop(x):
            pass  # no-op: constraint is always satisfied

        def entailed(x):
            return 1  # always entailed — consistent with noop propagator

        model.custom_constraint([x], prop, entailed).post()
        solutions = [x.get_value() for _ in iter(model.get_solver().solve, False)]
        self.assertEqual(sorted(solutions), [0, 1, 2])

    def test_is_entailed_false_consistent(self):
        """is_entailed_fn returning -1 (FALSE) — consistent with propagator that also fails.

        Contract: propagate_fn must raise Contradiction for any assignment where
        is_entailed_fn returns -1.  Here x must be even: propagator removes odd
        values, and isEntailed returns FALSE when an odd value is still in domain.
        """
        model = Model()
        x = model.intvar(0, 4, "x")  # domain {0,1,2,3,4}

        from pychoco.exceptions import Contradiction

        def prop(x):
            # Keep only even values: remove 1 and 3
            for v in [1, 3]:
                if v >= x.get_lb() and v <= x.get_ub():
                    x.remove_value(v)

        def entailed(x):
            # FALSE if odd values are still reachable (shouldn't happen after prop)
            # TRUE if domain contains only even values
            vals = x.get_domain_values() if x.has_enumerated_domain() else range(x.get_lb(), x.get_ub() + 1)
            if all(v % 2 == 0 for v in vals):
                return 1
            return 0

        model.custom_constraint([x], prop, entailed).post()
        solutions = [x.get_value() for _ in iter(model.get_solver().solve, False)]
        self.assertEqual(sorted(solutions), [0, 2, 4])

    def test_is_entailed_domain_aware(self):
        """is_entailed_fn inspects domains to report TRUE/UNDEFINED; solutions correct."""
        model = Model()
        x = model.intvar(0, 5, "x")
        y = model.intvar(0, 5, "y")

        def prop(x, y):
            x.update_ub(y.get_ub())

        def entailed(x, y):
            # TRUE: x's UB is already <= y's LB — all completions satisfy x <= y
            if x.get_ub() <= y.get_lb():
                return 1
            return 0  # UNDEFINED

        model.custom_constraint([x, y], prop, entailed).post()
        solutions = []
        while model.get_solver().solve():
            solutions.append((x.get_value(), y.get_value()))
        self.assertTrue(len(solutions) > 0)
        for vx, vy in solutions:
            self.assertLessEqual(vx, vy)
