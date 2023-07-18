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

    def test_check_theory_and_hypotheses_returns_false_with_empty_hypothesis(self):
        self.instance.theory_desc.value = 'Theory starts here...'
        self.instance.hypotheses[1].value = 'x = 0'
        testValue = self.instance.check_theory_and_hypotheses()
        self.assertFalse(testValue)

    def test_check_theory_and_hypotheses_returns_false_with_empty_null_hypothesis(self):
        self.instance.theory_desc.value = 'Theory starts here...'
        self.instance.hypotheses[0].value = 'x < 0'
        testValue = self.instance.check_theory_and_hypotheses()
        self.assertFalse(testValue)

    def test_get_error_messages_gives_error_for_empty_hypothesis(self):
        self.instance.theory_desc.value = 'Theory starts here...'
        self.instance.hypotheses[1].value = 'Let assume x = 0'
        errors = self.instance.get_error_messages()
        self.assertEqual(errors, ('', 'The hypothesis must contain at least one verb', ''))

    def test_get_error_messages_gives_error_for_empty_null_hypothesis(self):
        self.instance.theory_desc.value = 'Theory starts here...'
        self.instance.hypotheses[0].value = 'Let assume x < 0'
        errors = self.instance.get_error_messages()
        self.assertEqual(errors, ('', '', 'The null hypothesis must contain at least one verb')) 
    
    def test_get_error_messages_gives_error_for_theory(self):
        self.instance.theory_desc.value = 'Theory'
        self.instance.hypotheses[0].value = "The Earth is flat"
        self.instance.hypotheses[1].value = "The Earth is round"
        errors = self.instance.get_error_messages()
        self.assertEqual(errors, ('Your must describe your theory with sentence(s) that contain at least one verb', '', ''))

    def test_check_theory_and_hypotheses_accept_valid_inputs(self):
        self.instance.data_limitations = [widgets.Text('Limitation1')]
        self.instance.theory_desc.value = 'Theory starts here...'
        self.instance.hypotheses[0].value = "The Earth is flat"    
        self.instance.hypotheses[1].value = "The Earth is round"
        testValue = self.instance.check_theory_and_hypotheses()
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
        return_value = self.instance.format_hypotheses_and_theory()
        test_str = '## Testing hypothesis: Test value\\n### Theory and insights\\nThe first claim<br />The second claim\\n### Hypotheses\\n- Hypothesis (H1): Test value        \\n- Null hypothesis (H0): Null test value\\n### Data analysis'
        self.assertEqual(return_value, test_str)

    def test_clear_theory_clears_theory(self):
        self.instance.theory_desc.value = 'Theory of testing'
        self.instance.clear_theory()
        self.assertEqual(self.instance.theory_desc.value, '')


        
