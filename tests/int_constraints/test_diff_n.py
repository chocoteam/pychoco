import unittest

from pychoco import create_model


class TestDiffN(unittest.TestCase):

    def testDiffN1(self):
        m = create_model()
        x = m.intvars(2, 0, 3)
        y = m.intvars(2, 0, 3)
        width = m.intvars(2, 0, 3)
        height = m.intvars(2, 0, 3)
        diff_n = m.diff_n(x, y, width, height)
        diff_n.post()
        while m.get_solver().solve():
            self.assertTrue(diff_n.is_satisfied())
