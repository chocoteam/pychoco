import unittest

from pychoco.model import Model


class TestSubCircuit(unittest.TestCase):

    def testSubCircuit1(self):
        model = Model()
        x = model.intvars(10, 0, 20)
        model.sub_circuit(x, 0, model.intvar(0, len(x) - 1)).post()
        model.get_solver().solve();
        self.assertEqual(1, model.get_solver().get_solution_count())

    def testSubCircuit2(self):
        model = Model()
        x = model.intvars(5, 0, 8)
        model.sub_circuit(x, 0, model.intvar(0, len(x) - 1)).post()
        model.get_solver().find_all_solutions();
        self.assertEqual(61, model.get_solver().get_solution_count())
