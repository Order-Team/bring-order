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
        self.instance.explanatory = Mock()
        self.instance.dependent = Mock()

    def test_check_numerical_data_returns_only_filtered_data(self):
        loans_data = pd.read_csv("tests/loansData.csv")    
        self.instance.dataset = loans_data
        filtered = self.instance.check_numerical_data(loans_data)
        self.assertEqual(6, len(filtered))

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
        self.instance.bogui.create_message.assert_called_with(
            'There are not enough categorical variables to perform a chi-square test.')   

    def test_cannot_test_independence_with_one_categorical_variable(self):
        iris_data = pd.read_csv("tests/test_iris.csv")
        self.instance.dataset = iris_data
        self.instance.select_variables()
        self.instance.bogui.create_message.assert_called_with(
            'There are not enough categorical variables to perform a chi-square test.') 

    def test_independence_test_returns_true_for_independent_variables(self):
        loans_data = pd.read_csv("tests/loansData.csv")    
        self.instance.dataset = loans_data
        self.instance.select_variables = Mock()     
        self.instance.explanatory.value = 'Loan.Purpose'
        self.instance.dependent.value = 'State'
        result = self.instance.check_variable_independence()
        self.assertEqual(result, ('Loan.Purpose', 'State', True))

    def test_independence_test_returns_false_for_dependent_variables(self):
        loans_data = pd.read_csv("tests/loansData.csv")    
        self.instance.dataset = loans_data
        self.instance.select_variables = Mock()     
        self.instance.explanatory.value = 'Home.Ownership'
        self.instance.dependent.value = 'Interest.Rate'
        result = self.instance.check_variable_independence()
        self.assertEqual(result, ('Home.Ownership', 'Interest.Rate', False))        


