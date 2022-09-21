import unittest

from pychoco.model import Model


class TestModel(unittest.TestCase):

    def test_create_model(self):
        model = Model("MyModel")
        self.assertEqual(model.name, "MyModel")
