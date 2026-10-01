import gc
import unittest

from pychoco import Model
from pychoco.solver import _VAR_SEL_FN, _VAL_SEL_FN


class TestCustomSearch(unittest.TestCase):

    def test_lower_bound_val_selector(self):
        """Custom search: input-order var selector + lower-bound val selector."""
        model = Model()
        x = model.intvar(0, 5, "x")
        y = model.intvar(0, 5, "y")

        def var_sel(variables):
            unfix = [v for v in variables if v.get_lb() != v.get_ub()]
            return unfix[0] if unfix else None

        def val_sel(var):
            return var.get_lb()

        solver = model.get_solver()
        solver.set_custom_search([x, y], var_sel, val_sel)
        self.assertTrue(solver.solve())
        self.assertGreaterEqual(x.get_value(), 0)
        self.assertGreaterEqual(y.get_value(), 0)

    def test_upper_bound_val_selector(self):
        """Custom search: upper-bound val selector yields descending values."""
        model = Model()
        x = model.intvar(0, 5, "x")

        def var_sel(variables):
            unfix = [v for v in variables if v.get_lb() != v.get_ub()]
            return unfix[0] if unfix else None

        def val_sel(var):
            return var.get_ub()

        solver = model.get_solver()
        solver.set_custom_search([x], var_sel, val_sel)
        self.assertTrue(solver.solve())
        self.assertEqual(x.get_value(), 5)

    def test_smallest_domain_first(self):
        """Custom search: smallest-domain var selector."""
        model = Model()
        x = model.intvar(0, 10, "x")
        y = model.intvar(3, 4, "y")

        def smallest_domain(variables):
            unfix = [v for v in variables if v.get_lb() != v.get_ub()]
            return min(unfix, key=lambda v: v.get_ub() - v.get_lb()) if unfix else None

        def val_sel(var):
            return var.get_lb()

        solver = model.get_solver()
        solver.set_custom_search([x, y], smallest_domain, val_sel)
        self.assertTrue(solver.solve())

    def test_all_solutions_count(self):
        """Custom search enumerates the same number of solutions as default."""
        def count_solutions(use_custom):
            model = Model()
            x = model.intvar(0, 2, "x")
            y = model.intvar(0, 2, "y")
            if use_custom:
                def var_sel(variables):
                    unfix = [v for v in variables if v.get_lb() != v.get_ub()]
                    return unfix[0] if unfix else None
                def val_sel(var):
                    return var.get_lb()
                model.get_solver().set_custom_search([x, y], var_sel, val_sel)
            count = 0
            while model.get_solver().solve():
                count += 1
            return count

        self.assertEqual(count_solutions(False), count_solutions(True))

    def test_callbacks_outlive_temporary_solver(self):
        """Selectors stay alive when set through a temporary Solver wrapper.

        get_solver() returns a new wrapper each time: the native solver must
        not be left with the addresses of freed ctypes callbacks.
        """
        def alive_callbacks():
            gc.collect()
            return sum(isinstance(o, (_VAR_SEL_FN, _VAL_SEL_FN)) for o in gc.get_objects())

        model = Model()
        x = model.intvar(0, 2, "x")
        y = model.intvar(0, 2, "y")

        def var_sel(variables):
            unfix = [v for v in variables if v.get_lb() != v.get_ub()]
            return unfix[0] if unfix else None

        def val_sel(var):
            return var.get_lb()

        before = alive_callbacks()
        model.get_solver().set_custom_search([x, y], var_sel, val_sel)
        self.assertEqual(alive_callbacks(), before + 2)

        # Callbacks that would take over the freed slots, were the selectors freed.
        impostor_calls = []

        def impostor_var():
            impostor_calls.append("var")
            return -1

        def impostor_val(_idx):
            impostor_calls.append("val")
            return 0

        impostors = [_VAR_SEL_FN(impostor_var) for _ in range(50)]
        impostors += [_VAL_SEL_FN(impostor_val) for _ in range(50)]

        count = 0
        while model.get_solver().solve():
            count += 1
        self.assertEqual(count, 9)
        self.assertEqual(impostor_calls, [])
        del impostors

    def test_custom_search_with_constraint(self):
        """Custom search works alongside posted constraints."""
        model = Model()
        x = model.intvar(0, 5, "x")
        y = model.intvar(0, 5, "y")
        model.arithm(x, "<", y).post()

        def var_sel(variables):
            unfix = [v for v in variables if v.get_lb() != v.get_ub()]
            return unfix[0] if unfix else None

        def val_sel(var):
            return var.get_lb()

        solver = model.get_solver()
        solver.set_custom_search([x, y], var_sel, val_sel)

        solutions = []
        while solver.solve():
            solutions.append((x.get_value(), y.get_value()))

        self.assertTrue(len(solutions) > 0)
        for vx, vy in solutions:
            self.assertLess(vx, vy)
