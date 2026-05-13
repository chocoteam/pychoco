import unittest

from pychoco.model import Model


class TestModel(unittest.TestCase):

    def test_create_model(self):
        model = Model("MyModel")
        self.assertEqual(model.name, "MyModel")

    def test_create_model_without_name(self):
        model = Model()
        self.assertEqual(model.name, "Model " + str(id(model)))

    def test_model_with_settings(self):
        model = Model(lcg=True)
        xs = model.intvars(5, 0, 4, "x")
        model.all_different(xs).post()
        print(model)