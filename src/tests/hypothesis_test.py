
import unittest
from hypothesis import Hypothesis
from ipywidgets import widgets


class TestHypothesis(unittest.TestCase):   
    def setUp(self):
        self.instance = Hypothesis()
        self.instance.hypothesis.value = 'x = 0'
        self.instance.null_hypothesis.value = 'x > 0'

    def test_set_hypothesis(self):
        self.assertEqual(self.instance.set_hypothesis(),True)
           
    def test_populating_fields(self):
        self.instance.hypothesis.value = 'y = 10'
        self.instance.null_hypothesis.value = 'y > 10'
        self.assertEqual(self.instance.hypothesis.value, 'y = 10')
        self.assertEqual(self.instance.null_hypothesis.value, 'y > 10')

    def test_clear_button_clicked(self):
        self.instance._clear_button_clicked()
        self.assertEqual(self.instance.hypothesis.value, '')
        self.assertEqual(self.instance.null_hypothesis.value, '')
    
    def test_save_button_clicked(self):
        self.instance._save_button_clicked()
        self.assertEqual(self.instance.hypothesis, 'Hypothesis: x = 0')
        self.assertEqual(self.instance.null_hypothesis, 'Null hypothesis: x > 0')


    def test_initialize_buttons(self):
        a,b = self.instance._initialize_buttons()
        self.assertNotEqual (a,None)
        self.assertNotEqual(b, None)
        


       