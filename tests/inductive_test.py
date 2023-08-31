import unittest
from ipywidgets import widgets
from bring_order.inductive import Inductive
from unittest.mock import Mock, MagicMock
from bring_order.boutils import BOUtils
from bring_order.bogui import BOGui
from bring_order.boval import BOVal

class TestInductive(unittest.TestCase):
    def setUp(self):
        next_step = [None]
        ai_disabled = [False]
        self.instance = Inductive(BOGui(), BOUtils(), BOVal(), ai_disabled, next_step)
        self.instance.boval = BOVal()
        self.instance.utils = Mock()
        self.instance.bogui = Mock()
        self.instance.bogui.create_button = Mock()
        self.instance.bogui.create_input_field = lambda value, ph: widgets.Text(
            value=value,
            placeholder=ph
        )
        self.instance.bogui.create_error_message = lambda value: widgets.HTML(value=value)
        self.instance.bogui.create_message = lambda value: widgets.HTML(value=value)
        self.instance.bogui.create_label = lambda value: widgets.Label(value=value)
        self.instance.bogui.create_grid = lambda rows, cols, items: widgets.VBox(items)
        
    def test_cell_count_starts_at_0(self):
        self.assertEqual(self.instance._cell_count, 0)

    def test_new_analysis_has_no_conclusion(self):
        self.assertIsNone(self.instance.conclusion)

    def test_that_empty_summary_returns_false(self):
        self.assertFalse(self.instance.boval.check_value_not_empty(self.instance.fields[2].value))

    def test_open_cells_button_is_created(self):
        self.assertEqual(self.instance.buttons['open'].description, 'Open cells')

    def test_correct_amount_of_buttons_is_created(self):
        self.assertEqual(len(self.instance.buttons), 13)

    def test_filled_summary_returns_true(self):
        self.instance.fields[1].value = "Childrens' usage of psychosis medication has increased."
        self.assertTrue(self.instance.boval.check_value_not_empty(self.instance.fields[1]))

    def test_new_observation_requires_notes(self):
        self.instance.boval.check_value_not_empty = MagicMock()
        self.instance.boval.check_value_not_empty.return_value = False
        self.instance._new_observation()
        self.assertEqual(self.instance.fields[3].value, 'The observation cannot be empty or contain special symbols')

    def test_cell_count_cannot_be_less_than_zero(self):
        self.instance._delete_last_cell()
        self.assertEqual(0, self.instance._cell_count)

    def test_delete_last_cell_decreases_cell_count(self):
        self.instance._cell_count = 5
        self.instance._delete_last_cell()
        self.assertEqual(4, self.instance._cell_count)

    def test_open_cells_increases_cell_count_correctly(self):
        self.instance.utils.create_code_cells_above = MagicMock()
        self.instance._cell_count = 3
        self.instance.fields[0].value = 3
        self.instance._open_cells()
        self.assertEqual(6, self.instance._cell_count)
        self.instance.utils.create_code_cells_above.assert_called()

    def test_zero_cells_are_not_run(self):
        self.instance.utils.run_cells_above = MagicMock()
        self.instance._run_cells()
        self.instance.utils.run_cells_above.assert_not_called()

    def test_new_observation_cannot_be_empty(self):
        self.instance.fields[1].value = ''
        self.instance._new_observation()
        self.assertEqual(self.instance.fields[3].value, 'The observation cannot be empty or contain special symbols')
  
    def test_new_observation_is_saved(self):
        self.instance.lists[1].append("There is a lot of noise.")
        self.instance.conclusion = MagicMock()
        self.instance.fields[1].value = "The sample is too small."
        self.instance._new_observation()
        self.assertEqual(2, len(self.instance.lists[1]))

    def test_format_observation_returns_correct_string(self):
        obs = 'The day is sunny.'
        self.instance.fields[1].value = obs
        self.instance.lists[1].append(obs)
        text = self.instance._format_observation()
        correct = '#### Observation 1: The day is sunny\\nThe day is sunny.'
        self.assertEqual(text, correct)

    def test_format_observation_returns_correct_string_with_line_breaks(self):
        obs = 'The day is sunny.\nYesterday was sunny, too.'
        self.instance.fields[1].value = obs
        self.instance.lists[1].append(obs)
        text = self.instance._format_observation()
        correct = '#### Observation 1: The day is sunny\\nThe day is sunny.<br />Yesterday was sunny, too.'
        self.assertEqual(text, correct)

    def test_format_observation_returns_correct_observation_number_in_string(self):
        obs1 = 'The day is sunny.'
        obs2 = 'Dogs are sleeping.'
        self.instance.lists[1].append(obs1)
        self.instance.lists[1].append(obs2)
        self.instance.fields[1].value = obs2
        text = self.instance._format_observation()
        correct = '#### Observation 2: Dogs are sleeping\\nDogs are sleeping.'
        self.assertEqual(text, correct)

    def test_format_summary_returns_correct_string(self):
        self.instance.fields[2].value = "It's been a nice warm summer day today."
        text = self.instance._format_summary()
        correct = "### Summary: It's been a nice warm...\\nIt's been a nice warm summer day today."
        self.assertEqual(text, correct)

    def test_format_summary_returns_correct_string_with_line_breaks(self):
        self.instance.fields[2].value = 'Hot day.\nI would like to go swimming.'
        text = self.instance._format_summary()
        correct = '### Summary: Hot day\\nHot day.<br />I would like to go swimming.'
        self.assertEqual(text, correct)

    def test_preconceptions_has_one_item_after_creating_Inductive_object(self):
        self.assertEqual(len(self.instance.lists[0]), 1)

    def test_add_preconception_adds_item_to_list(self):
        self.instance.lists[0] = [
            widgets.Text(value='', placeholder='Preconception 1')
        ]

        self.instance._add_preconception()
        self.assertEqual(len(self.instance.lists[0]), 2)

    def test_start_inductive_analysis_creates_markdown_cell(self):
        self.instance.utils.create_markdown_cells_above = MagicMock()
        self.instance.start_inductive_analysis()
        self.instance.utils.create_markdown_cells_above.assert_called_with(1, '## Data exploration')

    def test_check_preconceptions_returns_false_when_no_preconceptios_are_written(self):
        self.assertFalse(self.instance._check_preconceptions())

    def test_check_preconceptions_returns_true_with_at_least_one_non_empty_value(self):
        self.instance.lists[0] = [
            widgets.Text(value='Test preconception', placeholder='Preconception 1'),
            widgets.Text(value='', placeholder='Preconception 2')
        ]
        self.assertTrue(self.instance._check_preconceptions())

    def test_format_preconceptions_returns_correct_string(self):
        self.instance.lists[0] = [
            widgets.Text(value='Dogs like treats', placeholder='Preconception 1'),
            widgets.Text(value='Chicken is the most popular flavor', placeholder='Preconception 2')
        ]
        text = self.instance._format_preconceptions()
        correct = '### Preconceptions\\n- Dogs like treats\\n- Chicken is the most popular flavor\\n### Data analysis'
        self.assertEqual(text, correct)

    def test_save_preconceptions_shows_error_if_no_preconceptions_are_written(self):
        self.instance._create_preconception_grid = Mock()
        self.instance._save_preconceptions()
        self.instance._create_preconception_grid.assert_called_with(error='The preconception cannot be empty or contain special symbols')
        self.instance.utils.create_markdown_cells_above.assert_not_called()

    def test_save_preconceptions_filters_empty_input_fields(self):
        self.instance.lists[0] = [
            widgets.Text(value='Dogs like treats', placeholder='Preconception 1'),
            widgets.Text(value='', placeholder='Preconception 2'),
            widgets.Text(value='Chicken is the most popular flavor', placeholder='Preconception 3'),
            widgets.Text(value='', placeholder='Preconception 4')
        ]
        self.instance._save_preconceptions()
        self.assertEqual(len(self.instance.lists[0]), 2)
        self.assertEqual(self.instance.lists[0][0].value, 'Dogs like treats')
        self.assertEqual(self.instance.lists[0][1].value, 'Chicken is the most popular flavor')

    def test_save_preconceptions_creates_markdown_cell(self):
        self.instance.lists[0][0].value = 'Dogs like treats'
        text = '### Preconceptions\\n- Dogs like treats\\n### Data analysis'
        self.instance._save_preconceptions()
        self.instance.utils.create_markdown_cells_above.assert_called_with(
            how_many=1,
            text=text)
        
    def test_save_preconceptions_calls_create_cell_operations(self):
        self.instance._create_cell_operations = Mock()
        self.instance.lists[0][0].value = 'Dogs like treats'
        self.instance._save_preconceptions()
        self.instance._create_cell_operations.assert_called()

    def test_open_cells_does_not_open_negative_amount_of_cells(self):
        self.instance._cell_count = 3
        self.instance.fields[0].value = -2
        self.instance._open_cells()
        self.assertEqual(self.instance._cell_count, 3)
        self.instance.utils.create_code_cells_above.assert_not_called()

    def test_clear_cells_clears_correct_amount_of_cells(self):
        self.instance._cell_count = 3
        self.instance._clear_cells()
        self.instance.utils.clear_code_cells_above.assert_called_with(3)

    def test_run_cells_does_not_run_zero_cells(self):
        self.instance._run_cells()
        self.instance.utils.run_cells_above.assert_not_called()

    def test_run_cells_runs_correct_amount_of_cells(self):
        self.instance._cell_count = 3
        self.instance._run_cells()
        self.instance.utils.run_cells_above.assert_called_with(3)

    def test_run_cells_disables_buttons(self):
        self.instance._buttons_disabled = Mock()
        self.instance._cell_count = 1
        self.instance._run_cells()
        self.instance._buttons_disabled.assert_called_with(True)

    def test_run_cells_creates_conclusion_grid(self):
        self.instance._cell_count = 1
        self.instance._run_cells()
        self.assertIsNotNone(self.instance.conclusion)

    def test_submit_summary_shows_error_with_empty_summary(self):
        self.instance._display_summary = MagicMock()
        self.instance._submit_summary()
        self.instance._display_summary.assert_called_with(error='The summary cannot be empty or contain special symbols')

    def test_submit_summary_creates_markdown_cell(self):
        self.instance.utils.create_markdown_cells_above = MagicMock()
        self.instance.fields[2].value = 'They lived happily ever after.'
        text = '### Summary: They lived happily ever after\\nThey lived happily ever after.'
        self.instance._submit_summary()
        self.instance.utils.create_markdown_cells_above.assert_called_with(1, text=text)

    def test_submit_summary_calls_new_analysis(self):
        self.instance._evaluation_of_analysis = MagicMock()
        self.instance.fields[2].value = 'They lived happily ever after.'
        self.instance._submit_summary()
        self.instance._evaluation_of_analysis.assert_called()

    def test_change_cell_count(self):
        self.assertEqual(self.instance._cell_count, 0)
        self.instance.change_cell_count(1)
        self.assertEqual(self.instance._cell_count, 1)
        self.instance.change_cell_count(3)
        self.assertEqual(self.instance._cell_count, 4)
        self.instance.change_cell_count(-2)
        self.assertEqual(self.instance._cell_count, 2)

    def test_change_cell_count_does_not_make_cell_count_negative(self):
        self.instance._cell_count = 2
        self.instance.change_cell_count(-3)
        self.assertEqual(self.instance._cell_count, 0)

    def test_run_cells_checks_for_unsuitable_tests_in_code(self):
        self.instance._cell_count = 2
        self.instance.not_normal = ['sepallength', 'petalcount', 'petalwidth']
        self.instance.checklist = ['zscore', 'pearson', 'oneway']
        self.instance._run_cells()
        self.instance.utils.check_cells_above.assert_called()
    
    def test_execute_calls_summary_view(self):
        self.instance._display_summary = MagicMock()
        self.instance._execute_ready()
        self.instance._display_summary.assert_called()
    
    def test_save_results_saves_correct_text(self):
        self.instance.utils.create_markdown_cells_above = MagicMock()
        self.instance._close_evaluation = MagicMock()
        self.instance.data_limitations = [widgets.Text('Limitation1')]
        self.instance.lists[2].append(widgets.Checkbox(value=False,description='Prec1'))
        self.instance.lists[2].append(widgets.Checkbox(value=True,description='Prec2'))
        self.instance.fields[4].value = 35
        self.instance.fields[5].value = 50
        self.instance._save_results()
        self.instance.utils.create_markdown_cells_above.assert_called_once_with(how_many=1, text='### Evaluation of the analysis \\n#### Limitations that were noticed in the data:\\n- Limitation1\\n#### Evaluations:\\n- According to the pre-evaluation, the analysis confirmed\
                approximately 35 % of the preconceptions.\\n- According to the final evaluation, the analysis confirmed approximately\
                50 % of the preconceptions.\\n#### The analysis did not support these preconceptions:\\n- Prec1\\n')
        self.instance._close_evaluation.assert_called()

    def test_save_results_saves_correct_text_if_all_preconceptions_are_true(self):
        self.instance.utils.create_markdown_cells_above = MagicMock()
        self.instance.data_limitations = [widgets.Text('Limitation1')]
        self.instance.lists[2].append(widgets.Checkbox(value=True,description='Prec1'))
        self.instance.lists[2].append(widgets.Checkbox(value=True,description='Prec2'))
        self.instance.fields[4].value = 25
        self.instance.fields[5].value = 15
        self.instance._save_results()
        self.instance.utils.create_markdown_cells_above.assert_called_once_with(how_many=1, text='### Evaluation of the analysis \\n#### Limitations that were noticed in the data:\\n- Limitation1\\n#### Evaluations:\\n- According to the pre-evaluation, the analysis confirmed\
                approximately 25 % of the preconceptions.\\n- According to the final evaluation, the analysis confirmed approximately\
                15 % of the preconceptions.\\n#### Note that the analysis appears to confirm\
            all stated preconceptions!\\n')

    def test_complete_evaluation_saves_correct_text(self):
        self.instance.fields[6] = widgets.Text('The difference between evaluations evaluation caused by testing')
        self.instance.utils.create_markdown_cells_above = MagicMock()
        self.instance._complete_evaluation()
        self.instance.utils.create_markdown_cells_above.assert_called_with(1,text='#### The difference between the pre- and final evaluation caused by: \\nThe difference between evaluations evaluation caused by testing')

    def test_complete_evaluation_saves_correct_text_if_explanation_is_empty(self):
        self.instance.fields[6] = widgets.Text('')
        self.instance.utils.create_markdown_cells_above = MagicMock()
        self.instance._complete_evaluation()
        self.instance.utils.create_markdown_cells_above.assert_called_with(1,text='#### The difference between the pre- and final evaluation caused by: \\nNo explanation was given!')

    def test_representation(self):
        printed = self.instance.__repr__()
        self.assertEqual(printed, '')