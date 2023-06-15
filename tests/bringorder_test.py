import unittest
import bring_order
from unittest.mock import Mock, ANY
from bring_order.bringorder import BringOrder
from bring_order.bogui import BOGui
from bring_order.deductive import Deductive
from bring_order.inductive import Inductive

class TestBringOrder(unittest.TestCase):
    def setUp(self):
        self.instance = BringOrder()
        self.instance.bogui = Mock()
        self.instance.boutils = Mock()

    def test_deductive_button_is_created(self):
        self.instance.create_deductive_button()
        self.instance.bogui.create_button.assert_called()

    def test_inductive_button_is_created(self):
        self.instance.create_inductive_button()
        self.instance.bogui.create_button.assert_called()
         
    def test_representation(self):
        printed = self.instance.__repr__()
        self.assertEqual(printed, '')
