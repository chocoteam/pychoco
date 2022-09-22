import unittest

from pychoco.model import Model


class TestSetElement(unittest.TestCase):

    def test1(self):
        m = Model()
        setvars = [m.setvar(set([]), set(range(0, 5))) for i in range(0, 3)]
        s = m.setvar(set(range(0, 5)))
        i = m.intvar(0, 3)
        m.set_all_different(setvars).post()
        m.set_element(i, setvars, s).post()
        while m.get_solver().solve():
            set_value = setvars[i.get_value()].get_value()
            self.assertSetEqual(set_value, s.get_value())
