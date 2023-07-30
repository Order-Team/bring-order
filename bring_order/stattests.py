from ipywidgets import widgets
from IPython.display import display
import pandas as pd
from scipy import stats

class Stattests:

    def __init__(self, bogui):
        self.dataset = pd.DataFrame()
        self.bogui = bogui

    def check_numerical_data(self, dataframe):
        """Extract numerical data from pandas dataframe
        and checks properties of data(is normally distributed).
        args:
            dataframe: pandas dataframe
        returns:
            checked_indexes: dictionary
        """
        checked_indexes = {}
        num_data = {}
        num_indexes = dataframe.select_dtypes(include="number")
        str_indexes = dataframe.select_dtypes(include=["object", "string"])

        for index in num_indexes.columns:
            lst = list(num_indexes[index].dropna())
            num_data[index] = lst
        #loop trough dtypes marked as strings or objects.
        for index in str_indexes.columns:
            lst = list(str_indexes[index].dropna())
            numerical = True
            # loop to check that all values are numerical.
            for idx, item in enumerate(lst):
                if item.lstrip('-').replace('.','',1).isdigit() is False:
                    numerical = False
                    break
                #change sring value to float.
                lst[idx] = float(item)
            if numerical:
                num_data[index] = lst
        for item in num_data:
            #call for function(s) to check data property
            ndistributed = self._is_normally_distributed(num_data[item])
            checked_indexes[item] = ndistributed

        self.chi_square_test()
        return checked_indexes

    def _is_normally_distributed(self, list_):
        """Check if values in the given list are normally distributed.
        args:
            values: list of values
        returns:
            boolean
        """
        result = stats.shapiro(list_)
        if len(result) >= 2:
            if result[1] > 0.05:
                return True
            return False
        return False

    def chi_square_test(self):
        """Creates option for chi square testing"""
        question = self.bogui.create_message('Do you want to check for variable independence?')
        yes_button = self.bogui.create_button('Yes', self.select_variables)
        chi_test_grid = widgets.AppLayout(header = question,
            left_sidebar = None,
            center = widgets.HBox([
                yes_button,
            ]),
            footer = None)
        display(chi_test_grid)

    def select_variables(self, _=None):
        """Creates dropdowns for selecting two variables from imported data and performs 
        a chi-square test of independence between them"""
        if len(self.dataset) >= 2:
            categorical = self.dataset.select_dtypes(exclude='number')
            variables = categorical.columns.values
            style = {'description_width': 'initial'}
            if len(variables) >= 2:
                explanatory = widgets.Dropdown(
                    options = variables,
                    description = 'Explanatory variable',
                    style = style
                )
                dependent = widgets.Dropdown(
                    options = variables,
                    description ='Dependent variable',
                    style = style
                )
                variable_grid = widgets.AppLayout(
                header = self.bogui.create_message('Select variables from your data'),
                left_sidebar = None,
                center = widgets.VBox([
                    explanatory,
                    dependent
                ]),
                footer=None)
                display(variable_grid)
                exp = explanatory.value
                dep = dependent.value
                def check_variable_independence(_=None):
                    crosstab = pd.crosstab(self.dataset[exp], self.dataset[dep])
                    result = stats.chi2_contingency(crosstab)
                    if len(result) >= 2:
                        message = self.bogui.create_message(
                        f"The test statistic is {result[0]:.6f} and\
                        the p-value value is {result[1]:.6f}")
                        result_view = widgets.VBox([message])
                        display(result_view)
                    else:
                        message = self.bogui.create_message(
                            "The the could not be implemented")
                        result_view = widgets.VBox([message])
                        display(result_view) 
                chi_test__button = self.bogui.create_button(
                    'Check', check_variable_independence)
                display(chi_test__button)
            else:
                message = self.bogui.create_message(
                    'There are not enough categorical variables in your data')
                display(message)
        else:
            message = self.bogui.create_message('Please import a csv file first')
            display(message)     





