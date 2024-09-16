import unittest

from pychoco.model import Model


class TestIfThen(unittest.TestCase):

    def testIfThen1(self):
        m = Model()

        x = m.intvar(0,10)
        y = m.intvar(0,100)

        m.if_then(m.arithm(x, "<", 10),
                  m.arithm(y, ">", 42))

        solutions = m.get_solver().find_all_solutions()
        for s in solutions:
            if_cond = s.get_int_val(x) < 10
            then_cond = s.get_int_val(y) > 42
            self.assertTrue(~if_cond or then_cond)

    def testIfThenBool(self):
        m = Model()

        y = m.intvar(0,100)
        b = m.boolvar()

        m.if_then(b, m.arithm(y, ">", 42))

        solutions = m.get_solver().find_all_solutions()
        for s in solutions:
            if_cond = s.get_int_val(b) == 1
            then_cond = s.get_int_val(y) > 42
            self.assertTrue(~if_cond or then_cond)

    def testImplies(self):
        m = Model()

        x = m.intvar(0,10)
        b = m.boolvar()

        cons = m.arithm(x, "<", 10)
        cons.implies(b)

        solutions = m.get_solver().find_all_solutions()
        for s in solutions:
            if_cond = s.get_int_val(x) < 10
            then_cond = bool(s.get_int_val(b))
            self.assertTrue(~if_cond or then_cond)


    def testImpliedBy(self):
        m = Model()

        x = m.intvar(0, 10)
        b = m.boolvar()

        cons = m.arithm(x, "<", 10)
        cons.implied_by(b)

        solutions = m.get_solver().find_all_solutions()
        for s in solutions:
            if_cond = bool(s.get_int_val(b))
            then_cond = s.get_int_val(x) < 10
            self.assertTrue(~if_cond or then_cond)

    def test_if_then_else(self):
        m = Model()
        x = m.intvar(0, 10)
        y = m.intvar(0, 10)
        cstr1 = m.arithm(x, ">", y)
        cstr2 = m.arithm(y, ">=", 5)
        cstr3 = m.arithm(y, "<=", 3)
        m.if_then_else(cstr1, cstr2, cstr3)
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            if s.get_int_val(x) > s.get_int_val(y):
                self.assertTrue(s.get_int_val(y) >= 5)
            else:
                self.assertTrue(s.get_int_val(y) <= 3)

    def test_if_then_else_bool(self):
        m = Model()
        x = m.intvar(0, 10)
        y = m.intvar(0, 10)
        b = m.boolvar()
        cstr2 = m.arithm(y, ">=", 5)
        cstr3 = m.arithm(y, "<=", 3)
        m.if_then_else(b, cstr2, cstr3)
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            if s.get_int_val(b) == 1:
                self.assertTrue(s.get_int_val(y) >= 5)
            else:
                self.assertTrue(s.get_int_val(y) <= 3)

    def test_if_only_if(self):
        m = Model()
        x = m.intvar(0, 10)
        y = m.intvar(0, 10)
        cstr1 = m.arithm(x, ">", y)
        cstr2 = m.arithm(y, ">=", 5)
        m.if_only_if(cstr1, cstr2)
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            b1 = s.get_int_val(x) > s.get_int_val(y)
            b2 = s.get_int_val(y) >= 5
            self.assertEqual(b1, b2)

    def test_if_only_if_bool(self):
        m = Model()
        x = m.intvar(0, 10)
        y = m.intvar(0, 10)
        cstr1 = m.arithm(x, ">", y)
        b = m.boolvar()
        m.if_only_if(b, cstr1)
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            b1 = s.get_int_val(x) > s.get_int_val(y)
            b2 = s.get_int_val(b) == 1
            self.assertEqual(b1, b2)

    def test_reify_x_eq_y(self):
        m = Model()
        x = m.intvar(0, 10)
        y = m.intvar(0, 10)
        b = m.boolvar()
        m.reify_x_eq_y(x, y, b)
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            b1 = s.get_int_val(x) == s.get_int_val(y)
            b2 = s.get_int_val(b) == 1
            self.assertEqual(b1, b2)

    def test_reify_x_eq_c(self):
        m = Model()
        x = m.intvar(0, 10)
        y = 5
        b = m.boolvar()
        m.reify_x_eq_y(x, y, b)
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            b1 = s.get_int_val(x) == y
            b2 = s.get_int_val(b) == 1
            self.assertEqual(b1, b2)

    def test_reify_x_ne_y(self):
        m = Model()
        x = m.intvar(0, 10)
        y = m.intvar(0, 10)
        b = m.boolvar()
        m.reify_x_ne_y(x, y, b)
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            b1 = s.get_int_val(x) != s.get_int_val(y)
            b2 = s.get_int_val(b) == 1
            self.assertEqual(b1, b2)

    def test_reify_x_ne_c(self):
        m = Model()
        x = m.intvar(0, 10)
        y = 5
        b = m.boolvar()
        m.reify_x_ne_y(x, y, b)
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            b1 = s.get_int_val(x) != y
            b2 = s.get_int_val(b) == 1
            self.assertEqual(b1, b2)

    def test_reify_x_eq_yc(self):
        m = Model()
        x = m.intvar(0, 10)
        y = m.intvar(0, 10)
        c = 2
        b = m.boolvar()
        m.reify_x_eq_yc(x, y, c, b)
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            b1 = s.get_int_val(x) == s.get_int_val(y) + c
            b2 = s.get_int_val(b) == 1
            self.assertEqual(b1, b2)

    def test_reify_x_ne_yc(self):
        m = Model()
        x = m.intvar(0, 10)
        y = m.intvar(0, 10)
        c = 2
        b = m.boolvar()
        m.reify_x_ne_yc(x, y, c, b)
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            b1 = s.get_int_val(x) != s.get_int_val(y) + c
            b2 = s.get_int_val(b) == 1
            self.assertEqual(b1, b2)

    def test_reify_x_lt_y(self):
        m = Model()
        x = m.intvar(0, 10)
        y = m.intvar(0, 10)
        b = m.boolvar()
        m.reify_x_lt_y(x, y, b)
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            b1 = s.get_int_val(x) < s.get_int_val(y)
            b2 = s.get_int_val(b) == 1
            self.assertEqual(b1, b2)

    def test_reify_x_gt_y(self):
        m = Model()
        x = m.intvar(0, 10)
        y = m.intvar(0, 10)
        b = m.boolvar()
        m.reify_x_gt_y(x, y, b)
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            b1 = s.get_int_val(x) > s.get_int_val(y)
            b2 = s.get_int_val(b) == 1
            self.assertEqual(b1, b2)

    def test_reify_x_le_y(self):
        m = Model()
        x = m.intvar(0, 10)
        y = m.intvar(0, 10)
        b = m.boolvar()
        m.reify_x_le_y(x, y, b)
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            b1 = s.get_int_val(x) <= s.get_int_val(y)
            b2 = s.get_int_val(b) == 1
            self.assertEqual(b1, b2)

    def test_reify_x_ge_y(self):
        m = Model()
        x = m.intvar(0, 10)
        y = m.intvar(0, 10)
        b = m.boolvar()
        m.reify_x_ge_y(x, y, b)
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            b1 = s.get_int_val(x) >= s.get_int_val(y)
            b2 = s.get_int_val(b) == 1
            self.assertEqual(b1, b2)

    def test_reify_x_lt_yc(self):
        m = Model()
        x = m.intvar(0, 10)
        y = m.intvar(0, 10)
        c = 2
        b = m.boolvar()
        m.reify_x_lt_yc(x, y, c, b)
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            b1 = s.get_int_val(x) < s.get_int_val(y) + c
            b2 = s.get_int_val(b) == 1
            self.assertEqual(b1, b2)

    def test_reify_x_gt_yc(self):
        m = Model()
        x = m.intvar(0, 10)
        y = m.intvar(0, 10)
        c = 2
        b = m.boolvar()
        m.reify_x_gt_yc(x, y, c, b)
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            b1 = s.get_int_val(x) > s.get_int_val(y) + c
            b2 = s.get_int_val(b) == 1
            self.assertEqual(b1, b2)

    def test_reify_x_in_s(self):
        m = Model()
        x = m.intvar(0, 10)
        s = [1, 3, 5, 7]
        b = m.boolvar()
        m.reify_x_in_s(x, s, b)
        sols = m.get_solver().find_all_solutions()
        for sol in sols:
            b1 = sol.get_int_val(x) in s
            b2 = sol.get_int_val(b) == 1
            self.assertEqual(b1, b2)

    def test_reify_x_not_in_s(self):
        m = Model()
        x = m.intvar(0, 10)
        s = [1, 3, 5, 7]
        b = m.boolvar()
        m.reify_x_not_in_s(x, s, b)
        sols = m.get_solver().find_all_solutions()
        for sol in sols:
            b1 = sol.get_int_val(x) not in s
            b2 = sol.get_int_val(b) == 1
            self.assertEqual(b1, b2)