import unittest
import bring_order
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

    def test_empty_hypothesis(self):
        self.instance.hypotheses[0].value = ""
        self.instance.hypotheses[1].value = ""
        testValue = self.instance.check_hypotheses()
        self.assertFalse(testValue)

    def test_empty_hypotheses_display_warning(self):
        self.instance.hypotheses[0].value = ""
        self.instance.hypotheses[1].value = ""
        self.instance.check_hypotheses()
        self.assertEqual(self.instance.empty_hypo_error.value, 'Hypothesis missing')
        self.assertEqual(self.instance.empty_null_error.value, 'Null hypothesis missing')

    def test_valid_inputs_are_accepted(self):
        self.instance.hypotheses[0].value = "The Earth is flat"    
        self.instance.hypotheses[1].value = "The Earth is round"
        testValue = self.instance.check_hypotheses()
        self.assertEqual(self.instance.empty_hypo_error.value, '')
        self.assertEqual(self.instance.empty_null_error.value, '')
        self.assertTrue(testValue)
    
    def test_hypothesis_fields_can_be_cleared(self):
        self.instance.hypotheses[0].value = "Roses are red"
        self.instance.hypotheses[1].value = "Violets are blue"
        self.instance.clear_hypotheses()
        self.assertEqual(self.instance.hypotheses[0].value, '')
        self.assertEqual(self.instance.hypotheses[1].value, '')

    def test_saving_hypotheses_displays_grid(self):
        self.instance.hypotheses[0].value = "Roses are red"
        self.instance.hypotheses[1].value = "Violets are blue"
        self.instance.check_hypotheses = MagicMock()   
        self.instance.check_hypotheses.return_value = True
        self.instance.create_confirmed_grid = MagicMock()
        self.instance.create_confirmed_grid.return_value = "Hello"
        self.instance.save_hypotheses(self)
        self.assertIsNotNone(self.instance.confirmed_grid)

    def test_bad_hypotheses_are_cleared(self):
        self.instance.clear_hypotheses = MagicMock()
        self.instance.limitation_prompt = MagicMock()
        self.instance.bad_hypotheses()
        self.instance.clear_hypotheses.assert_called()

    def test_all_done_hides_widgets(self):
        self.instance.save_results = MagicMock()
        self.instance.all_done()
        self.instance.save_results.assert_called()
        
        





        
