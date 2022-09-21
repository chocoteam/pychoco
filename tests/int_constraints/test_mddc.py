import unittest

from pychoco.model import Model
from pychoco.objects.graphs.multivalued_decision_diagram import MultivaluedDecisionDiagram


class TestMddc(unittest.TestCase):

    def testMddc1(self):
        m = Model()
        intvars = m.intvars(3, 0, 1)
        tuples = [[0, 0, 0], [1, 1, 1]]
        m.mddc(intvars, MultivaluedDecisionDiagram(intvars, tuples)).post()
        while m.get_solver().solve():
            pass
        self.assertEqual(m.get_solver().get_solution_count(), 2)

    def testMddc2(self):
        model = Model()
        intvars = model.intvars(3, 0, 2)
        tuples = [[0, 1, 2], [2, 1, 0]]
        model.mddc(intvars, MultivaluedDecisionDiagram(intvars, tuples)).post();
        while model.get_solver().solve():
            pass
        self.assertEqual(model.get_solver().get_solution_count(), 2)
