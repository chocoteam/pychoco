import unittest

from pychoco import create_model


class TestIncreasing(unittest.TestCase):

    def testIncreasing1(self):
        m = create_model()
        intvars = m.intvars(10, 0, 10)
        m.increasing(intvars).post()
        for i in range(0, 10):
            m.get_solver().solve()
            sol = [v.get_value() for v in intvars]
            for j in range(0, 9):
                self.assertGreaterEqual(sol[j + 1], sol[j])

    def testIncreasing2(self):
        m = create_model()
        intvars = m.intvars(10, 0, 0)
        m.increasing(intvars).post()
        sols = m.get_solver().find_all_solutions()
        self.assertEquals(len(sols), 1)

