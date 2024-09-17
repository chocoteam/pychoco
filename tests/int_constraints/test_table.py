import unittest

from pychoco.model import Model


class TestTable(unittest.TestCase):

    def testTable1(self):
        m = Model()
        intvars = m.intvars(3, 1, 2)
        tuples = [
            [0, 0, 0],
            [1, 1, 1],
            [2, 2, 2],
            [3, 3, 3]
        ]
        table_constraint = m.table(intvars, tuples, False)
        table_constraint.post()
        m.get_solver().solve()
        self.assertEqual(m.get_solver().get_solution_count(), 1)

    def testTable2(self):
        m = Model()
        x = m.intvar(0, 4)
        y = m.boolvar()
        z = m.boolvar()
        tuples = [
            [0, -1, 1],
            [0, 0, 1],
            [5, -1, 1],
            [1, 0, 1]
        ]
        m.table([x, y, z], tuples, algo="CT+").post()
        m.get_solver().find_all_solutions()
        self.assertEqual(m.get_solver().get_solution_count(), 2)

    def testTable3(self):
        m = Model()
        x = m.intvar(0, 3)
        y = m.boolvar()
        tuples = [
            [-1, 1],
        ]
        m.table([x, y], tuples, algo="CT+", universal_value=-1).post()
        m.get_solver().find_all_solutions()
        self.assertEqual(m.get_solver().get_solution_count(), 4)