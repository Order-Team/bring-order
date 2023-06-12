import unittest
import bring_order
from unittest.mock import Mock, patch, MagicMock
from bring_order.boutils import BOUtils
from IPython import display

class TestBOUtils(unittest.TestCase):

    def setUp(self):
        self.instance = BOUtils()        

    def test_clear_cells_creates_new_cells(self):
        BOUtils.create_code_cells_at_bottom = Mock()
        self.instance.clear_code_cells_below(5)
        self.instance.create_code_cells_at_bottom.assert_called()

    def test_clear_code_and_observation_cells_creates_correct_amount_of_cells(self):
        BOUtils.create_code_and_observation_cells = Mock()
        self.instance.clear_code_and_observation_cells(6)
        self.instance.create_code_and_observation_cells.assert_called_with(3)

