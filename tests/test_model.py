import unittest

from pychoco import create_model


class TestModel(unittest.TestCase):

    def test_create_model(self):
        model = create_model("MyModel")
        self.assertEqual(model.get_name(), "MyModel")
