import unittest
import bring_order
from unittest.mock import Mock, patch, MagicMock
from bring_order.boutils import BOUtils
from bring_order.bodi import Bodi
from IPython import display

class TestBodi(unittest.TestCase):

    def setUp(self):
        self.instance = Bodi()
        self.instance.boutils = Mock()

    def test_add_code_cell_adds_two_cells(self):
        self.instance.add_code_cell()
        self.instance.boutils.create_code_cells_below.assert_called_with(2)

    def test_data_limits_creates_markdown_cell(self):
        self.instance.data_limits()    
        self.instance.boutils.create_markdown_cells_below.assert_called()