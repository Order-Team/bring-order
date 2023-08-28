import unittest
from ipywidgets import widgets
from bring_order.deductive import Deductive
from unittest.mock import Mock, MagicMock
from bring_order.boutils import BOUtils
from bring_order.bogui import BOGui
from bring_order.boval import BOVal

class TestDeductive(unittest.TestCase):
    """ Test class for testing the Deductive class
    """
    def setUp(self):
        """ test instance of Deductive - class
        """
        next_step = [None]
        ai_disabled = [False]
        self.instance = Deductive(BOGui(), BOUtils(), BOVal(), ai_disabled, next_step)
        self.instance.boutils = Mock()

    def test_check_theory_and_hypotheses_submit_returns_false_with_empty_hypothesis(self):
        self.instance.theory_desc.value = 'Theory starts here.'
        self.instance.hypotheses[1].value = 'The quick brown fox jumps over the lazy dog'
        testValue = self.instance.check_theory_and_hypotheses(False)
        self.assertFalse(testValue)

    def test_check_theory_and_hypotheses_validate_returns_false_with_invalid_null_hypothesis(self):
        self.instance.theory_desc.value = 'The quick brown fox jumps over the lazy dog'
        self.instance.hypotheses[0].value = 'The quick brown fox jumps over the lazy dog'
        testValue = self.instance.check_theory_and_hypotheses(True)
        self.assertFalse(testValue)

    def test_get_error_messages_gives_error_for_invalid_hypothesis(self):
        self.instance.theory_desc.value = 'The quick brown fox jumps over the lazy dog'
        self.instance.hypotheses[0].value = 'True/False'
        self.instance.hypotheses[1].value = 'The quick brown fox jumps over the lazy dog'
        errors = self.instance._get_error_messages()
        self.assertEqual(errors, ('', 'The hypothesis must contain at least 3 words and must not contain special characters', ''))

    def test_get_error_messages_gives_error_for_invalid_null_hypothesis(self):
        self.instance.theory_desc.value = 'The quick brown fox jumps over the lazy dog'
        self.instance.hypotheses[0].value = 'The quick brown fox jumps over the lazy dog'
        self.instance.hypotheses[1].value = 'ABCABCABC123123@@@'
        errors = self.instance._get_error_messages()
        self.assertEqual(errors, ('', '', 'The null hypothesis must contain at least 3 words and must not contain special characters')) 

    def test_get_error_messages_gives_error_for_theory(self):
        self.instance.theory_desc.value = 'Theory'
        self.instance.hypotheses[0].value = "The quick brown fox jumps over the lazy dog"
        self.instance.hypotheses[1].value = "The quick brown fox does not jump over the lazy dog"
        errors = self.instance._get_error_messages()
        self.assertEqual(errors, ('The theory must contain at least 3 words and must not contain special characters', '', ''))

    def test_get_error_messages_gives_error_for_empty_value(self):
        self.instance.theory_desc.value = ""
        self.instance.hypotheses[0].value = ""
        self.instance.hypotheses[1].value = ""
        errors = self.instance._get_error_messages()
        self.assertEqual(errors, ('The theory must contain at least 3 words and must not contain special characters',
                            'The hypothesis must contain at least 3 words and must not contain special characters',
                            'The null hypothesis must contain at least 3 words and must not contain special characters'))

    def test_get_error_messages_gives_no_error_for_right_values(self):
        self.instance.theory_desc.value = "The quick brown fox jumps over the lazy dog"
        self.instance.hypotheses[0].value = "The quick brown fox jumps over the lazy dog"
        self.instance.hypotheses[1].value = "The quick brown fox does not jump over the lazy dog"
        errors = self.instance._get_error_messages()
        self.assertEqual(errors, ('', '', ''))

    def test_get_warning_messages_gives_warning_for_hypothesis(self):
        self.instance.theory_desc.value = 'The quick brown fox jumps over the lazy dog'
        self.instance.hypotheses[0].value = 'over the lazy dog'
        self.instance.hypotheses[1].value = 'The quick brown fox jumps over the lazy dog'
        errors = self.instance._get_warning_messages()
        self.assertEqual(errors, ('', 'Warning! The hypothesis does not fill criteria of\
             including a subject, a predicate and an object.', ''))

    def test_get_warning_messages_gives_warning_for_null_hypothesis(self):
        self.instance.theory_desc.value = 'The quick brown fox jumps over the lazy dog'
        self.instance.hypotheses[0].value = 'The quick brown fox jumps over the lazy dog'
        self.instance.hypotheses[1].value = "The quick brown fox"
        errors = self.instance._get_warning_messages()
        self.assertEqual(errors, ('', '', 'Warning! The null hypothesis does not fill criteria of\
             including a subject, a predicate and an object.'))

    def test_get_warning_messages_gives_warning_for_theory(self):
        self.instance.theory_desc.value = 'Theory theory theory'
        self.instance.hypotheses[0].value = "The quick brown fox jumps over the lazy dog"
        self.instance.hypotheses[1].value = "The quick brown fox does not jump over the lazy dog"
        errors = self.instance._get_warning_messages()
        self.assertEqual(errors, ('Warning! The theory does not fill criteria of\
             including a subject, a predicate and an object.', '', ''))

    def test_check_theory_and_hypotheses_accept_valid_inputs(self):
        self.instance.data_limitations = [widgets.Text('Limitation1')]
        self.instance.theory_desc.value = "The quick brown fox jumps over the lazy dog" 
        self.instance.hypotheses[0].value = "The quick brown fox jumps over the lazy dog"
        self.instance.hypotheses[1].value = "The quick brown fox does not jump over the lazy dog"
        testValue = self.instance.check_theory_and_hypotheses(True)
        self.assertTrue(testValue)

    def test_check_theory_and_hypotheses_accept_valid_inputs_without_validation(self):
        self.instance.data_limitations = [widgets.Text('Limitation1')]
        self.instance.theory_desc.value = "The quick brown fox jumps over the lazy dog"
        self.instance.hypotheses[0].value = "The quick brown fox jumps over the lazy dog"
        self.instance.hypotheses[1].value = "The quick brown fox does not jump over the lazy dog"
        testValue = self.instance.check_theory_and_hypotheses(False)
        self.assertTrue(testValue)

    def test_check_theory_and_hypotheses_not_accept_wrong_inputs(self):
        self.instance.data_limitations = [widgets.Text('Limitation1')]
        self.instance.theory_desc.value = "The quick brown fox jumps over the lazy dog"
        self.instance.hypotheses[0].value = "The quick brown"
        self.instance.hypotheses[1].value = "The quick brown fox does not jump over the lazy dog"
        testValue = self.instance.check_theory_and_hypotheses(True)
        self.assertFalse(testValue)

    def test_check_theory_and_hypotheses_not_accept_wrong_inputs_without_validation(self):
        self.instance.data_limitations = [widgets.Text('Limitation1')]
        self.instance.theory_desc.value = "The quick brown fox jumps over the lazy dog"
        self.instance.hypotheses[0].value = "The quick"
        self.instance.hypotheses[1].value = "The quick brown fox does not jump over the lazy dog"
        testValue = self.instance.check_theory_and_hypotheses(False)
        self.assertFalse(testValue)

    def test_hypothesis_fields_can_be_cleared(self):
        self.instance.hypotheses[0].value = "Roses are red"
        self.instance.hypotheses[1].value = "Violets are blue"
        self.instance.clear_hypotheses()
        self.assertEqual(self.instance.hypotheses[0].value, '')
        self.assertEqual(self.instance.hypotheses[1].value, '')

    def test_bad_hypotheses_are_cleared(self):
        self.instance.clear_hypotheses = MagicMock()
        self.instance.bad_hypotheses()
        self.instance.clear_hypotheses.assert_called()

    def test_format_hypotheses_and_theory_returns_correct_string(self):
        self.instance.hypotheses[0].value = 'Test value'
        self.instance.hypotheses[1].value = 'Null test value'
        self.instance.theory_desc.value = 'The first claim\nThe second claim'
        self.maxDiff = None
        return_value = self.instance._format_hypotheses_and_theory()
        test_str = '## Testing hypothesis: Test value\\n### Theory and insights\\nThe first claim<br />The second claim\\n### Hypotheses\\n- Hypothesis (H1): Test value        \\n- Null hypothesis (H0): Null test value\\n### Data analysis'
        self.assertEqual(return_value, test_str)

    def test_clear_theory_clears_theory(self):
        self.instance.theory_desc.value = 'Theory of testing'
        self.instance.clear_theory()
        self.assertEqual(self.instance.theory_desc.value, '')

    def test_open_cells_increases_cell_count_correctly(self):
        self.instance.cell_count = 2
        self.instance.add_cells_int.value = 3
        self.instance.open_cells()
        self.assertEqual(5, self.instance.cell_count)
        self.instance.boutils.create_code_cells_above.assert_called()
    
    def test_open_cells_not_increases_cell_count_if_value_is_zero(self):
        self.instance.cell_count = 2
        self.instance.add_cells_int.value = 0
        self.instance.open_cells()  
        self.assertEqual(2, self.instance.cell_count)
        self.instance.boutils.create_code_cells_above.assert_not_called()

    def test_delete_last_cells_reduce_cell_count(self):
        self.instance.cell_count = 5
        self.instance.delete_last_cell()
        self.instance.delete_last_cell()
        self.assertEqual(3, self.instance.cell_count)
        self.instance.boutils.delete_cell_above.assert_called()

    def test_delete_last_cells_not_reduce_cell_count_is_value_is_zero(self):
        self.instance.cell_count = 0
        self.instance.delete_last_cell()
        self.assertEqual(0, self.instance.cell_count)
        self.instance.boutils.delete_cell_above.assert_not_called()

    def test_run_cells_calls_the_method_with_correct_value(self):
        self.instance.cell_count = 3
        self.instance.run_cells()
        self.instance.boutils.run_cells_above.assert_called_with(3)

    def test_clear_cells_calls_the_method_with_correct_value(self):
        self.instance.cell_count = 3
        self.instance.clear_cells()
        self.instance.boutils.clear_code_cells_above.assert_called_with(3)

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

    def test_run_cells_checks_for_unsuitable_tests_in_code(self):
        self.instance.cell_count = 2
        self.instance.not_normal = ['sepallength', 'petalcount', 'petalwidth']
        self.instance.checklist = ['zscore', 'pearson', 'oneway']
        self.instance.run_cells()
        self.instance.boutils.check_cells_above.assert_called()

    def test_submit_theory_calls_check_theory(self):
        self.instance.check_theory_and_hypotheses = MagicMock()
        self.instance.submit_theory_and_hypotheses()
        self.instance.check_theory_and_hypotheses.assert_called_with(False)

    def test_save_theory_saves_correct_text(self):
        self.instance.boutils.create_markdown_cells_above = MagicMock()
        self.instance.hypotheses[0].value = 'Test value'
        self.instance.hypotheses[1].value = 'Null test value'
        self.instance.theory_desc.value = 'The first claim\nThe second claim'
        self.maxDiff = None
        self.instance.save_theory_and_hypotheses()
        self.instance.boutils.create_markdown_cells_above.assert_called_with(1,text='## Testing hypothesis: Test value\\n### Theory and insights\\nThe first claim<br />The second claim\\n### Hypotheses\\n- Hypothesis (H1): Test value        \\n- Null hypothesis (H0): Null test value\\n### Data analysis')

    def test_representation(self):
        printed = self.instance.__repr__()
        self.assertEqual(printed, '')

