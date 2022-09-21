import unittest

from pychoco.model import Model


class TestSubPath(unittest.TestCase):

    def testSubPath1(self):
        model = Model()
        x = [
            model.intvar(4),
            model.intvar(1),
            model.intvar(0),
            model.intvar(2),
        ]
        start = model.intvar(-3, 10)
        end = model.intvar(-3, 10)
        size = model.intvar(-3, 10)
        model.sub_path(x, start, end, 0, size).post()
        model.get_solver().solve();
        self.assertEqual(1, model.get_solver().get_solution_count())
        self.assertEqual(3, size.get_value())
        self.assertEqual(3, start.get_value())
        self.assertEqual(0, end.get_value())

    def testSubPath2(self):
        model = Model()
        x = [
            model.intvar(4),
            model.intvar(-3, 6),
            model.intvar(0),
            model.intvar(2),
        ]
        start = model.intvar(-3, 10)
        end = model.intvar(-3, 10)
        size = model.intvar(3)
        model.sub_path(x, start, end, 0, size).post()
        model.get_solver().solve()
        self.assertEqual(1, model.get_solver().get_solution_count())
        self.assertEqual(3, size.get_value())
        self.assertEqual(3, start.get_value())
        self.assertEqual(1, x[1].get_value())
        self.assertEqual(0, end.get_value())
