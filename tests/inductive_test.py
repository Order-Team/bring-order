import unittest
import src
from src.inductive import Inductive
from unittest.mock import Mock, ANY
from src.boutils import BOUtils
from src.bogui import BOGui

class TestInductive(unittest.TestCase):
    def setUp(self):
        self.instance = Inductive(0)     
        self.instance.utils = Mock(wraps=BOUtils)   
        self.instance.bogui = Mock()

    def test_cell_count_starts_at_1(self):
        self.assertEqual(self.instance.cell_count, 1)

    def test_new_analysis_has_no_conclusion(self):
        self.assertIsNone(self.instance.conclusion)

    def test_open_cells_creates_button(self):
        self.instance.create_open_cells_button()
        self.instance.bogui.create_button.assert_called()




    
