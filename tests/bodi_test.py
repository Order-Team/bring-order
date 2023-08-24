import unittest
import os
import pandas as pd
from ipywidgets import widgets
from ipyfilechooser import FileChooser
from unittest.mock import Mock, MagicMock
from bring_order.boutils import BOUtils
from bring_order.bogui import BOGui
from bring_order.bodi import Bodi
from bring_order.ai import Ai
from bring_order.boval import BOVal

class TestBodi(unittest.TestCase):


    def setUp(self):
        next_step = [None]
        dataset_variables = [[]]
        ai_disabled = [False]
        self.instance = Bodi(BOUtils(), BOGui(), BOVal(), dataset_variables, ai_disabled, next_step=next_step)
        self.instance.boutils = Mock()
        self.instance.bogui = Mock()
        self.instance.limitations = Mock()
        self.instance.stattests = Mock()
        self.instance.bogui.create_error_message = lambda value: widgets.HTML(value=value)
        self.instance.bogui.create_message = lambda value: widgets.HTML(value=value)
        self.instance.bogui.create_label = lambda value: widgets.Label(value=value)
        self.instance.limitations.empty_limitations_error = self.instance.bogui.create_error_message('')
        self.instance.limitations.get_limitations_for_print = lambda: widgets.HTML(value='')
        self.instance.stattests.check_numerical_data = lambda data: {}

    def test_correct_amount_of_buttons_is_created(self):
        self.assertEqual(len(self.instance.buttons), 15)

    def test_open_cells_increases_cell_count_with_default_one(self):
        correct_cell_count = self.instance.cell_count + 1
        self.instance._open_cells()
        self.assertEqual(self.instance.cell_count, correct_cell_count)

    def test_open_cells_increases_cell_count_with_selected_value(self):
        self.instance.fields[3].value = 3
        correct_cell_count = self.instance.cell_count + 3
        self.instance._open_cells()
        self.assertEqual(self.instance.cell_count, correct_cell_count)

    def test_open_cells_creates_code_cell(self):
        self.instance._open_cells()
        self.instance.boutils.create_code_cells_above.assert_called_with(1)

    def test_open_cells_creates_selected_number_of_code_cells(self):
        self.instance.fields[3].value = 3
        self.instance._open_cells()
        self.instance.boutils.create_code_cells_above.assert_called_with(3)

    def test_delete_last_cell_does_not_delete_extra_cells(self):
        correct_cell_count = self.instance.cell_count
        self.instance._delete_last_cell()
        self.assertEqual(self.instance.cell_count, correct_cell_count)
        self.instance.boutils.delete_cell_above.assert_not_called()

    def test_delete_last_cell_decreases_cell_count(self):
        self.instance.cell_count = 3
        self.instance._delete_last_cell()
        self.assertEqual(self.instance.cell_count, 2)

    def test_delete_last_cell_removes_cell(self):
        self.instance._open_cells()
        self.instance._delete_last_cell()
        self.instance.boutils.delete_cell_above.asset_called()

    def test_start_analysis_clicked_checks_limitations(self):
        self.instance._start_analysis_clicked()
        self.instance.limitations.call_check_limitation.assert_called()

    def test_format_data_description_returns_correct_string(self):
        self.instance.fields[0].value = 'My title'
        self.instance.fields[1].value = 'My data'
        self.instance.fields[2].value = 'List of integers.'
        text = self.instance.format_data_description()
        correct = '# My title\\n ## Data: My data\\n ### Description\\nList of integers.'
        self.assertEqual(text, correct)

    def test_format_data_description_returns_correct_string_with_new_line(self):
        self.instance.fields[0].value = 'My title'
        self.instance.fields[1].value = 'My data'
        self.instance.fields[2].value = 'List of integers.\nAscending order.'
        text = self.instance.format_data_description()
        correct = '# My title\\n ## Data: My data\\n ### Description\\nList of integers.<br />Ascending order.'
        self.assertEqual(text, correct)

    def test_run_cells_runs_the_correct_amount_of_cells(self):
        self.instance.bogui.create_input_field = lambda dv, ph : widgets.Text(f'{dv}{ph}')
        self.instance.bogui.create_message = lambda value : widgets.HTML(value)
        self.instance.bogui.create_grid = lambda rows, cols, items : widgets.GridspecLayout(rows, cols)
        self.instance.cell_count = 3
        self.instance.checklist = None
        self.instance._run_cells()
        self.instance.boutils.run_cells_above.assert_called_with(3)

    def test_start_analysis_clicked_creates_markdown_cell(self):
        self.instance.limitations.format_limitations = MagicMock()
        text = self.instance.limitations.format_limitations.return_value = '### Limitations\\n- Limitation0\\n- Limitation1\\n'
        self.instance.limitations.call_check_limitation = MagicMock()
        self.instance.limitations.call_check_limitation.return_value = True
        self.instance._start_analysis_clicked()
        self.instance.boutils.create_markdown_cells_above.assert_called_with(1, text=text)

    def test_start_analysis_clicked_sets_error_message_if_limitations_are_empty(self):
        self.instance.limitations.call_check_limitation = MagicMock()
        self.instance.limitations.call_check_limitation.return_value = False
        self.instance._start_analysis_clicked()
        self.instance.limitations.set_error_value.assert_called_with('Data limitations cannot be empty or\
                 contain special symbols')
        self.instance.boutils.create_markdown_cells_above.assert_not_called()

    def test_start_data_import_sets_error_message_if_title_empty(self):
        self.instance.bodi = Mock()
        self.instance._start_data_import()
        self.instance.bodi.assert_called_with(error='The title cannot be empty or contain special symbols')
        self.instance.boutils.create_markdown_cells_above.assert_not_called()

    def test_start_data_import_sets_error_message_if_data_name_empty(self):
        self.instance.bodi = Mock()
        self.instance.fields[0].value = "My title"
        self.instance._start_data_import()
        self.instance.bodi.assert_called_with(error='The data set name cannot be empty or contain special symbols')
        self.instance.boutils.create_markdown_cells_above.assert_not_called()

    def test_start_data_import_sets_error_message_if_description_empty(self):
        self.instance.bodi = Mock()
        self.instance.fields[0].value = "My title"
        self.instance.fields[1].value = 'My data'
        self.instance._start_data_import()
        self.instance.bodi.assert_called_with(error='The data description cannot be empty or contain special characters')
        self.instance.boutils.create_markdown_cells_above.assert_not_called()

    def test_start_data_import_creates_markdown_cell(self):
        self.instance.fields[0].value = 'My title'
        self.instance.fields[1].value = 'My data'
        self.instance.fields[2].value = 'The sample size is 100.'
        self.instance._start_data_import()
        text = '# My title\\n ## Data: My data\\n ### Description\\nThe sample size is 100.'
        self.instance.boutils.create_markdown_cells_above.assert_called_with(1, text=text)

    def test_open_cells_does_not_open_negative_amount_of_cells(self):
        self.instance.fields[3].value = -1
        self.instance._open_cells()
        self.assertEqual(self.instance.cell_count, 0)
        self.instance.boutils.create_code_cells_above.assert_not_called()

    def test_add_limitation_adds_limitation(self):
        self.instance._display_limitations_view = MagicMock()
        self.instance._add_limitation()
        self.instance.limitations.add_limitation.assert_called()    

    def test_remove_limitation_adds_limitation(self):
        self.instance._display_limitations_view = MagicMock()
        self.instance._remove_limitation()
        self.instance.limitations.remove_limitations.assert_called()        

    '''
    def test_run_cells_checks_if_user_runs_tests(self):
        self.instance.bogui.create_message = lambda value : widgets.HTML(value)
        self.instance.bogui.create_grid = lambda rows, cols, items : widgets.GridspecLayout(rows, cols)
        self.instance.cell_count = 1
        self.instance.run_cells()
        self.instance.stattests.detect_tests.assert_called()
    '''
    '''
    def test_toggle_ai_updates_button(self):
        self.instance._toggle_ai()
        self.assertEqual(self.instance.buttons['assist'].description, 'Close AI assistant')
        self.assertEqual(self.instance.buttons['assist'].button_style, 'warning')
        self.instance._toggle_ai()
        self.assertEqual(self.instance.buttons['assist'].description, 'AI assistant')
        self.assertEqual(self.instance.buttons['assist'].button_style, 'success')
    '''

    def test_show_cell_operations_calls_data_preparation_grid(self):
        self.instance.data_preparation_grid = MagicMock()
        self.instance._show_cell_operations()
        self.instance.data_preparation_grid.assert_called()

    def test_start_data_import_prepares_file_chooser(self):
        self.instance.file_chooser = FileChooser()
        self.instance.file_chooser.register_callback = MagicMock()
        self.instance.fields[0].value = 'Title'
        self.instance.fields[1].value = 'Data set'
        self.instance.fields[2].value = 'Description of data'
        self.instance._start_data_import()
        self.instance.file_chooser.register_callback.assert_called()
        self.assertEqual(self.instance.file_chooser.title, 'Choose a data file:')
        
    def test_import_data_opens_and_executes_two_code_cells(self):
        self.instance.bogui.create_grid = lambda rows, cols, items: widgets.VBox(items)
        self.instance.file_chooser = Mock()
        self.instance.file_chooser.selected = os.getcwd() + '/tests/test_iris.csv'
        self.instance.load_cfg_file = MagicMock()
        self.instance._import_data()
        self.instance.boutils.create_code_cells_above.assert_called_with(2)
        self.assertEqual(self.instance.boutils.execute_cell_from_current.call_count, 2)

    def test_import_data_calls_check_variables(self):
        self.instance.bogui.create_grid = lambda rows, cols, items: widgets.VBox(items)
        self.instance.check_variables = MagicMock()
        self.instance.file_chooser = Mock()
        self.instance.file_chooser.selected = os.getcwd() + '/tests/test_iris.csv'
        self.instance.load_cfg_file = MagicMock()
        self.instance._import_data()
        self.instance.check_variables.assert_called()

    def test_check_variable_independence_creates_error_message_if_needed(self):
        self.instance.stattests.check_variable_independence = lambda: ('var1', 'var2', 'Error')
        self.instance.bogui.create_error_message = MagicMock()
        self.instance._check_variable_independence()
        self.instance.bogui.create_error_message.assert_called_with('Error')

    def test_check_variable_independence_adds_limitation_and_creates_message(self):
        self.instance.stattests.check_variable_independence = lambda: ('var1', 'var2', False)
        self.instance.limitations.data_limitations = [widgets.Text('')]
        self.instance.limitations.get_values = lambda: ['']
        self.instance.bogui.create_message = MagicMock()
        self.instance._check_variable_independence()
        self.assertEqual(
            self.instance.limitations.data_limitations[-1].value,
            'var1 and var2 are not independent'
        )
        self.instance.bogui.create_message.assert_called_with(
            'Result added to limitations: var1 and var2 are not independent')

    def test_check_variable_independence_adds_new_limitation_if_last_not_empty(self):
        self.instance.stattests.check_variable_independence = lambda: ('var1', 'var2', False)
        self.instance.limitations.data_limitations = [widgets.Text(value='Old limitation')]
        self.instance.limitations.get_values = lambda: ['Old limitation']
        self.instance.limitations.add_limitation = lambda: self.instance.limitations.data_limitations.append(widgets.Text())
        self.instance._check_variable_independence()
        self.assertEqual(
            self.instance.limitations.data_limitations[0].value,
            'Old limitation'
        )
        self.assertEqual(
            self.instance.limitations.data_limitations[1].value,
            'var1 and var2 are not independent'
        )

    def test_check_variable_independence_does_not_add_same_limitation_twice(self):
        self.instance.stattests.check_variable_independence = lambda: ('var1', 'var2', False)
        self.instance.limitations.data_limitations = [widgets.Text('var1 and var2 are not independent')]
        self.instance.limitations.get_values = lambda: ['var1 and var2 are not independent']
        self.instance._check_variable_independence()
        self.assertEqual(len(self.instance.limitations.data_limitations), 1)
        
    def test_check_variable_independence_does_not_add_limitation_and_creates_message(self):
        self.instance.stattests.check_variable_independence = lambda: ('var1', 'var2', True)
        self.instance.limitations.data_limitations = [widgets.Text('')]
        self.instance.limitations.get_values = lambda: ['']
        self.instance.bogui.create_message = MagicMock()
        self.instance._check_variable_independence()
        self.assertNotEqual(
            self.instance.limitations.data_limitations[-1].value,
            'var1 and var2 are independent'
        )
        self.instance.bogui.create_message.assert_called_with(
            'var1 and var2 are independent')
        
    def test_display_independence_test_disables_buttons(self):
        self.instance.bogui.create_grid = lambda rows, cols, items: widgets.VBox(items)
        self.instance.stattests.select_variables = lambda: widgets.AppLayout()
        for button in ['open', 'delete', 'run', 'assist', 'limitations']:
            self.instance.buttons[button].disabled = False
        self.instance._display_independence_test()
        self.assertTrue(self.instance.buttons['open'].disabled)
        self.assertTrue(self.instance.buttons['delete'].disabled)
        self.assertTrue(self.instance.buttons['run'].disabled)
        self.assertTrue(self.instance.buttons['assist'].disabled)
        self.assertTrue(self.instance.buttons['limitations'].disabled)
        self.assertTrue(self.instance.buttons['independence'].disabled)

    def test_display_independence_test_does_not_disable_other_buttons_if_test_cannot_be_performed(self):
        self.instance.stattests.select_variables = lambda: widgets.HTML(
            'There are not enough categorical variables to perform a chi-square test.')
        for button in ['open', 'delete', 'run', 'assist', 'limitations']:
            self.instance.buttons[button].disabled = False
        self.instance._display_independence_test()
        self.assertFalse(self.instance.buttons['open'].disabled)
        self.assertFalse(self.instance.buttons['delete'].disabled)
        self.assertFalse(self.instance.buttons['run'].disabled)
        self.assertFalse(self.instance.buttons['assist'].disabled)
        self.assertFalse(self.instance.buttons['limitations'].disabled)
        self.assertTrue(self.instance.buttons['independence'].disabled)

    def test_close_independence_test_activates_buttons(self):
        self.instance.bogui.create_grid = lambda rows, cols, items: widgets.VBox(items)
        for button in ['open', 'delete', 'run', 'independence', 'assist', 'limitations']:
            self.instance.buttons[button].disabled = True
        self.instance._close_independence_test()
        self.assertFalse(self.instance.buttons['open'].disabled)
        self.assertFalse(self.instance.buttons['delete'].disabled)
        self.assertFalse(self.instance.buttons['run'].disabled)
        self.assertEqual(self.instance.buttons['assist'].disabled, self.instance.ai_disabled[0])
        self.assertFalse(self.instance.buttons['limitations'].disabled)
        self.assertFalse(self.instance.buttons['independence'].disabled)

    def test_load_cfg_file_returns_list_of_tests(self):
        result = self.instance.load_cfg_file('tests/')
        test_list = ['ttest', 'oneway', 'pearson', 'zscore', 'linregress']
        self.assertEqual(test_list, result)

    def test_change_cell_count(self):
        self.assertEqual(self.instance.cell_count, 0)
        self.instance.change_cell_count(1)
        self.assertEqual(self.instance.cell_count, 1)
        self.instance.change_cell_count(3)
        self.assertEqual(self.instance.cell_count, 4)
        self.instance.change_cell_count(-2)
        self.assertEqual(self.instance.cell_count, 2)

    def test_change_cell_count_does_not_make_cell_count_negative(self):
        self.instance.cell_count = 2
        self.instance.change_cell_count(-3)
        self.assertEqual(self.instance.cell_count, 0)