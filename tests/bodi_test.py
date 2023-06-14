import unittest
import bring_order
from unittest.mock import Mock, patch, MagicMock
from bring_order.boutils import BOUtils
from bring_order.bogui import BOGui
from bring_order.bodi import Bodi
from IPython import display

class TestBodi(unittest.TestCase):

    def setUp(self):
        def start_analysis():
            pass

        self.instance = Bodi(BOUtils(), BOGui(), start_analysis=start_analysis)
        self.instance.boutils = Mock()
        self.instance.bogui = Mock()

    def test_start_data_hides_current_input(self):
        self.instance.start_data_import()
        self.instance.boutils.hide_current_input.assert_called()

    def test_check_limitations_returns_false_when_empty(self):
        self.assertFalse(self.instance.check_limitations())

    def test_check_limitations_returns_true_when_not_empty(self):
        self.instance.data_limitations.value = "Some limitations"
        self.assertTrue(self.instance.check_limitations())