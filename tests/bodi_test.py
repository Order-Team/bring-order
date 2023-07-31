import unittest
from ipywidgets import widgets
from unittest.mock import Mock, patch, MagicMock
from bring_order.boutils import BOUtils
from bring_order.bogui import BOGui
from bring_order.bodi import Bodi

class TestBodi(unittest.TestCase):

    def setUp(self):
        next_step = [None]

        self.instance = Bodi(BOUtils(), BOGui(), next_step=next_step)
        self.instance.boutils = Mock()
        self.instance.bogui = Mock()
        self.instance.limitations = Mock()
        self.instance.bogui.create_error_message = lambda value: widgets.HTML(value=value)
        self.instance.bogui.create_message = lambda value: widgets.HTML(value=value)
        self.instance.bogui.create_label = lambda value: widgets.Label(value=value)
        self.instance.limitations.empty_limitations_error = self.instance.bogui.create_error_message('')

    def test_correct_amount_of_buttons_is_created(self):
        self.assertEqual(len(self.instance.buttons), 10)

    def test_bodi_hides_current_input(self):
        self.instance.bodi()
        self.instance.boutils.hide_current_input.assert_called()

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
        self.instance.start_analysis_clicked()
        self.instance.limitations.call_check_limitation.assert_called()

    def test_format_data_description_returns_correct_string(self):
        self.instance.title.value = 'My title'
        self.instance.data_name.value = 'My data'
        self.instance.data_description.value = 'List of integers.'
        text = self.instance.format_data_description()
        correct = '# My title\\n ## Data: My data\\n ### Description\\nList of integers.'
        self.assertEqual(text, correct)

    def test_format_data_description_returns_correct_string_with_new_line(self):
        self.instance.title.value = 'My title'
        self.instance.data_name.value = 'My data'
        self.instance.data_description.value = 'List of integers.\nAscending order.'
        text = self.instance.format_data_description()
        correct = '# My title\\n ## Data: My data\\n ### Description\\nList of integers.<br />Ascending order.'
        self.assertEqual(text, correct)

    def test_run_cells_runs_the_correct_amount_of_cells(self):
        self.instance.bogui.create_input_field = lambda dv, ph : widgets.Text(f'{dv}{ph}')
        self.instance.bogui.create_message = lambda value : widgets.HTML(value)
        self.instance.cell_count = 3
        self.instance.run_cells()
        self.instance.boutils.run_cells_above.assert_called_with(3)

    def test_start_analysis_clicked_creates_markdown_cell(self):
        self.instance.limitations.format_limitations = MagicMock()
        text = self.instance.limitations.format_limitations.return_value = '### Limitations\\n- Limitation0\\n- Limitation1\\n'        
        self.instance.limitations.call_check_limitation = MagicMock()
        self.instance.limitations.call_check_limitation.return_value = True
        self.instance.start_analysis_clicked()
        self.instance.boutils.create_markdown_cells_above.assert_called_with(1, text=text)

    def test_start_analysis_clicked_sets_error_message_if_limitations_are_empty(self):
        self.instance.limitations.call_check_limitation = MagicMock()
        self.instance.limitations.call_check_limitation.return_value = False
        self.instance.start_analysis_clicked()
        self.instance.limitations.set_error_value.assert_called_with('Data limitations cannot be empty')
        self.instance.boutils.create_markdown_cells_above.assert_not_called()

    def test_start_data_import_sets_error_message_if_data_name_empty(self):
        self.instance.bodi = Mock()
        self.instance.start_data_import()
        self.instance.bodi.assert_called_with(error='Please give your study a title')
        self.instance.boutils.create_markdown_cells_above.assert_not_called()

    def test_start_data_import_sets_error_message_if_description_empty(self):
        self.instance.bodi = Mock()
        self.instance.title.value = "My title"
        self.instance.data_name.value = 'My data'
        self.instance.start_data_import()
        self.instance.bodi.assert_called_with(error='You must give some description of the data')
        self.instance.boutils.create_markdown_cells_above.assert_not_called()

    def test_start_data_import_creates_markdown_cell(self):
        self.instance.title.value = 'My title'
        self.instance.data_name.value = 'My data'
        self.instance.data_description.value = 'The sample size is 100.'
        self.instance.start_data_import()
        text = '# My title\\n ## Data: My data\\n ### Description\\nThe sample size is 100.'
        self.instance.boutils.create_markdown_cells_above.assert_called_with(1, text=text)

    def test_open_cells_does_not_open_negative_amount_of_cells(self):
        self.instance.add_cells_int.value = -1
        self.instance.open_cells()
        self.assertEqual(self.instance.cell_count, 0)
        self.instance.boutils.create_code_cells_above.assert_not_called()
   







        



