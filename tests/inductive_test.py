import unittest
import bring_order
from bring_order.inductive import Inductive
from unittest.mock import Mock, MagicMock
from bring_order.boutils import BOUtils
from bring_order.bogui import BOGui

class TestInductive(unittest.TestCase):
    def setUp(self):
        self.instance = Inductive(BOGui(), BOUtils())
        self.instance.bogui.create_button = Mock()

    def test_cell_count_starts_at_0(self):
        self.assertEqual(self.instance.cell_count, 0)

    def test_new_analysis_has_no_conclusion(self):
        self.assertIsNone(self.instance.conclusion)

    def test_that_empty_summary_returns_false(self):
        self.assertFalse(self.instance.check_notes())

    def test_open_cells_button_is_created(self):
        self.assertEqual(self.instance.buttons['Open cells'].description, 'Open cells')

    def test_correct_amount_of_buttons_is_created(self):
        self.assertEqual(len(self.instance.buttons), 8)

    def test_filled_summary_returns_true(self):
        self.instance.notes.value = "Childrens' usage of psychosis medication has increased."
        self.assertTrue(self.instance.check_notes())   

    def test_execute_ready_requires_notes(self):
        self.instance.check_notes = MagicMock()
        self.instance.check_notes.return_value = False
        self.instance.execute_ready()
        self.assertEqual(self.instance.empty_notes_error.value, 'Observation field can not be empty')

    def test_cell_count_cannot_be_less_than_zero(self):
        self.instance.delete_last_cell()
        self.assertEqual(0, self.instance.cell_count)

    def test_delete_last_cell_decreases_cell_count(self):
        self.instance.cell_count = 5
        self.instance.delete_last_cell()
        self.assertEqual(4, self.instance.cell_count)

    def test_open_cells_increases_cell_count_correctly(self):
        self.instance.cell_count = 3
        self.instance.add_cells_int.value = 3
        self.instance.open_cells()  
        self.assertEqual(7, self.instance.cell_count)  

    # def test_open_cells_button_creates_button(self):
    #     self.instance.create_open_cells_button()
    #     self.instance.bogui.create_button.assert_called()
    #
    # def test_create_delete_button_creates_button(self):
    #     self.instance.create_delete_button()
    #     self.instance.bogui.create_button.assert_called()
    #
    # def test_create_run_button_creates_button(self):
    #     self.instance.create_run_button()
    #     self.instance.bogui.create_button.assert_called()
    #
    # def test_create_clear_button_creates_button(self):
    #     self.instance.create_clear_button()
    #     self.instance.bogui.create_button.assert_called()
