'''Bring Order Data Import and preparation. '''
from ipywidgets import widgets
from IPython.display import display, clear_output
import pandas as pd
from scipy import stats
from pandas import read_csv



class Bodi:
    '''Creates code cells for importing data and markdown cell(s) to describe data limitations'''
    def __init__(self, boutils, bogui, next_step):
        """Class constructor
        """
        self.boutils = boutils
        self.bogui = bogui
        self.cell_count = 0
        self.buttons = self.bogui.init_buttons(self.button_list)
        self.title = self.bogui.create_input_field()
        self.data_name = self.bogui.create_input_field()
        self.data_description = self.bogui.create_text_area()
        self.add_cells_int = self.bogui.create_int_text()
        self.import_grid = self.data_import_grid()
        self.data_limitations = [self.bogui.create_input_field('', 'Limitation 1')]
        self.limitation_grid = None
        self.empty_limitations_error = self.bogui.create_error_message()
        self.file_chooser = self.bogui.create_file_chooser()
        self.dataframe = pd.DataFrame()
        self.next_step = next_step

    @property
    def button_list(self):
        """Buttons for Bodi class.

        Returns:
            list of tuples in format (tag: str, description: str, command: func, style: str)
        """

        button_list = [
            ('save', 'Save description', self.start_data_import, 'success'),
            ('open', 'Open cells', self.open_cells, 'warning'),
            ('delete', 'Delete last cell', self.delete_last_cell, 'danger'),
            ('run', 'Run cells', self.run_cells, 'primary'),
            ('add', 'Add limitation', self.add_limitation, 'primary'),
            ('start', 'Start analysis', self.start_analysis_clicked, 'success'),
            ('remove', 'Remove limitation', self.remove_limitation, 'warning')
        ]

        return button_list

    def data_import_grid(self):
        """Creates widget grid"""
        cell_number_label = self.bogui.create_label(
            'Add code cells for data preparation:')

        grid = widgets.HBox([
            cell_number_label,
            self.add_cells_int,
            self.buttons['open'],
            self.buttons['run'],
            self.buttons['delete']
            ])
        return grid


    def open_cells(self, _=None):
        """Button function that opens selected number of cells above widget cell"""
        if self.add_cells_int.value > 0:
            self.cell_count += self.add_cells_int.value
            self.boutils.create_code_cells_above(self.add_cells_int.value)

    def delete_last_cell(self, _=None):
        """Button function to delete the last data import code cell"""
        if self.cell_count > 1:
            self.boutils.delete_cell_above()
            self.cell_count -= 1

    def run_cells(self, _=None):
        """Button function that runs data import cells"""
        self.boutils.run_cells_above(self.cell_count)
        if self.limitation_grid:
            self.limitation_grid.close()
        self.display_limitations()

    def add_limitation(self, _=None):
        """Button function to add new limitation"""
        if self.limitation_grid:
            self.limitation_grid.close()
        self.data_limitations.append(self.bogui.create_input_field
                                    ('',f'Limitation {len(self.data_limitations)+1}'))
        self.empty_limitations_error.value = ''
        self.display_limitations()

    def remove_limitation(self, _=None):
        """Button function to remove a limitation field"""
        if len(self.data_limitations) > 1:
            # implementation
            self.data_limitations.pop()
            self.limitation_grid.close()
            self.empty_limitations_error.value = ''
            self.display_limitations()

    def display_limitations(self):
        """Shows text boxes and buttons for adding limitations"""
        limitations_label = self.bogui.create_message(
                value='Identify limitations to the data: what kind of\
                questions cannot be answered with it?')

        limitation_grid = widgets.VBox(self.data_limitations)

        self.limitation_grid = widgets.AppLayout(
            header=limitations_label,
            center=limitation_grid,
            footer=widgets.VBox([
                self.empty_limitations_error,
                widgets.HBox([
                    self.buttons['start'],
                    self.buttons['add'],
                    self.buttons['remove']
                ])
            ]),
            pane_heights=['30px', 1, '70px'],
            grid_gap='12px'
        )
        display(self.limitation_grid)

    def check_limitations(self, item=''):
        """Checks that limitations have been given or commented"""
        if item == '':
            return False
        return True

    def call_check_limitation(self):
        """Checks that none of the limitations is empty"""
        for limitation in self.data_limitations:
            if not self.check_limitations(limitation.value):
                return False
        return True

    def format_limitations(self):
        """Formats limitations for markdown to prevent Javascript error        
        Returns:
            formatted_limitations (str)
        """
        formatted_limitations = '### Limitations\\n'
        for item in self.data_limitations:
            limitation = '<br />'.join(item.value.split('\n'))
            limitation_text = f'- {limitation}\\n'
            formatted_limitations += limitation_text

        return formatted_limitations

    def start_analysis_clicked(self, _=None):
        """Button function to start analysis after data preparation"""
        if self.call_check_limitation():
            text = self.format_limitations()
            self.boutils.create_markdown_cells_above(1, text=text)
            clear_output(wait=True)
            self.next_step[0] = 'start_analysis'
        else:
            self.empty_limitations_error.value = 'Data limitations cannot be empty'

    def format_data_description(self):
        """Formats data description for markdown
        
        Returns:
            formatted_text (str)
        """
        title = f'# {self.title.value}'
        dataset = f'{self.data_name.value}'
        description = '<br />'.join(self.data_description.value.split('\n'))
        formatted_text = f'{title}\\n ## Data: {dataset}\\n ### Description: \\n{description}'
        return formatted_text

    def start_data_import(self, _=None):
        """Creates markdown for data description and shows buttons for data import"""
        if self.title.value == '':
            self.bodi(error='Please give your study a title')
        elif self.data_name.value == '':
            self.bodi(error='You must name the data set')
        elif self.data_description.value == '':
            self.bodi(error='You must give some description of the data')

        else:
            self.boutils.hide_current_input()
            clear_output(wait=True)

            def fc_callback():
                self.file_chooser.title = self.file_chooser.selected_filename
                if self.file_chooser.selected.endswith('.csv'):
                    data_frame = pd.read_csv(self.file_chooser.selected)
                    n_distributed = self.check_numerical_data(data_frame)
                    self.dataframe = data_frame
                    values_ok = []
                    for key, val in n_distributed.items():
                        if not val:
                            values_ok.append(key)
                    if len(values_ok) > 0:
                        indexes = ', '.join(values_ok)
                        self.file_chooser.title = f'Attention! Following data in index(es):\
                                                {indexes} are not normally distributed.'
                else:
                    self.file_chooser.title = 'Unknown file type, please import manually'
                self.import_grid.layout.visibility = 'visible'

            self.file_chooser.register_callback(fc_callback)
            self.file_chooser.title = 'Choose a data file'
            self.import_grid.layout.visibility = 'hidden'
            display(widgets.VBox([
                self.file_chooser,
                self.import_grid
                ]))

            self.boutils.create_markdown_cells_above(1, text=self.format_data_description())
            self.cell_count += 1

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

    def bodi(self, error=''):
        """Main function"""
        clear_output(wait=True)
        question = self.bogui.create_message('What kind of data are you using?')
        title_label = self.bogui.create_label('Main title of your research:')
        data_name_label = self.bogui.create_label('Name of the data set:')
        description_label = self.bogui.create_label('Description of the data:')
        error_message = self.bogui.create_error_message(error)

        grid = widgets.AppLayout(
            header = question,
            left_sidebar = widgets.VBox([
                title_label,
                data_name_label,
                description_label
            ]),
            center=widgets.VBox([
                    self.title,
                    self.data_name,
                    self.data_description
            ]),
            footer = widgets.HBox([
                self.buttons['save'],
                error_message,
            ]),
            pane_widths=[1, 5, 0],
            grid_gap='10px'
        )
        display(grid)
        if 'data_name' in error:
            self.data_name.focus()
        elif 'description' in error:
            self.data_description.focus()
        else:
            self.title.focus()

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
        if len(self.dataframe) >= 2:
            categorical = self.dataframe.select_dtypes(exclude='number')
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
                def check_variable_independence(_=None):
                    exp = explanatory.value
                    dep = dependent.value
                    crosstab = pd.crosstab(self.dataframe[exp], self.dataframe[dep])
                    result = stats.chi2_contingency(crosstab)
                    if len(result) >= 2:
                        message = self.bogui.create_message(
                            f"The test statistic is {result[0]:.6f} and\
                                the p-value value is {result[1]:.6f}")
                        result_view = widgets.VBox([message])
                        display(result_view)
                    else:
                        display("Error")         
                chi_test__button = self.bogui.create_button('Check', check_variable_independence)
                display(chi_test__button)
            else:
                message = self.bogui.create_message(
                    'There are not enough categorical variables in your data')
                display(message)

        else:
            message = self.bogui.create_message('Please import a csv file first')
            display(message)
