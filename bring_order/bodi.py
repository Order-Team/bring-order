"""Bring Order Data Import and preparation."""
from ipywidgets import widgets
from IPython.display import display, clear_output
import pandas as pd
from limitations import Limitations
from stattests import Stattests

class Bodi:
    """Creates code cells for importing data and markdown cell(s) to describe data limitations"""
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
        self.limitations = Limitations(self.bogui)
        self.file_chooser = self.bogui.create_file_chooser()
        self.stattests = Stattests(self.bogui)
        self.next_step = next_step


    @property
    def button_list(self):
        """Buttons for Bodi class.

        Returns:
            list of tuples in format (tag: str, description: str, command: func, style: str)
        """
        button_list = [
            ('save', 'Save description', self.start_data_import, 'success'),
            ('analyze', 'Analyze this data', self.check_variables, 'success'),
            ('import', 'Import manually', self.show_cell_operations, 'primary'),
            ('continue', 'Continue', self.show_cell_operations, 'primary'),
            ('open', 'Open cells', self.open_cells, 'warning'),
            ('delete', 'Delete last cell', self.delete_last_cell, 'danger'),
            ('run', 'Run cells', self.run_cells, 'primary'),
            ('add', 'Add limitation', self.add_limitation, 'primary'),
            ('remove', 'Remove limitation', self.remove_limitation, 'warning'),
            ('start', 'Start analysis', self.start_analysis_clicked, 'success'),
            ('assist', 'AI assistant', self.ai, 'primary'),
        ]
        return button_list

    def ai(self, _=None):
        self.next_step[0] = 'ai'

    def data_import_grid(self):
        """Creates widget grid"""
        cell_number_label = self.bogui.create_label(
            'Add code cells for data preparation:')

        grid = widgets.HBox([
            cell_number_label,
            self.add_cells_int,
            self.buttons['open'],
            self.buttons['run'],
            self.buttons['delete'],
            self.buttons['assist']
            ])

        return grid

    def show_cell_operations(self, _=None):
        """Button function to show buttons for cell operations."""

        clear_output(wait=True)
        display(self.data_import_grid())

    def open_cells(self, _=None):
        """Button function that opens selected number of cells above widget cell"""
        if self.add_cells_int.value > 0:
            self.cell_count += self.add_cells_int.value
            self.boutils.create_code_cells_above(self.add_cells_int.value)

    def delete_last_cell(self, _=None):
        """Button function to delete the last data import code cell"""
        if self.cell_count > 0:
            self.boutils.delete_cell_above()
            self.cell_count -= 1

    def run_cells(self, _=None):
        """Button function that runs data import cells and shows limitation inputs."""

        self.boutils.run_cells_above(self.cell_count)
        self.display_limitations_view()

    def display_limitations_view(self):
        """Displays limitation view."""

        limitation_grid = self.limitations.create_limitation_grid()
        limitation_grid.footer=widgets.VBox([
            self.limitations.empty_limitations_error,
            widgets.HBox([
                self.buttons['add'],
                self.buttons['remove']
            ])
        ])

        self.show_cell_operations()
        display(limitation_grid)
        display(self.buttons['start'])

    def add_limitation(self, _=None):
        """Button function for adding new limitation."""

        self.limitations.add_limitation()
        self.display_limitations_view()

    def remove_limitation(self, _=None):
        """Button function for removing limitation."""
        self.limitations.remove_limitation()
        self.display_limitations_view()

    def format_data_description(self):
        """Formats data description for markdown
        
        Returns:
            formatted_text (str)
        """
        title = f'# {self.title.value}'
        dataset = f'{self.data_name.value}'
        description = '<br />'.join(self.data_description.value.split('\n'))
        formatted_text = f'{title}\\n ## Data: {dataset}\\n ### Description\\n{description}'
        return formatted_text

    def start_analysis_clicked(self, _=None):
        """Button function to start analysis after data preparation"""
        if self.limitations.call_check_limitation():
            text = self.limitations.format_limitations()
            self.boutils.create_markdown_cells_above(1, text=text)
            clear_output(wait=True)
            self.next_step[0] = 'start_analysis'
        else:
            self.limitations.set_error_value('Data limitations cannot be empty')

    def fc_callback(self):
        """Opens two code cells to import pandas and read a csv file
        after the user has selected the file."""

        if self.file_chooser.selected.endswith('.csv'):
            self.file_chooser.title = self.file_chooser.selected_filename
            self.boutils.create_code_cells_above(2)
            self.boutils.execute_cell_from_current(
                distance=-2,
                code='import pandas as pd',
                hide_input=False
            )
            self.boutils.execute_cell_from_current(
                distance=1,
                code=f"data_frame = pd.read_csv('{self.file_chooser.selected}')",
                hide_input=False
            )
            self.file_chooser.register_callback(self.fc_callback_on_change)
            clear_output(wait=True)
            display(widgets.VBox([
                self.file_chooser,
                self.buttons['analyze']
            ]))

        else:
            self.file_chooser.title = 'Unknown file type, choose a csv file or import manually.'
            clear_output(wait=True)
            display(widgets.VBox([
                self.file_chooser,
                self.buttons['import']
            ]))

    def fc_callback_on_change(self):
        """Reads another csv file without importing pandas."""

        if self.file_chooser.selected.endswith('.csv'):
            self.file_chooser.title = self.file_chooser.selected_filename
            self.boutils.execute_cell_from_current(
                distance=-1,
                code=f"data_frame = pd.read_csv('{self.file_chooser.selected}')",
                hide_input=False
            )
            clear_output(wait=True)
            display(widgets.VBox([
                self.file_chooser,
                self.buttons['analyze']
            ]))

        else:
            self.file_chooser.title = 'Unknown file type, choose a csv file or import manually.'
            clear_output(wait=True)
            display(widgets.VBox([
                self.file_chooser,
                self.buttons['import']
            ]))

    def check_normal_distribution(self):
        """Checks which variables are not normally distributed and returns a message."""

        message = 'All the numerical data variables seem to be normally distributed.'
        data_frame = pd.read_csv(self.file_chooser.selected)
        n_distributed = self.stattests.check_numerical_data(data_frame)
        self.stattests.dataset = data_frame
        values_ok = []
        for key, val in n_distributed.items():
            if not val:
                values_ok.append(key)
        if len(values_ok) > 0:
            indexes = ', '.join(values_ok)
            message = f'Attention! The following data variables are not normally distributed:\
                {indexes}.'

        return message

    def check_variables(self, _=None):
        """Button function to check if data variables are normally distributed
        and to let the user check if selected data variables are independent."""

        clear_output(wait=True)
        normal_dist_result = self.bogui.create_message(self.check_normal_distribution())
        display(widgets.VBox([
            normal_dist_result,
            self.stattests.select_variables(),
            self.buttons['continue']
        ]))

    def start_data_import(self, _=None):
        """Creates markdown for data description and shows buttons for data import"""
        if self.title.value == '':
            self.bodi(error = 'Please give your study a title')
        elif self.data_name.value == '':
            self.bodi(error = 'You must name the data set')
        elif self.data_description.value == '':
            self.bodi(error = 'You must give some description of the data')

        else:
            self.boutils.create_markdown_cells_above(1, text=self.format_data_description())

            self.file_chooser.register_callback(self.fc_callback)
            self.file_chooser.title = 'Choose a data file:'

            clear_output(wait=True)
            display(widgets.VBox([
                self.file_chooser,
                self.buttons['import']
            ]))

    def initiate_ai_assistant(self, _=None):
        feature_description = self.bogui.create_message('Enter a natural language prompt. The AI assistant will propose code to implement your request.')

        api_key_label = self.bogui.create_label('Enter your Open AI key here:')


        grid = widgets.AppLayout(
        header = feature_description,
        left_sidebar = widgets.HBox([
            api_key_label,
            self.api_key,
        ]),
        center=widgets.VBox([
                self.natural_language_prompt
        ]),
        footer = widgets.VBox([
            self.buttons['send_ai'],
            self.buttons['clear_ai'],
            self.buttons['advanced_ai'],
        ]),
        pane_widths=[1, 5, 0],
        grid_gap='10px'
        )

        display(grid)


    def bodi(self, error=''):
        """Main function"""
        self.boutils.hide_current_input()
        self.boutils.hide_selected_input()
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

        if 'name' in error:
            self.data_name.focus()
        elif 'description' in error:
            self.data_description.focus()
        else:
            self.title.focus()
