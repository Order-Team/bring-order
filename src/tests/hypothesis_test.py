
import unittest
from hypothesis import Hypothesis

class TestHypothesis(unittest.TestCase):
    """ Test class for testing the Hypothesis - class
    """
    def setUp(self):
        """ test instance of Hypothesis - class
        """
        self.instance = Hypothesis()
        self.instance.hypothesis.value = 'x = 0'
        self.instance.null_hypothesis.value = 'x > 0'

    def test_populating_fields(self):
        """ generating new values and checking if they are the same.
        """
        self.instance.hypothesis.value = 'y = 10'
        self.instance.null_hypothesis.value = 'y > 10'
        self.assertEqual(self.instance.hypothesis.value, 'y = 10')
        self.assertEqual(self.instance.null_hypothesis.value, 'y > 10')

    def test_clear_button_clicked(self):
        """ checking if test clear button clears values
        """
        self.instance.clear_button_clicked()
        self.assertEqual(self.instance.hypothesis.value, '')
        self.assertEqual(self.instance.null_hypothesis.value, '')

    def test_save_button_clicked(self):
        """ checking that save button saves the hypothesis and null hypothesis - strings
        """
        self.instance.save_button_clicked()
        self.assertEqual(self.instance.hypothesis, 'Hypothesis: x = 0')
        self.assertEqual(self.instance.null_hypothesis, 'Null hypothesis: x > 0')

    def test_initialize_buttons(self):
        """ checking that initialize button does not return None
        """
        save_button,clear_button = self.instance.initialize_buttons()
        self.assertNotEqual (save_button,None)
        self.assertNotEqual(clear_button, None)
    
    def test_empty_input_hypothesis_and_nullhypothesis(self):
        self.instance.hypothesis.value = ''
        self.instance.null_hypothesis.value = ''
        self.instance.save_button_clicked()
        self.assertEqual(self.instance.error_message, 'Hypothesis and Null hypothesis missing')
   

    def test_empty_input_hypothesis(self):
        self.instance.hypothesis.value = ''
        self.instance.null_hypothesis.value = 'x > 0'
        self.instance.save_button_clicked()
        self.assertEqual(self.instance.error_message, 'Hypothesis missing')


    def test_empty_input_nullhypothesis(self):
        self.instance.hypothesis.value = 'x = 0'
        self.instance.null_hypothesis.value = ''
        self.instance.save_button_clicked()
        self.assertEqual(self.instance.error_message, 'Null hypothesis missing')
