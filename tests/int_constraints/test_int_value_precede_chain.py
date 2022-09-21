import unittest

from pychoco.model import Model


class TestIntValuePrecedeChain(unittest.TestCase):

    def testIntValuePrecedeChain1(self):
        for i in range(0, 10):
            model = Model()
            intvars = model.intvars(5, 0, 5)
            model.int_value_precede_chain(intvars, [1, 2]).post()
            model.get_solver().set_random_search(*intvars)
            while model.get_solver().solve():
                pass
            s1 = model.get_solver().get_solution_count()
            model = Model()
            intvars = model.intvars(5, 0, 5)
            model.int_value_precede_chain(intvars, [1, 2]).post()
            model.get_solver().set_random_search(*intvars)
            while model.get_solver().solve():
                pass
            s2 = model.get_solver().get_solution_count()
            self.assertEqual(s1, s2)
