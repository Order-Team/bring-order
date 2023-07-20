'''Bring Order Data Import (and preparation). 
Creates code cells for importing and cleaning data and markdown cell to describe the limitations
and requirements of data. After code cells displays "ready to analyse" button. After button is 
pressed displays text field and "ready" button. Empty text field is not accepted.'''
from ipywidgets import widgets
from IPython.display import display, clear_output
from pandas import read_csv


class Bodi:
    '''Creates code cells for importing data and markdown cell(s) to describe data limitations'''
    def __init__(self, boutils, bogui, start_analysis):
        """Class constructor
        """
        self.start_analysis = start_analysis
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
                value='Identify limitations to the data: what kind of questions cannot be answered with it?')

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
            self.start_analysis()
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
                    data_frame = read_csv(self.file_chooser.selected)
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

    def check_numerical_data(self, pd_dataframe):
        """Extract numerical data from pandas dataframe
        and checks properties of data(is normally distributed).

        args:
            pandas dataframe

        returns:
            dictionary: {index : bool}
        """
        #call for function(s) to check data property
        #d = is_normally_distributed(data)

        return {data1: True, data2: False}

    def bodi(self, error=''):
        """Main function"""
        clear_output(wait=True)


        question = self.bogui.create_message('What kind of data are you using?')
        title_label = self.bogui.create_label('Main title of your research:')
        data_name_label = self.bogui.create_label('Name of the data set:')
        description_label = self.bogui.create_label('Description of the data:')
        error_message = self.bogui.create_error_message(error)

        grid = widgets.AppLayout(
            header=question,
            left_sidebar=widgets.VBox([
                title_label,
                data_name_label,
                description_label
            ]),
            center=widgets.VBox([
                    self.title,
                    self.data_name,
                    self.data_description
            ]),
            footer=widgets.HBox([
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
