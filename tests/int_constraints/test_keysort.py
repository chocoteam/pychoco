import unittest

from pychoco import create_model


class TestKeysort(unittest.TestCase):

    def testKeysort1(self):
        model = create_model()
        x = [
            [model.intvar(2), model.intvar(3), model.intvar(1001)],
            [model.intvar(2), model.intvar(4), model.intvar(1002)],
            [model.intvar(1), model.intvar(5), model.intvar(1003)],
            [model.intvar(2), model.intvar(3), model.intvar(1004)]
        ]
        y = [
            [model.intvar(0, 3), model.intvar(2, 6), model.intvar(1000, 10006)],
            [model.intvar(0, 3), model.intvar(2, 6), model.intvar(1000, 10006)],
            [model.intvar(0, 3), model.intvar(2, 6), model.intvar(1000, 10006)],
            [model.intvar(0, 3), model.intvar(2, 6), model.intvar(1000, 10006)]
        ]
        model.keysort(x, None, y, 2).post()
        model.get_solver().solve()
        self.assertEquals(y[0][0].get_value(), 1)
        self.assertEquals(y[0][1].get_value(), 5)
        self.assertEquals(y[0][2].get_value(), 1003)
        self.assertEquals(y[1][0].get_value(), 2)
        self.assertEquals(y[1][1].get_value(), 3)
        self.assertEquals(y[1][2].get_value(), 1001)
        self.assertEquals(y[2][0].get_value(), 2)
        self.assertEquals(y[2][1].get_value(), 3)
        self.assertEquals(y[2][2].get_value(), 1004)
        self.assertEquals(y[3][0].get_value(), 2)
        self.assertEquals(y[3][1].get_value(), 4)
        self.assertEquals(y[3][2].get_value(), 1002)

    def testKeysort2(self):
        model = create_model()
        x = [
            [model.intvar(3, 3), model.intvar(1, 1)],
            [model.intvar(1, 4), model.intvar(2, 2)],
            [model.intvar(4, 4), model.intvar(3, 3)],
            [model.intvar(1, 4), model.intvar(4, 4)],
        ]
        y = [
            [model.intvar(1, 4), model.intvar(1, 4)],
            [model.intvar(1, 4), model.intvar(1, 4)],
            [model.intvar(1, 4), model.intvar(1, 4)],
            [model.intvar(1, 4), model.intvar(1, 4)],
        ]
        model.keysort(x, None, y, 2).post()
        while model.get_solver().solve():
            pass
        self.assertEquals(model.get_solver().get_solution_count(), 16)
