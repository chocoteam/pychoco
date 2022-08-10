import unittest

from pychoco import create_model


class TestBitsIntChanneling(unittest.TestCase):

    def testBitsIntChanneling1(self):
        model = create_model()
        bits = [
            model.boolvar(False),
            model.boolvar(True),
            model.boolvar(False),
            model.boolvar(True),
            model.boolvar(False)
        ]
        intvar = model.intvar(0, 100)
        model.bits_int_channeling(bits, intvar).post()
        self.assertTrue(model.get_solver().solve())
        self.assertEqual(intvar.get_value(), 10)
        self.assertFalse(model.get_solver().solve())

    def testBitsIntChanneling2(self):
        model = create_model()
        bits = []
        intvar = model.intvar(0, 100)
        model.bits_int_channeling(bits, intvar).post()
        self.assertTrue(model.get_solver().solve())
        self.assertEqual(intvar.get_value(), 0)
        self.assertFalse(model.get_solver().solve())

    def testBitsIntChanneling3(self):
        model = create_model()
        bits = model.boolvars(7)
        intvar = model.intvar(10)
        model.bits_int_channeling(bits, intvar).post()
        self._check_solutions(model, bits, intvar)

    def testBitsIntChanneling4(self):
        model = create_model()
        bits = model.boolvars(10)
        var = model.intvar(0, 1000)
        model.bits_int_channeling(bits, var).post()
        self._check_solutions(model, bits, var)

    def testBitsIntChannelingFail(self):
        model = create_model()
        bits = model.boolvars(7)
        intvar = model.intvar(128, 500)
        model.bits_int_channeling(bits, intvar).post()
        self.assertFalse(model.get_solver().solve())

    def _check_solutions(self, model, bits, var):
        nb_sol = 0
        while model.get_solver().solve():
            nb_sol += 1
            exp = 1
            number = 0
            for bit in bits:
                number += bit.get_value() * exp
                exp *= 2
            self.assertEqual(number, var.get_value())
        self.assertTrue(nb_sol > 0)
