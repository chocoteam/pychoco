import unittest

from pychoco import create_model


class TestBoolsIntChanneling(unittest.TestCase):

    def testBoolsIntChanneling1(self):
        m = create_model()
        bools = m.boolvars(10)
        intvar = m.intvar(0, 9)
        m.bools_int_channeling(bools, intvar).post()
        while m.get_solver().solve():
            for b in range(0, 10):
                if b == intvar.get_value():
                    self.assertTrue(bools[b].get_value())
                else:
                    self.assertFalse(bools[b].get_value())
            self.assertTrue(m.get_solver().get_solution_count(), 10)

    def testBoolsIntChannelingFail(self):
        m = create_model()
        bools = m.boolvars(10)
        intvar = m.intvar(10, 11)
        m.or_(*bools).post()
        m.bools_int_channeling(bools, intvar).post()
        self.assertFalse(m.get_solver().solve())
