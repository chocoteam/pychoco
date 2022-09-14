import unittest

from pychoco import create_model
from pychoco.objects.graphs.multivalued_decision_diagram import MultivaluedDecisionDiagram


class TestMDD(unittest.TestCase):

    def test_mdd_1(self):
        model = create_model("MyModel")
        v = model.intvars(4, 0, 10)
        tuples = [[0, 1, 1, 1], [1, 1, 1, 2]]
        mdd = MultivaluedDecisionDiagram(v, tuples)
