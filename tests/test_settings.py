import unittest

from pychoco.settings import Settings


class TestSettings(unittest.TestCase):

    def test_create_settings(self):
        settings = Settings()
        self.assertIsNotNone(settings)

