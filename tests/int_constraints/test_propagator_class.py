import unittest

from pychoco import Model, Propagator
from pychoco.exceptions import Contradiction


class TestPropagatorClass(unittest.TestCase):

    def test_basic_ub_filtering(self):
        """Class-based propagator filters UB of x according to UB of y."""
        model = Model()
        x = model.intvar(0, 10, "x")
        y = model.intvar(0, 5, "y")

        class UBSync(Propagator):
            def propagate(self):
                self.vars[0].update_ub(self.vars[1].get_ub())

        UBSync([x, y]).post()
        solutions = []
        while model.get_solver().solve():
            solutions.append((x.get_value(), y.get_value()))
        self.assertTrue(len(solutions) > 0)
        for vx, vy in solutions:
            self.assertLessEqual(vx, vy)

    def test_instance_attribute(self):
        """Propagator instance attributes are preserved across calls."""
        model = Model()
        x = model.intvar(0, 3, "x")

        class CountingProp(Propagator):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.call_count = 0

            def propagate(self):
                self.call_count += 1

        prop = CountingProp([x])
        prop.post()
        solutions = list(iter(model.get_solver().solve, False))
        self.assertEqual(len(solutions), 4)
        self.assertGreater(prop.call_count, 0)

    def test_contradiction_via_raise(self):
        """Raising Contradiction inside propagate — no solution found."""
        model = Model()
        x = model.intvar(0, 5, "x")

        class AlwaysFail(Propagator):
            def propagate(self):
                raise Contradiction()

        AlwaysFail([x]).post()
        self.assertFalse(model.get_solver().solve())

    def test_is_entailed_override(self):
        """Overriding is_entailed works correctly."""
        model = Model()
        x = model.intvar(0, 4, "x")

        class EvenOnly(Propagator):
            def propagate(self):
                for v in [1, 3]:
                    if self.vars[0].get_lb() <= v <= self.vars[0].get_ub():
                        self.vars[0].remove_value(v)

            def is_entailed(self):
                v = self.vars[0]
                vals = (v.get_domain_values() if v.has_enumerated_domain()
                        else range(v.get_lb(), v.get_ub() + 1))
                return 1 if all(i % 2 == 0 for i in vals) else 0

        EvenOnly([x]).post()
        solutions = [x.get_value() for _ in iter(model.get_solver().solve, False)]
        self.assertEqual(sorted(solutions), [0, 2, 4])

    def test_priority_parameter(self):
        """Custom priority is accepted without error."""
        model = Model()
        x = model.intvar(0, 5, "x")

        class SlowProp(Propagator):
            def propagate(self):
                pass

        SlowProp([x], priority=7).post()
        self.assertTrue(model.get_solver().solve())

    def test_post_twice_raises(self):
        """Posting the same instance twice raises RuntimeError."""
        model = Model()
        x = model.intvar(0, 5, "x")

        class Noop(Propagator):
            def propagate(self):
                pass

        prop = Noop([x])
        prop.post()
        with self.assertRaises(RuntimeError):
            prop.post()

    def test_multiple_propagators(self):
        """Multiple class-based propagators coexist correctly."""
        model = Model()
        x = model.intvar(0, 10)
        y = model.intvar(0, 10)
        z = model.intvar(0, 10)

        class UBSync(Propagator):
            def propagate(self):
                self.vars[0].update_ub(self.vars[1].get_ub())

        UBSync([x, y]).post()
        UBSync([y, z]).post()
        self.assertTrue(model.get_solver().solve())
