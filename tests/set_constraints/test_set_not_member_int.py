import unittest

from pychoco.model import Model


class TestSetNotMemberInt(unittest.TestCase):

    def test1(self):
        m = Model()
        intvar = m.intvar(0, 100)
        setvar = m.setvar([], [1, 10, 20, 50, 77, 92])
        m.set_not_member_int(intvar, setvar).post()
        while m.get_solver().solve():
            self.assertTrue(intvar.get_value() not in setvar.get_value())
