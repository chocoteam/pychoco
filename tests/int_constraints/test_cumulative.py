import unittest

from pychoco.model import Model


class TestCumulative(unittest.TestCase):

    def testCumulative1(self):
        m = Model()
        t1 = m.task(m.intvar(9), m.intvar(6), m.intvar(15))
        t2 = m.task(m.intvar(8), m.intvar(0, 6), m.intvar(8, 14))
        m.cumulative([t1, t2], [m.intvar(1), m.intvar(1)], m.intvar(1)).post()
        m.get_solver().solve()
        self.assertEqual(t2.duration.get_value(), 0)
