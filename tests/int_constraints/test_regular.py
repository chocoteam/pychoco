import unittest

from pychoco import create_model, create_finite_automaton


class TestRegular(unittest.TestCase):

    def testRegular1(self):
        model = create_model()
        n = 10
        intvars = model.intvars(n, 0, 2)
        auto = create_finite_automaton()
        start = auto.add_state()
        end = auto.add_state()
        auto.set_initial_state(start)
        auto.set_final(start)
        auto.set_final(end)
        auto.add_transition(start, start, 0, 1)
        auto.add_transition(start, end, 2)
        auto.add_transition(end, start, 2)
        auto.add_transition(end, start, 0, 1)
        model.regular(intvars, auto).post()
        model.get_solver().set_input_order_lb_search(*intvars)
        while model.get_solver().solve():
            pass
        self.assertEqual(model.get_solver().get_solution_count(), 59049)

    def testRegular2(self):
        model = create_model()
        n = 12
        intvars = model.intvars(n, 0, 2)
        # different rules are formulated as patterns that must NOT be matched by x
        forbidden_regexps = [
            # do not end with '00' if start with '11'
            "11(0|1|2)*00",
            # at most three consecutive 0
            "(0|1|2)*0000(0|1|2)*",
            # no pattern '112' at position 5
            "(0|1|2){4}112(0|1|2)*",
            # pattern '12' after a 0 or a sequence of 0
            "(0|1|2)*02(0|1|2)*",
            "(0|1|2)*01(0|1)(0|1|2)*",
            # at most three 2 on consecutive even positions
            "(0|1|2)((0|1|2)(0|1|2))*2(0|1|2)2(0|1|2)2(0|1|2)*"
        ]
        # a unique automaton is built as the complement language composed of all the forbidden patterns
        auto = create_finite_automaton()
        for reg in forbidden_regexps:
            a = create_finite_automaton(reg)
            auto = auto.union(a)
            auto.minimize()
        auto = auto.complement()
        auto.minimize()
        self.assertEqual(auto.nb_states, 54)
        model.regular(intvars, auto).post()
        model.get_solver().set_input_order_lb_search(*intvars)
        while model.get_solver().solve():
            pass
        self.assertEqual(model.get_solver().get_solution_count(), 25980)
