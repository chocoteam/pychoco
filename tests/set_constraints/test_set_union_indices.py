import unittest

from pychoco.model import Model


class TestSetUnion(unittest.TestCase):

    def test1(self):
        m = Model()
        a = m.setvar([], range(0, 5))
        b = m.setvar([], range(5, 10))
        c = m.setvar([], range(5, 7))
        setvars = [a, b, c]
        d = m.setvar([], range(0, 10))
        indices = m.setvar([], range(0, 2))
        m.set_union_indices(setvars, indices, d).post()
        while m.get_solver().solve():
            value = set()
            for i in indices.get_value():
                value = value.union(setvars[i].get_value())
            self.assertSetEqual(value, d.get_value())
