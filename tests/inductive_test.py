import unittest
import bring_order
from bring_order.inductive import Inductive
from unittest.mock import Mock, MagicMock
from bring_order.boutils import BOUtils
from bring_order.bogui import BOGui

class TestInductive(unittest.TestCase):
    def setUp(self):
        self.instance = Inductive()     
        self.instance.utils = Mock(wraps=BOUtils)   
        self.instance.bogui = Mock()

    def test_cell_count_starts_at_1(self):
        self.assertEqual(self.instance.cell_count, 1)

    def test_new_analysis_has_no_conclusion(self):
        self.assertIsNone(self.instance.conclusion)

    def test_open_cells_button_creates_button(self):
        self.instance.create_open_cells_button()
        self.instance.bogui.create_button.assert_called()

    def test_create_delete_button_creates_button(self):
        self.instance.create_delete_button()
        self.instance.bogui.create_button.assert_called()

    def test_create_run_button_creates_button(self):
        self.instance.create_run_button()
        self.instance.bogui.create_button.assert_called()

    def test_create_clear_button_creates_button(self):
        self.instance.create_clear_button()
        self.instance.bogui.create_button.assert_called()

        




    
