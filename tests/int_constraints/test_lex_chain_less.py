import unittest

from pychoco.model import Model


class TestLexChainLess(unittest.TestCase):

    def testLexChainLess1(self):
        m = Model()
        ar1 = m.intvars(3, 0, 5)
        ar2 = m.intvars(3, -1, 4)
        c = m.lex_chain_less([ar1, ar2])
        c.post()
        while m.get_solver().solve():
            self.assertTrue(c.is_satisfied())

    def testLexChainLess2(self):
        m = Model()
        ar1 = m.intvars(3, 0, 5)
        ar2 = m.intvars(3, -1, 4)
        c = m.lex_chain_less(ar1, ar2)
        c.post()
        while m.get_solver().solve():
            self.assertTrue(c.is_satisfied())
