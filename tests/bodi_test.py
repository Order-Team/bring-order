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

    def test_correct_amount_of_buttons_is_created(self):
        self.assertEqual(len(self.instance.buttons), 6)

    def test_start_data_hides_current_input(self):
        self.instance.data_name.value = 'Some title'
        self.instance.data_description.value = 'Some description'
        self.instance.start_data_import()
        self.instance.boutils.hide_current_input.assert_called()

    def test_check_limitations_returns_false_when_empty(self):
        self.assertFalse(self.instance.check_limitations())

    def test_check_limitations_returns_true_when_not_empty(self):
        value = "Some limitations"
        self.assertTrue(self.instance.check_limitations(value))

    def test_open_cells_increases_cell_count_with_default_one(self):
        correct_cell_count = self.instance.cell_count + 1
        self.instance.open_cells()
        self.assertEqual(self.instance.cell_count, correct_cell_count)

    def test_open_cells_increases_cell_count_with_selected_value(self):
        self.instance.add_cells_int.value = 3
        correct_cell_count = self.instance.cell_count + 3
        self.instance.open_cells()
        self.assertEqual(self.instance.cell_count, correct_cell_count)

    def test_open_cells_creates_code_cell(self):
        self.instance.open_cells()
        self.instance.boutils.create_code_cells_above.assert_called_with(1)

    def test_open_cells_creates_selected_number_of_code_cells(self):
        self.instance.add_cells_int.value = 3
        self.instance.open_cells()
        self.instance.boutils.create_code_cells_above.assert_called_with(3)

    def test_delete_last_cell_does_not_delete_extra_cells(self):
        correct_cell_count = self.instance.cell_count
        self.instance.delete_last_cell()
        self.assertEqual(self.instance.cell_count, correct_cell_count)
        self.instance.boutils.delete_cell_above.assert_not_called()

    def test_delete_last_cell_decreases_cell_count(self):
        self.instance.cell_count = 3
        self.instance.delete_last_cell()
        self.assertEqual(self.instance.cell_count, 2)

    def test_delete_last_cell_removes_cell(self):
        self.instance.open_cells()
        self.instance.delete_last_cell()
        self.instance.boutils.delete_cell_above.asset_called()

    def test_start_analysis_clicked_checks_limitations(self):
        self.instance.call_check_limitation = Mock()
        self.instance.start_analysis_clicked()
        self.instance.call_check_limitation.assert_called()
