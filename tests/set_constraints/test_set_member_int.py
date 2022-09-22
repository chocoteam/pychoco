import unittest

from pychoco.model import Model


class TestSetMemberInt(unittest.TestCase):

    def test1(self):
        m = Model()
        intvar = m.intvar(0, 100)
        setvar = m.setvar([], [1, 10, 20, 50, 77, 92])
        m.set_member_int(intvar, setvar).post()
        while m.get_solver().solve():
            self.assertTrue(intvar.get_value() in setvar.get_value())
