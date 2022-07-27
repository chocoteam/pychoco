import unittest

from pychoco import create_model


class TestIntVar(unittest.TestCase):

    def test_create_intvar(self):
        model = create_model("MyModel")
        a = model.intvar(0, 10, "a")
        b = model.intvar(1, 2)
        self.assertEqual(a.get_name(), "a")
        self.assertEqual(a.get_lb(), 0)
        self.assertEqual(a.get_ub(), 10)
        self.assertEqual(b.get_lb(), 1)
        self.assertEqual(b.get_ub(), 2)
