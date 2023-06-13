import unittest
import bring_order
from unittest.mock import Mock, ANY
from bring_order.bringorder import BringOrder
from bring_order.bogui import BOGui

class TestBringOrder(unittest.TestCase):
    def setUp(self):
        self.instance = BringOrder()
        self.instance.bogui = Mock()
        self.instance.boutils = Mock()

    def test_buttons_are_created(self):
        self.assertIsNotNone(self.instance.deductive_button)
        self.assertIsNotNone(self.instance.inductive_button)

    def test_deductive_analysis_starts(self):
        self.instance.start_deductive_analysis()
        self.instance.boutils.create_and_execute_code_cell.assert_called_with('Deductive(data_limitations="")')

    def test_inductive_analysis_starts(self):
        self.instance.start_inductive_analysis()
        self.instance.boutils.create_and_execute_code_cell.assert_called_with('Inductive()')                 

    def test_representation(self):
        printed = self.instance.__repr__()
        self.assertEqual(printed, '')
