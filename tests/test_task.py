import unittest

from pychoco.model import Model


class TestTask(unittest.TestCase):

    def test_create_task_iv_iv_iv(self):
        model = Model("MyModel")
        s = model.intvar(0, 10)
        d = model.intvar(0, 10)
        e = model.intvar(0, 20)
        t = model.task(s, d, e)
        self.assertEqual(t.start.get_ub(), 10)
        self.assertEqual(t.end.get_lb(), 0)
        self.assertEqual(t.duration.get_lb(), 0)
        t.ensure_bound_consistency()

    def test_create_task_iv_i(self):
        model = Model("MyModel")
        s = model.intvar(0, 10)
        d = 10
        t = model.task(s, d)
        self.assertEqual(t.start.get_ub(), 10)
        self.assertEqual(t.end.get_ub(), 20)
        self.assertEqual(t.duration.get_lb(), 10)
        t.ensure_bound_consistency()

    def test_create_task_iv_iv(self):
        model = Model("MyModel")
        s = model.intvar(0, 10)
        d = model.intvar(0, 10)
        t = model.task(s, d)
        self.assertEqual(t.start.get_ub(), 10)
        self.assertEqual(t.end.get_ub(), 20)
        self.assertEqual(t.duration.get_lb(), 0)
        t.ensure_bound_consistency()

    def test_create_task_iv_i_iv(self):
        model = Model("MyModel")
        s = model.intvar(0, 10)
        d = 10
        e = model.intvar(0, 20)
        t = model.task(s, d, e)
        t.ensure_bound_consistency()
        self.assertEqual(t.start.get_ub(), 10)
        self.assertEqual(t.end.get_lb(), 10)
        self.assertEqual(t.duration.get_lb(), 10)
