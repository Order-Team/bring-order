import unittest
import bring_order
from unittest.mock import Mock, patch, MagicMock
from bring_order.boutils import BOUtils

class TestBOUtils(unittest.TestCase):
    def setUp(self):
        self.instance = BOUtils()

    def test_clear_cells_creates_new_cells(self):
        BOUtils.create_code_cells = MagicMock()
        self.instance.clear_code_cells_below(5)
        self.instance.create_code_cells.assert_called()

