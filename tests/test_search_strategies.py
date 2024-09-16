import math
import unittest

from pychoco.model import Model


class TestSearchStrategies(unittest.TestCase):

    def setUp(self):
        self.model = Model()
        self.vars = self.model.intvars(5, 0, 10)
        self.model.all_different(self.vars).post()
        self.obj = self.model.intvar(0, 5 * 10)
        self.model.sum(self.vars, "=", self.obj).post()

    def test_default_search(self):
        self.model.get_solver().set_default_search()
        self.model.get_solver().find_optimal_solution(objective=self.obj, maximize=True)

    def test_dom_over_w_deg_search(self):
        self.model.get_solver().set_dom_over_w_deg_search(self.vars)
        self.model.get_solver().find_optimal_solution(objective=self.obj, maximize=True)

    def test_dom_over_w_deg_ref_search(self):
        self.model.get_solver().set_dom_over_w_deg_ref_search(*self.vars)
        self.model.get_solver().find_optimal_solution(objective=self.obj, maximize=True)

    def test_dom_over_w_deg_ref_search(self):
        self.model.get_solver().set_dom_over_w_deg_ref_search(*self.vars)
        self.model.get_solver().find_optimal_solution(objective=self.obj, maximize=True)

    def test_activity_based_search(self):
        self.model.get_solver().show_restarts()
        self.model.get_solver().set_activity_based_search(*self.vars)
        self.model.get_solver().find_optimal_solution(objective=self.obj, maximize=True)

    def test_min_dom_lb_search(self):
        self.model.get_solver().set_min_dom_lb_search(*self.vars)
        self.model.get_solver().find_optimal_solution(objective=self.obj, maximize=True)

    def test_min_dom_ub_search(self):
        self.model.get_solver().set_min_dom_ub_search(*self.vars)
        self.model.get_solver().find_optimal_solution(objective=self.obj, maximize=True)

    def test_random_search(self):
        self.model.get_solver().set_random_search(*self.vars)
        self.model.get_solver().find_optimal_solution(objective=self.obj, maximize=True)

    def test_conflict_history_search(self):
        self.model.get_solver().set_conflict_history_search(*self.vars)
        self.model.get_solver().find_optimal_solution(objective=self.obj, maximize=True)

    def test_input_order_lb_search(self):
        self.model.get_solver().set_input_order_lb_search(*self.vars)
        self.model.get_solver().find_optimal_solution(objective=self.obj, maximize=True)

    def test_input_order_ub_search(self):
        self.model.get_solver().set_input_order_ub_search(*self.vars)
        self.model.get_solver().find_optimal_solution(objective=self.obj, maximize=True)

    def test_failure_length_based_search(self):
        self.model.get_solver().set_failure_length_based_search(*self.vars)
        self.model.get_solver().find_optimal_solution(objective=self.obj, maximize=True)

    def test_failure_rate_based_search(self):
        self.model.get_solver().set_failure_rate_based_search(*self.vars)
        self.model.get_solver().find_optimal_solution(objective=self.obj, maximize=True)

    def test_pick_on_dom_search(self):
        self.model.get_solver().set_pick_on_dom_search(*self.vars)
        self.model.get_solver().find_optimal_solution(objective=self.obj, maximize=True)

    def test_pick_on_fil_search(self):
        self.model.get_solver().set_pick_on_fil_search(*self.vars)
        self.model.get_solver().find_optimal_solution(objective=self.obj, maximize=True)