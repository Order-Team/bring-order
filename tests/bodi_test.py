import unittest
from ipywidgets import widgets
from unittest.mock import Mock, patch, MagicMock
from bring_order.boutils import BOUtils
from bring_order.bogui import BOGui
from bring_order.bodi import Bodi
from IPython import display
import pandas as pd
import scipy.stats as stats

class TestBodi(unittest.TestCase):

    def setUp(self):
        next_step = [None]

        self.instance = Bodi(BOUtils(), BOGui(), next_step=next_step)
        self.instance.boutils = Mock()
        self.instance.bogui = Mock()

    def test_correct_amount_of_buttons_is_created(self):
        self.assertEqual(len(self.instance.buttons), 7)

    def test_start_data_hides_current_input(self):
        self.instance.title.value = 'Some title'
        self.instance.data_name.value = 'Some data'
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

    def test_format_data_description_returns_correct_string(self):
        self.instance.title.value = 'My title'
        self.instance.data_name.value = 'My data'
        self.instance.data_description.value = 'List of integers.'
        text = self.instance.format_data_description()
        correct = '# My title\\n ## Data: My data\\n ### Description: \\nList of integers.'
        self.assertEqual(text, correct)

    def test_format_data_description_returns_correct_string_with_new_line(self):
        self.instance.title.value = 'My title'
        self.instance.data_name.value = 'My data'
        self.instance.data_description.value = 'List of integers.\nAscending order.'
        text = self.instance.format_data_description()
        correct = '# My title\\n ## Data: My data\\n ### Description: \\nList of integers.<br />Ascending order.'
        self.assertEqual(text, correct)

    def test_format_limitations_returns_correct_string(self):
        self.instance.data_limitations[0].value = 'Limitation0'
        self.instance.data_limitations.append(widgets.Text(f'Limitation1'))
        text = self.instance.format_limitations()
        correct = '### Limitations\\n- Limitation0\\n- Limitation1\\n'
        self.assertEqual(text, correct)

    def test_add_limitation_adds_limitation_input_to_list(self):
        self.instance.bogui.create_input_field = lambda dv, ph : widgets.Text(
            value=f'{dv}',
            placeholder=f'{ph}')
        self.instance.bogui.create_message = lambda value : widgets.HTML(value)
        self.instance.add_limitation()
        self.assertEqual(len(self.instance.data_limitations), 2)
        self.instance.add_limitation()
        self.assertEqual(len(self.instance.data_limitations), 3)

    def test_run_cells_runs_the_correct_amount_of_cells(self):
        self.instance.bogui.create_input_field = lambda dv, ph : widgets.Text(f'{dv}{ph}')
        self.instance.bogui.create_message = lambda value : widgets.HTML(value)
        self.instance.cell_count = 3
        self.instance.run_cells()
        self.instance.boutils.run_cells_above.assert_called_with(3)

    def test_call_check_limitation_returns_false_when_one_limitation_is_empty(self):
        self.instance.data_limitations.append(widgets.Text('Limitation'))
        self.instance.data_limitations.append(widgets.Text(''))
        self.assertFalse(self.instance.call_check_limitation())

    def test_call_check_limitation_returns_true_with_no_empty_limitations(self):
        self.instance.data_limitations[0].value = 'Limitation0'
        for n in range(1,3):
            self.instance.data_limitations.append(
                widgets.Text(f'Limitation{n}')
            )
        self.assertTrue(self.instance.call_check_limitation())

    def test_start_analysis_clicked_creates_markdown_cell(self):
        self.instance.data_limitations[0].value = 'Limitation0'
        self.instance.data_limitations.append(widgets.Text(f'Limitation1'))
        text = '### Limitations\\n- Limitation0\\n- Limitation1\\n'
        self.instance.start_analysis_clicked()
        self.instance.boutils.create_markdown_cells_above.assert_called_with(1, text=text)

    def test_start_analysis_clicked_sets_error_message_if_limitations_are_empty(self):
        self.assertEqual(self.instance.empty_limitations_error.value, '')
        self.instance.data_limitations.append(widgets.Text(''))
        self.instance.start_analysis_clicked()
        self.assertEqual(
            self.instance.empty_limitations_error.value,
            'Data limitations cannot be empty'
        )
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
        text = '# My title\\n ## Data: My data\\n ### Description: \\nThe sample size is 100.'
        self.instance.boutils.create_markdown_cells_above.assert_called_with(1, text=text)

    def test_start_data_import_increases_cell_count(self):
        self.instance.title.value = 'My title'
        self.instance.data_name.value = 'My data'
        self.instance.data_description.value = 'The sample size is 100.'
        self.instance.start_data_import()
        self.assertEqual(self.instance.cell_count, 1)

    def test_open_cells_does_not_open_negative_amount_of_cells(self):
        self.instance.add_cells_int.value = -1
        self.instance.open_cells()
        self.assertEqual(self.instance.cell_count, 0)
        self.instance.boutils.create_code_cells_above.assert_not_called()

    def test_remove_limitation_removes_limitations(self):
        self.instance.bogui.create_input_field = lambda dv, ph : widgets.Text(
            value=f'{dv}',
            placeholder=f'{ph}')
        self.instance.bogui.create_message = lambda value : widgets.HTML(value)
        self.instance.add_limitation()
        self.assertEqual(len(self.instance.data_limitations), 2)
        self.instance.remove_limitation()
        self.assertEqual(len(self.instance.data_limitations), 1)
        
    def test_last_limitation_is_not_removed(self):
        self.instance.remove_limitation()
        self.assertEqual(len(self.instance.data_limitations), 1)

    def test_normally_distributed_data_returns_true(self):
        numbers = [345, 346, 347, 500, 200, 400, 100]
        result = self.instance._is_normally_distributed(numbers)
        self.assertTrue(result)

    def test_not_normally_distributed_data_returns_false(self): 
        numbers = [1, 2, 3, 4, 666, 44, 1, 1, 2, 3, 2, 2, 667, 101]
        result = self.instance._is_normally_distributed(numbers)
        self.assertFalse(result)    

    def test_cannot_test_independence_without_imported_data(self):
        self.instance.select_variables()
        self.instance.bogui.create_message.assert_called_with('Please import a csv file first')   

    def test_cannot_test_independence_with_one_categorical_variable(self):
        iris_data = pd.read_csv("tests/test_iris.csv")
        self.instance.dataframe = iris_data
        self.instance.select_variables()
        self.instance.bogui.create_message.assert_called_with(
            'There are not enough categorical variables in your data') 

    def test_importing_data_prompts_for_testing_independence_of_varibales(self):
        loans_data = pd.read_csv("tests/loansData.csv")
        self.instance.chi_square_test = MagicMock()
        self.instance.dataframe = loans_data        
        self.instance.check_numerical_data(loans_data)
        self.instance.chi_square_test.assert_called()






        



