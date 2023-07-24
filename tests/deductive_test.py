import unittest
from ipywidgets import widgets
from bring_order.deductive import Deductive
from unittest.mock import Mock, MagicMock
from bring_order.boutils import BOUtils
from bring_order.bogui import BOGui

class TestDeductive(unittest.TestCase):
    """ Test class for testing the Deductive class
    """
    def setUp(self):
        """ test instance of Deductive - class
        """
        start_new = Mock()
        self.instance = Deductive(BOGui(), BOUtils(), start_new)
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
        self.assertEqual(errors, ('', 'The hypothesis must be at least 8 characters and\
             not contain special characters', ''))

    def test_get_error_messages_gives_error_for_invalid_null_hypothesis(self):
        self.instance.theory_desc.value = 'The quick brown fox jumps over the lazy dog'
        self.instance.hypotheses[0].value = 'The quick brown fox jumps over the lazy dog'
        self.instance.hypotheses[1].value = 'ABCABCABC123123@@@'
        errors = self.instance._get_error_messages()
        self.assertEqual(errors, ('', '', 'The null hypothesis must be at least 8 characters and\
             not contain special characters')) 
    
    def test_get_error_messages_gives_error_for_theory(self):
        self.instance.theory_desc.value = 'Theory'
        self.instance.hypotheses[0].value = "The quick brown fox jumps over the lazy dog"
        self.instance.hypotheses[1].value = "The quick brown fox does not jump over the lazy dog"
        errors = self.instance._get_error_messages()
        self.assertEqual(errors, ('The theory must be at least 8 characters and\
             not contain special characters', '', ''))
    
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

    def test_all_done_hides_widgets(self):
        self.instance.save_results = MagicMock()
        self.instance.all_done()
        self.instance.save_results.assert_called()
        
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
