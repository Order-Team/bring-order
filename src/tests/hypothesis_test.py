
import unittest
from hypothesis import Hypothesis


class TestHypothesis(unittest.TestCase):   
    def setUp(self):
        print("Set up")

    def test_setup(self):
        instance = Hypothesis()
        instance.set_hypothesis()
        self.assertEqual("Hello world", "Hello world")


