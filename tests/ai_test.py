import unittest
from bring_order.boutils import BOUtils
from bring_order.bogui import BOGui
from bring_order.bodi import Bodi
from bring_order.ai import Ai
from unittest.mock import Mock, MagicMock
import pandas as pd


class TestAi(unittest.TestCase):

    def setUp(self):
        next_step = [None]
        self.instance = Ai(BOGui(), BOUtils(), next_step=next_step)
        self.instance.boutils = Mock()
        self.instance.bogui = Mock()        
        self.instance.context_selection = Mock()

    def test_dataframe_variables_are_added_as_context(self):
        self.instance.dataset = pd.read_csv('tests/test_iris.csv')
        self.instance.context_selection.value = 'Include dataset'
        self.instance.select_context()
        test_context = 'Variables of the dataset are sepallength, sepalwidth, petallength, petalwidth, class'
        self.assertEqual(test_context, self.instance.context)
        