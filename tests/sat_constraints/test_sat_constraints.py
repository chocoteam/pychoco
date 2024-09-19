import unittest

from pychoco.constraints.cnf.log_op import reified_op, implies_op
from pychoco.model import Model


class TestIfThen(unittest.TestCase):

    def test_add_clauses_logop(self):
        m = Model()
        a = m.intvar(0, 10)
        b = m.intvar(0, 10)
        c = m.intvar(0, 10)
        logop = implies_op(m.arithm(a, ">=", b).reify(), m.arithm(c, "=", 5).reify())
        m.add_clauses_logop(logop)
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            va = s.get_int_val(a)
            vb = s.get_int_val(b)
            vc = s.get_int_val(c)
            if va >= vb:
                self.assertTrue(vc == 5)
            if vc != 5:
                self.assertFalse(va > vb)

    def test_add_clauses(self):
        m = Model()
        pos = m.boolvars(3)
        neg = m.boolvars(3)
        m.arithm(pos[0], "=", neg[0]).post()
        m.add_clauses(pos, neg)
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            p1 = s.get_int_val(pos[0]) == 1
            p2 = s.get_int_val(pos[1]) == 1
            p3 = s.get_int_val(pos[2]) == 1
            n1 = s.get_int_val(neg[0]) == 1
            n2 = s.get_int_val(neg[1]) == 1
            n3 = s.get_int_val(neg[2]) == 1
            self.assertTrue((p1 or p2 or p3) or (not n1 or not n2 or not n3))

    def test_add_clause_true(self):
        m = Model()
        b = m.boolvar()
        m.add_clause_true(b)
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            self.assertTrue(s.get_int_val(b) == 1)


    def test_add_clause_false(self):
        m = Model()
        b = m.boolvar()
        m.add_clause_false(b)
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            self.assertTrue(s.get_int_val(b) == 0)

    def test_add_clauses_bool_eq(self):
        m = Model()
        left = m.boolvar()
        right = m.boolvar()
        m.add_clauses_bool_eq(left, right)
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            b1 = s.get_int_val(left) == 1
            b2 = s.get_int_val(right) == 1
            self.assertTrue(b1 == b2)

    def test_add_clauses_bool_le(self):
        m = Model()
        left = m.boolvar()
        right = m.boolvar()
        m.add_clauses_bool_le(left, right)
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            b1 = s.get_int_val(left) == 1
            b2 = s.get_int_val(right) == 1
            self.assertTrue(b1 <= b2)

    def test_add_clauses_bool_lt(self):
        m = Model()
        left = m.boolvar()
        right = m.boolvar()
        m.add_clauses_bool_lt(left, right)
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            b1 = s.get_int_val(left) == 1
            b2 = s.get_int_val(right) == 1
            self.assertTrue(b1 < b2)

    def test_add_clauses_bool_not(self):
        m = Model()
        left = m.boolvar()
        right = m.boolvar()
        m.add_clauses_bool_not(left, right)
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            b1 = s.get_int_val(left) == 1
            b2 = s.get_int_val(right) == 1
            self.assertTrue(b1 != b2)

    def test_add_clauses_bool_or_array_eq_var(self):
        m = Model()
        bools = m.boolvars(3)
        target = m.boolvar()
        m.add_clauses_bool_or_array_eq_var(bools, target)
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            b1 = s.get_int_val(bools[0]) == 1
            b2 = s.get_int_val(bools[1]) == 1
            b3 = s.get_int_val(bools[2]) == 1
            btarget = s.get_int_val(target) == 1
            self.assertTrue((b1 or b2 or b3) == btarget)

    def test_add_clauses_bool_and_array_eq_var(self):
        m = Model()
        bools = m.boolvars(3)
        target = m.boolvar()
        m.add_clauses_bool_and_array_eq_var(bools, target)
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            b1 = s.get_int_val(bools[0]) == 1
            b2 = s.get_int_val(bools[1]) == 1
            b3 = s.get_int_val(bools[2]) == 1
            btarget = s.get_int_val(target) == 1
            self.assertTrue((b1 and b2 and b3) == btarget)

    def test_add_clauses_bool_or_eq_var(self):
        m = Model()
        left = m.boolvar()
        right = m.boolvar()
        target = m.boolvar()
        m.add_clauses_bool_or_eq_var(left, right, target)
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            b1 = s.get_int_val(left) == 1
            b2 = s.get_int_val(right) == 1
            b3 = s.get_int_val(target) == 1
            self.assertTrue((b1 or b2) == b3)

    def test_add_clauses_bool_and_eq_var(self):
        m = Model()
        left = m.boolvar()
        right = m.boolvar()
        target = m.boolvar()
        m.add_clauses_bool_and_eq_var(left, right, target)
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            b1 = s.get_int_val(left) == 1
            b2 = s.get_int_val(right) == 1
            b3 = s.get_int_val(target) == 1
            self.assertTrue((b1 and b2) == b3)

    def test_add_clauses_bool_xor_eq_var(self):
        m = Model()
        left = m.boolvar()
        right = m.boolvar()
        target = m.boolvar()
        m.add_clauses_bool_xor_eq_var(left, right, target)
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            b1 = s.get_int_val(left) == 1
            b2 = s.get_int_val(right) == 1
            b3 = s.get_int_val(target) == 1
            self.assertTrue((b1 ^ b2) == b3)

    def test_add_clauses_bool_is_eq_var(self):
        m = Model()
        left = m.boolvar()
        right = m.boolvar()
        target = m.boolvar()
        m.add_clauses_bool_is_eq_var(left, right, target)
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            b1 = 1 if s.get_int_val(left) == 1 else 0
            b2 = 1 if s.get_int_val(right) == 1 else 0
            b3 = s.get_int_val(target) == 1
            self.assertTrue((b1 == b2) == b3)

    def test_add_clauses_bool_is_neq_var(self):
        m = Model()
        left = m.boolvar()
        right = m.boolvar()
        target = m.boolvar()
        m.add_clauses_bool_is_neq_var(left, right, target)
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            b1 = 1 if s.get_int_val(left) == 1 else 0
            b2 = 1 if s.get_int_val(right) == 1 else 0
            b3 = s.get_int_val(target) == 1
            self.assertTrue((b1 != b2) == b3)

    def test_add_clauses_bool_is_le_var(self):
        m = Model()
        left = m.boolvar()
        right = m.boolvar()
        target = m.boolvar()
        m.add_clauses_bool_is_le_var(left, right, target)
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            b1 = 1 if s.get_int_val(left) == 1 else 0
            b2 = 1 if s.get_int_val(right) == 1 else 0
            b3 = s.get_int_val(target) == 1
            self.assertTrue((b1 <= b2) == b3)

    def test_add_clauses_bool_is_lt_var(self):
        m = Model()
        left = m.boolvar()
        right = m.boolvar()
        target = m.boolvar()
        m.add_clauses_bool_is_lt_var(left, right, target)
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            b1 = 1 if s.get_int_val(left) == 1 else 0
            b2 = 1 if s.get_int_val(right) == 1 else 0
            b3 = s.get_int_val(target) == 1
            self.assertTrue((b1 < b2) == b3)

    def test_add_clauses_bool_or_array_equal_true(self):
        m = Model()
        bools = m.boolvars(3)
        m.add_clauses_bool_or_array_equal_true(bools)
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            b1 = s.get_int_val(bools[0]) == 1
            b2 = s.get_int_val(bools[1]) == 1
            b3 = s.get_int_val(bools[2]) == 1
            self.assertTrue(b1 or b2 or b3)

    def test_add_clauses_bool_and_array_equal_false(self):
        m = Model()
        bools = m.boolvars(3)
        m.add_clauses_bool_and_array_equal_false(bools)
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            b1 = s.get_int_val(bools[0]) == 1
            b2 = s.get_int_val(bools[1]) == 1
            b3 = s.get_int_val(bools[2]) == 1
            self.assertFalse(b1 and b2 and b3)

    def test_add_clauses_at_most_one(self):
        m = Model()
        bools = m.boolvars(3)
        m.add_clauses_at_most_one(bools)
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            b1 = 1 if s.get_int_val(bools[0]) == 1 else 0
            b2 = 1 if s.get_int_val(bools[1]) == 1 else 0
            b3 = 1 if s.get_int_val(bools[2]) == 1 else 0

    def test_add_clauses_at_most_n_minus_one(self):
        m = Model()
        bools = m.boolvars(3)
        m.add_clauses_at_most_n_minus_one(bools)
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            b1 = 1 if s.get_int_val(bools[0]) == 1 else 0
            b2 = 1 if s.get_int_val(bools[1]) == 1 else 0
            b3 = 1 if s.get_int_val(bools[2]) == 1 else 0
            self.assertTrue(sum([b1, b2, b3]) <= 2)

    def test_add_clauses_sum_bool_array_greater_eq_var(self):
        m = Model()
        bools = m.boolvars(3)
        target = m.boolvar()
        m.add_clauses_sum_bool_array_greater_eq_var(bools, target)
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            b1 = 1 if s.get_int_val(bools[0]) == 1 else 0
            b2 = 1 if s.get_int_val(bools[1]) == 1 else 0
            b3 = 1 if s.get_int_val(bools[2]) == 1 else 0
            btarget = 1 if s.get_int_val(target) == 1 else 0
            self.assertTrue(sum([b1, b2, b3]) >= btarget)

    def test_add_clauses_max_bool_array_less_eq_var(self):
        m = Model()
        bools = m.boolvars(3)
        target = m.boolvar()
        m.add_clauses_max_bool_array_less_eq_var(bools, target)
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            b1 = 1 if s.get_int_val(bools[0]) == 1 else 0
            b2 = 1 if s.get_int_val(bools[1]) == 1 else 0
            b3 = 1 if s.get_int_val(bools[2]) == 1 else 0
            btarget = 1 if s.get_int_val(target) == 1 else 0
            self.assertTrue(max([b1, b2, b3]) <= btarget)

    def test_add_clauses_sum_bool_array_less_eq_var(self):
        m = Model()
        bools = m.boolvars(3)
        target = m.boolvar()
        m.add_clauses_sum_bool_array_less_eq_var(bools, target)
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            b1 = 1 if s.get_int_val(bools[0]) == 1 else 0
            b2 = 1 if s.get_int_val(bools[1]) == 1 else 0
            b3 = 1 if s.get_int_val(bools[2]) == 1 else 0
            btarget = 1 if s.get_int_val(target) == 1 else 0
            self.assertTrue(sum([b1, b2, b3]) <= btarget * 3)

    def test_add_constructive_disjunction(self):
        m = Model()
        a = m.intvar(0, 2)
        b = m.intvar(0, 2)
        c = m.intvar(0, 2)
        c1 = m.arithm(a, "=", 0)
        c2 = m.arithm(b, "=", 1)
        c3 = m.arithm(c, "=", 2)
        cons = [c1, c2, c3]
        m.add_constructive_disjunction(cons)
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            b1 = s.get_int_val(a) == 0
            b2 = s.get_int_val(b) == 1
            b3 = s.get_int_val(c) == 2
            self.assertTrue(b1 or b2 or b3)
