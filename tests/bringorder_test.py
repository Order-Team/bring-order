import unittest
import bring_order
from unittest.mock import Mock, MagicMock,ANY
from bring_order.bringorder import BringOrder
from bring_order.bogui import BOGui
from bring_order.deductive import Deductive
from bring_order.inductive import Inductive
from bring_order.bodi import Bodi

'''
class TestBringOrder(unittest.TestCase):
    def setUp(self):
        self.instance = BringOrder()
        self.instance.bogui = Mock()
        self.instance.boutils = Mock()
        self.instance.deductive = Mock()
        self.instance.inductive = Mock()
        self.instance.bodi = Mock()

    def test_deductive_button_is_created(self):
        self.instance.create_deductive_button()
        self.instance.bogui.create_button.assert_called()

    def test_inductive_button_is_created(self):
        self.instance.create_inductive_button()
        self.instance.bogui.create_button.assert_called()
         
    def test_representation(self):
        printed = self.instance.__repr__()
        self.assertEqual(printed, '')

    def test_deductive_start(self):
        self.instance.deductive.start_deductive_analysis = MagicMock()
        self.instance.deductive_button = Mock()
        self.instance.inductive_button = Mock()
        self.instance.start_deductive_analysis()
        self.instance.deductive.start_deductive_analysis.assert_called()

    def test_inductive_start(self):
        self.instance.inductive.start_inductive_analysis = MagicMock()
        self.instance.deductive_button = Mock()
        self.instance.inductive_button = Mock()
        self.instance.start_inductive_analysis()
        self.instance.inductive.start_inductive_analysis.assert_called()
'''    