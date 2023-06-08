import unittest
import src
from src.deductive import Deductive
from unittest.mock import Mock, MagicMock
from src.boutils import BOUtils
from src.bogui import BOGui

class TestDeductive(unittest.TestCase):
    """ Test class for testing the Deductive class
    """
    def setUp(self):
        """ test instance of Deductive - class
        """
        self.instance = Deductive()
        self.instance.bogui = Mock()

    def test_empty_hypothesis(self):
        self.instance.hypothesis_input.value = "" 
        self.instance.null_input.value = ""
        self.assertFalse(self.instance.check_hypotheses())

    def test_empty_hypotheses_display_warning(self):
        self.instance.hypothesis_input.value = "" 
        self.instance.null_input.value = ""
        self.instance.check_hypotheses()
        self.assertEqual(self.instance.empty_hypo_error.value, 'Hypothesis missing')
        self.assertEqual(self.instance.empty_null_error.value, 'Null hypothesis missing')    

    def test_valid_inputs_are_accepted(self):
        self.instance.hypothesis_input.value = "The Earth is flat"    
        self.instance.null_input.value = "The Earth is round"
        self.assertEqual(self.instance.empty_hypo_error.value, '')
        self.assertEqual(self.instance.empty_null_error.value, '')
        self.assertTrue(self.instance.check_hypotheses())
    
    def test_hypothesis_fields_can_be_cleared(self):
        self.instance.hypothesis_input.value = "Roses are red"
        self.instance.null_input.value = "Violets are blue"
        self.instance.clear_hypotheses()
        self.assertEqual(self.instance.hypothesis_input.value, '')
        self.assertEqual(self.instance.null_input.value, '')

    def test_saving_hypotheses_displays_grid(self):
        self.instance.hypothesis_input.value = "Roses are red"
        self.instance.null_input.value = "Violets are blue"  
        Deductive.check_hypotheses = MagicMock()   
        Deductive.check_hypotheses.return_value = True
        Deductive.create_confirmed_grid = MagicMock()
        Deductive.create_confirmed_grid.return_value = "Hello"
        self.instance.save_hypotheses(self)
        self.assertIsNotNone(self.instance.confirmed_grid)



        