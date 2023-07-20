import unittest
from ipywidgets import widgets
from bring_order.inductive import Inductive
from unittest.mock import Mock, MagicMock
from bring_order.boutils import BOUtils
from bring_order.bogui import BOGui

class TestInductive(unittest.TestCase):
    def setUp(self):
        start_new = Mock()
        self.instance = Inductive(BOGui(), BOUtils(), start_new)
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
        
    def test_cell_count_starts_at_0(self):
        self.assertEqual(self.instance._cell_count, 0)

    def test_new_analysis_has_no_conclusion(self):
        self.assertIsNone(self.instance.conclusion)

    def test_that_empty_summary_returns_false(self):
        self.assertFalse(self.instance._check_value_not_empty(self.instance.summary.value))

    def test_open_cells_button_is_created(self):
        self.assertEqual(self.instance.buttons['open'].description, 'Open cells')

    def test_correct_amount_of_buttons_is_created(self):
        self.assertEqual(len(self.instance.buttons), 15)

    def test_filled_summary_returns_true(self):
        self.instance._notes.value = "Childrens' usage of psychosis medication has increased."
        self.assertTrue(self.instance._check_value_not_empty(self.instance._notes))   

    def test_new_observation_requires_notes(self):
        self.instance._check_value_not_empty = MagicMock()
        self.instance._check_value_not_empty.return_value = False
        self.instance._new_observation()
        self.assertEqual(self.instance.empty_notes_error.value, 'Observation field can not be empty')

    def test_cell_count_cannot_be_less_than_zero(self):
        self.instance._delete_last_cell()
        self.assertEqual(0, self.instance._cell_count)

    def test_delete_last_cell_decreases_cell_count(self):
        self.instance._cell_count = 5
        self.instance._delete_last_cell()
        self.assertEqual(4, self.instance._cell_count)

    def test_open_cells_increases_cell_count_correctly(self):
        self.instance._cell_count = 3
        self.instance._add_cells_int.value = 3
        self.instance._open_cells()  
        self.assertEqual(6, self.instance._cell_count)  
        self.instance.utils.create_code_cells_above.assert_called()

    def test_zero_cells_are_not_run(self):
        self.instance._run_cells()
        self.instance.utils.run_cells_above.assert_not_called()

    def test_new_observation_cannot_be_empty(self):
        self.instance._check_value_not_empty = MagicMock()
        self.instance._check_value_not_empty.return_value = False
        self.instance._new_observation()
        self.assertEqual(self.instance.empty_notes_error.value, 'Observation field can not be empty')
  
    def test_new_observation_is_saved(self):
        self.instance.observations.append("There is a lot of noise.")
        self.instance._check_value_not_empty = MagicMock()        
        self.instance.conclusion = MagicMock()
        self.instance._notes.value = "The sample is too small."
        self.instance._check_value_not_empty.return_value = True
        self.instance._new_observation()
        self.assertEqual(2, len(self.instance.observations))

    def test_get_first_words_returns_correct_string_with_short_list(self):
        words = ['Short', 'list']
        first_words = self.instance._get_first_words(words)
        self.assertEqual(first_words, 'Short list')

    def test_get_first_words_returns_correct_string_with_long_list(self):
        words = ['Long', 'list', 'has', 'more', 'words', 'than', 'short', 'list']
        first_words = self.instance._get_first_words(words)
        self.assertEqual(first_words, 'Long list has more words...')

    def test_get_first_words_returns_first_short_sentence(self):
        words = ['My', 'sentence', 'is', 'short.', 'It', 'is', 'ok.']
        first_words = self.instance._get_first_words(words)
        self.assertEqual(first_words, 'My sentence is short')

    def test_get_first_words_returns_first_short_question(self):
        words = ['What', 'to', 'ask?', 'I', 'do', 'not', 'know.']
        first_words = self.instance._get_first_words(words)
        self.assertEqual(first_words, 'What to ask?')

    def test_get_first_words_returns_first_short_exclamation(self):
        words = ['I', 'want', 'ice', 'cream!', 'Preferably', 'mint', 'Puffet.']
        first_words = self.instance._get_first_words(words)
        self.assertEqual(first_words, 'I want ice cream!')

    def test_format_observation_returns_correct_string(self):
        obs = 'The day is sunny.'
        self.instance._notes.value = obs
        self.instance.observations.append(obs)
        text = self.instance._format_observation()
        correct = '#### Observation 1: The day is sunny\\nThe day is sunny.'
        self.assertEqual(text, correct)

    def test_format_observation_returns_correct_string_with_line_breaks(self):
        obs = 'The day is sunny.\nYesterday was sunny, too.'
        self.instance._notes.value = obs
        self.instance.observations.append(obs)
        text = self.instance._format_observation()
        correct = '#### Observation 1: The day is sunny\\nThe day is sunny.<br />Yesterday was sunny, too.'
        self.assertEqual(text, correct)

    def test_format_observation_returns_correct_observation_number_in_string(self):
        obs1 = 'The day is sunny.'
        obs2 = 'Dogs are sleeping.'
        self.instance.observations.append(obs1)
        self.instance.observations.append(obs2)
        self.instance._notes.value = obs2
        text = self.instance._format_observation()
        correct = '#### Observation 2: Dogs are sleeping\\nDogs are sleeping.'
        self.assertEqual(text, correct)

    def test_format_summary_returns_correct_string(self):
        self.instance.summary.value = "It's been a nice warm summer day today."
        text = self.instance._format_summary()
        correct = "### Summary: It's been a nice warm...\\nIt's been a nice warm summer day today."
        self.assertEqual(text, correct)

    def test_format_summary_returns_correct_string_with_line_breaks(self):
        self.instance.summary.value = 'Hot day.\nI would like to go swimming.'
        text = self.instance._format_summary()
        correct = '### Summary: Hot day\\nHot day.<br />I would like to go swimming.'
        self.assertEqual(text, correct)

    def test_preconceptions_has_one_item_after_creating_Inductive_object(self):
        self.assertEqual(len(self.instance.preconceptions), 1)

    def test_add_preconception_adds_item_to_list(self):
        self.instance.preconceptions = [
            widgets.Text(value='', placeholder='Preconception 1')
        ]

        self.instance._add_preconception()
        self.assertEqual(len(self.instance.preconceptions), 2)

    def test_start_inductive_analysis_creates_markdown_cell(self):
        self.instance.start_inductive_analysis()
        self.instance.utils.create_markdown_cells_above.assert_called_with(1, '## Data exploration')

    def test_check_preconceptions_returns_false_when_no_preconceptios_are_written(self):
        self.assertFalse(self.instance._check_preconceptions())

    def test_check_preconceptions_returns_true_with_at_least_one_non_empty_value(self):
        self.instance.preconceptions = [
            widgets.Text(value='Test preconception', placeholder='Preconception 1'),
            widgets.Text(value='', placeholder='Preconception 2')
        ]
        self.assertTrue(self.instance._check_preconceptions())

    def test_format_preconceptions_returns_correct_string(self):
        self.instance.preconceptions = [
            widgets.Text(value='Dogs like treats', placeholder='Preconception 1'),
            widgets.Text(value='Chicken is the most popular flavor', placeholder='Preconception 2')
        ]
        text = self.instance._format_preconceptions()
        correct = '### Preconceptions\\n- Dogs like treats\\n- Chicken is the most popular flavor\\n### Data analysis'
        self.assertEqual(text, correct)

    def test_save_preconceptions_shows_error_if_no_preconceptions_are_written(self):
        self.instance._create_preconception_grid = Mock()
        self.instance._save_preconceptions()
        self.instance._create_preconception_grid.assert_called_with(error='You must name at least one preconception')
        self.instance.utils.create_markdown_cells_above.assert_not_called()

    def test_save_preconceptions_filters_empty_input_fields(self):
        self.instance.preconceptions = [
            widgets.Text(value='Dogs like treats', placeholder='Preconception 1'),
            widgets.Text(value='', placeholder='Preconception 2'),
            widgets.Text(value='Chicken is the most popular flavor', placeholder='Preconception 3'),
            widgets.Text(value='', placeholder='Preconception 4')
        ]
        self.instance._save_preconceptions()
        self.assertEqual(len(self.instance.preconceptions), 2)
        self.assertEqual(self.instance.preconceptions[0].value, 'Dogs like treats')
        self.assertEqual(self.instance.preconceptions[1].value, 'Chicken is the most popular flavor')

    def test_save_preconceptions_creates_markdown_cell(self):
        self.instance.preconceptions[0].value = 'Dogs like treats'
        text = '### Preconceptions\\n- Dogs like treats\\n### Data analysis'
        self.instance._save_preconceptions()
        self.instance.utils.create_markdown_cells_above.assert_called_with(
            how_many=1,
            text=text)
        
    def test_save_preconceptions_calls_create_cell_operations(self):
        self.instance._create_cell_operations = Mock()
        self.instance.preconceptions[0].value = 'Dogs like treats'
        self.instance._save_preconceptions()
        self.instance._create_cell_operations.assert_called()

    def test_open_cells_does_not_open_negative_amount_of_cells(self):
        self.instance._cell_count = 3
        self.instance._add_cells_int.value = -2
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

    def test_start_new_analysis_calls_start_new(self):
        self.instance._start_new_analysis()
        self.instance.start_new.assert_called()

    def test_submit_summary_shows_error_with_empty_summary(self):
        self.instance._display_summary = Mock()
        self.instance._submit_summary()
        self.instance._display_summary.assert_called_with(error='You must write some kind of summary')

    def test_submit_summary_creates_markdown_cell(self):
        self.instance.summary.value = 'They lived happily ever after.'
        text = '### Summary: They lived happily ever after\\nThey lived happily ever after.'
        self.instance._submit_summary()
        self.instance.utils.create_markdown_cells_above.assert_called_with(1, text=text)

    #def test_submit_summary_calls_new_analysis(self):
    #    self.instance._new_analysis = Mock()
    #    self.instance.summary.value = 'They lived happily ever after.'
    #    self.instance._submit_summary()
    #    self.instance._new_analysis.assert_called()
