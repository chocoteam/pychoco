import math
import unittest

from pychoco import create_model


class TestSquare(unittest.TestCase):

    def testSquare1(self):
        m = create_model()
        x2 = m.intvar(0, 100)
        x = m.intvar(0, 10)
        m.square(x2, x).post()
        sols = m.get_solver().find_all_solutions()
        for s in sols:
            self.assertEqual(math.pow(s.get_int_val(x), 2), s.get_int_val(x2))
