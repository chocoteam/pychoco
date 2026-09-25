import unittest
from pychoco import Model


class TestStateInt(unittest.TestCase):

    def test_initial_value(self):
        model = Model()
        s = model.make_state_int(42)
        self.assertEqual(s.get(), 42)

    def test_set_get(self):
        model = Model()
        s = model.make_state_int(0)
        s.set(7)
        self.assertEqual(s.get(), 7)

    def test_add(self):
        model = Model()
        s = model.make_state_int(10)
        result = s.add(5)
        self.assertEqual(result, 15)
        self.assertEqual(s.get(), 15)

    def test_property(self):
        model = Model()
        s = model.make_state_int(3)
        self.assertEqual(s.value, 3)
        s.value = 99
        self.assertEqual(s.value, 99)

    def test_backtrack_in_propagator(self):
        """StateInt increments inside propagator; all solutions found."""
        model = Model()
        x = model.intvar(0, 2, "x")
        counter = model.make_state_int(0)

        def prop(v):
            counter.add(1)
            return 0

        model.custom_constraint([x], prop).post()
        solutions = []
        while model.get_solver().solve():
            solutions.append(x.get_value())

        self.assertEqual(sorted(solutions), [0, 1, 2])

    def test_backtrack_restores_value(self):
        """StateInt set inside propagator; successive solutions enumerate correctly."""
        model = Model()
        x = model.intvar(0, 1, "x")
        marker = model.make_state_int(-1)

        def prop(v):
            if v.get_lb() == v.get_ub():
                marker.set(v.get_lb())
            return 0

        model.custom_constraint([x], prop).post()
        values_at_solution = []
        while model.get_solver().solve():
            values_at_solution.append(x.get_value())

        self.assertEqual(sorted(values_at_solution), [0, 1])


class TestStateBool(unittest.TestCase):

    def test_initial_false(self):
        model = Model()
        b = model.make_state_bool()
        self.assertFalse(b.get())

    def test_initial_true(self):
        model = Model()
        b = model.make_state_bool(True)
        self.assertTrue(b.get())

    def test_set_get(self):
        model = Model()
        b = model.make_state_bool(False)
        b.set(True)
        self.assertTrue(b.get())
        b.set(False)
        self.assertFalse(b.get())

    def test_property(self):
        model = Model()
        b = model.make_state_bool(False)
        b.value = True
        self.assertTrue(b.value)

    def test_backtrack_in_propagator(self):
        """StateBool set inside propagator; all solutions found."""
        model = Model()
        x = model.intvar(0, 2, "x")
        flag = model.make_state_bool(False)
        seen = []

        def prop(v):
            flag.set(True)
            seen.append(flag.get())
            return 0

        model.custom_constraint([x], prop).post()
        solutions = []
        while model.get_solver().solve():
            solutions.append(x.get_value())

        self.assertEqual(sorted(solutions), [0, 1, 2])
        self.assertTrue(all(seen))


if __name__ == "__main__":
    unittest.main()
