'''Bring Order Data Import and preparation. '''
from ipywidgets import widgets
from IPython.display import display, clear_output
import pandas as pd
from limitations import Limitations
from stattests import Stattests

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
        self.limitations = Limitations(self.bogui, self.boutils)
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
            ('open', 'Open cells', self.open_cells, 'warning'),
            ('delete', 'Delete last cell', self.delete_last_cell, 'danger'),
            ('run', 'Run cells', self.run_cells, 'primary'),
            ('start', 'Start analysis', self.start_analysis_clicked, 'success')
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
        if self.limitations.limitation_grid:
            self.limitations.limitation_grid.close()
        self.limitations.display_limitations()
        #if self.buttons['start']:
        #    self.buttons['start'].close()
        display(self.buttons['start'])    

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
    
    def start_analysis_clicked(self, _=None):
        """Button function to start analysis after data preparation"""
        if self.limitations.call_check_limitation():
            text = self.limitations.format_limitations()
            self.boutils.create_markdown_cells_above(1, text=text)
            clear_output(wait=True)
            self.next_step[0] = 'start_analysis'
        else:
            self.limitations.set_error_value('Data limitations cannot be empty')    

    def start_data_import(self, _=None):
        """Creates markdown for data description and shows buttons for data import"""
        if self.title.value == '':
            self.bodi(error = 'Please give your study a title')
        elif self.data_name.value == '':
            self.bodi(error = 'You must name the data set')
        elif self.data_description.value == '':
            self.bodi(error = 'You must give some description of the data')

        else:
            self.boutils.hide_current_input()
            clear_output(wait=True)

            def fc_callback():
                self.file_chooser.title = self.file_chooser.selected_filename
                if self.file_chooser.selected.endswith('.csv'):
                    data_frame = pd.read_csv(self.file_chooser.selected)
                    n_distributed = self.stattests.check_numerical_data(data_frame)
                    self.stattests.dataset = data_frame
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


