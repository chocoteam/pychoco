import unittest

from pychoco.model import Model


class TestIfThen(unittest.TestCase):

    def testIfThen1(self):
        m = Model()

        x = m.intvar(0,10)
        y = m.intvar(0,100)

        m.if_then(m.arithm(x, "<", 10),
                  m.arithm(y,">", 42))

        m.arithm(x,"=",3).post()
        m.get_solver().solve()

        self.assertGreater(y.get_value(), 42)

