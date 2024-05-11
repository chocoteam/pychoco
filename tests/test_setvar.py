import unittest

from pychoco.model import Model


class TestSetVar(unittest.TestCase):

    def test_create_setvar(self):
        model = Model("MyModel")
        lb = set([0, 1, 2])
        ub = set([0, 1, 2, 3, 4])
        s = model.setvar(lb, ub)
        llb = s.get_lb()
        uub = s.get_ub()
        self.assertEqual(lb, llb)
        self.assertEqual(ub, uub)
        ss = model.setvar(lb, name="ss")
        self.assertEqual(ss.name, "ss")
        self.assertEqual(ss.get_value(), lb)
        sol = model.get_solver().find_solution()
        val = sol.get_set_val(s)
        s1 = model.setvar({}, {1, 2, 3, 5, 12}, name="y")