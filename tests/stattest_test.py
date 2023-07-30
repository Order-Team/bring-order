import unittest
from unittest.mock import Mock, MagicMock
from bring_order.stattests import Stattests
import pandas as pd
import scipy.stats as stats

class TestStattests(unittest.TestCase):

    def setUp(self):
        bogui = Mock()
        self.instance = Stattests(bogui)
        self.instance.bogui = bogui

    def test_normally_distributed_data_returns_true(self):
        numbers = [345, 346, 347, 500, 200, 400, 100]
        result = self.instance._is_normally_distributed(numbers)
        self.assertTrue(result)

    def test_not_normally_distributed_data_returns_false(self): 
        numbers = [1, 2, 3, 4, 666, 44, 1, 1, 2, 3, 2, 2, 667, 101]
        result = self.instance._is_normally_distributed(numbers)
        self.assertFalse(result)    

    def test_cannot_test_independence_without_imported_data(self):
        self.instance.select_variables()
        self.instance.bogui.create_message.assert_called_with('Please import a csv file first')   

    def test_cannot_test_independence_with_one_categorical_variable(self):
        iris_data = pd.read_csv("tests/test_iris.csv")
        self.instance.dataset = iris_data
        self.instance.select_variables()
        self.instance.bogui.create_message.assert_called_with(
            'There are not enough categorical variables in your data') 

    def test_importing_data_prompts_for_testing_independence_of_varibales(self):
        loans_data = pd.read_csv("tests/loansData.csv")
        self.instance.chi_square_test = MagicMock()
        self.instance.dataset = loans_data        
        self.instance.check_numerical_data(loans_data)
        self.instance.chi_square_test.assert_called()    