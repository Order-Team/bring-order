import unittest
import src
from src.deductive import Deductive
from unittest.mock import Mock, ANY
from src.boutils import BOUtils
from src.bogui import BOGui

class TestDeductive(unittest.TestCase):
    """ Test class for testing the Deductive class
    """
    def setUp(self):
        """ test instance of Deductive - class
        """
        self.instance = Deductive()

    def test_empty_hypothesis(self):
        self.assertFalse(self.instance.check_hypotheses())
    
    def test_hypothesis_fields_can_be_cleared(self):
        self.instance.hypothesis_input.value = "Roses are red"
        self.instance.null_input.value = "Violets are blue"
        self.instance.clear_hypotheses()
        self.assertEqual(self.instance.hypothesis_input.value, '')
        self.assertEqual(self.instance.null_input.value, '')