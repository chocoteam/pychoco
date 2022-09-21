import unittest

from pychoco.model import Model


class TestBinPacking(unittest.TestCase):

    def testBinPacking1(self):
        model = Model();
        item_size = [2, 3, 1];
        item_bin = model.intvars(3, -1, 1);
        bin_load = model.intvars(2, 3, 3);
        model.bin_packing(item_bin, item_size, bin_load).post()
        self.assertTrue(model.get_solver().solve())

    def testBinPacking2(self):
        model = Model()
        item_size = [2, 2, 2]
        item_bin = model.intvars(3, 0, 2)
        bin_load = model.intvars(3, 0, 5)
        model.arithm(item_bin[0], "!=", 0).post()
        model.bin_packing(item_bin, item_size, bin_load, 0).post()
        model.get_solver().find_all_solutions()
        self.assertEqual(model.get_solver().get_solution_count(), 16)
