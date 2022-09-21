import unittest

from pychoco.model import Model


class TestSort(unittest.TestCase):

    def testSort1(self):
        m = Model()
        iv1 = m.intvars(6, 0, 3)
        iv2 = m.intvars(6, 0, 3)
        sort = m.sort(iv1, iv2)
        sort.post()
        while m.get_solver().solve():
            self.assertTrue(sort.is_satisfied())
        self.assertTrue(m.get_solver().get_solution_count() > 0)
