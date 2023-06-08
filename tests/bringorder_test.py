import unittest
import src
from unittest.mock import Mock, ANY
from src.bringorder import BringOrder
from src.bogui import BOGui

class TestBringOrder(unittest.TestCase):
    def setUp(self):
        self.instance = BringOrder()
        self.instance.bogui = Mock()

    def test_buttons_are_created(self):
        self.assertIsNotNone(self.instance.deductive_button)
        self.assertIsNotNone(self.instance.inductive_button)

    def test_deductive_analysis_starts(self):
        self.instance.start_deductive_analysis()
        self.assertFalse(self.instance.inductive)

    def test_inductive_analysis_starts(self):
        self.instance.start_inductive_analysis()
        self.assertFalse(self.instance.deductive)                 

    def test_representation(self):
        printed = self.instance.__repr__()
        self.assertEqual(printed, "New Analysis")