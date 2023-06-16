"""Class for Inductive analysis"""
#import uuid
from ipywidgets import widgets
from IPython.display import display

class Inductive:
    """Class that guides inductive analysis"""
    def __init__(self, bogui, boutils):
        """Class constructor."""
        self.bogui = bogui
        self.utils = boutils
        self.cell_count = 0
        button_list = [['Open cells', self.open_cells, 'warning'],
                   ['Delete last cell', self.delete_last_cell, 'danger'],
                   ['Clear cells', self.clear_cells, 'danger'],
                   ['Run cells', self.run_cells, 'primary'],
                   ['New analysis', self.start_new_analysis, 'success'],
                   ["Ready", self.execute_ready, 'primary']
                 ]
        self.buttons = self.init_buttons(button_list)
        self.add_cells_int = self.bogui.create_int_text()
        self.notes = self.bogui.create_text_area()
        self.cell_operations = self.create_cell_operations()
        self.conclusion = None
        self.empty_notes_error = self.bogui.create_error_message()

    def open_cells(self, _=None):
        """Open cells button function that opens the selected
        number of code cells and one markdown cell"""
        self.cell_count += self.add_cells_int.value + 1
        self.utils.create_code_cells_above(self.add_cells_int.value)
        self.utils.create_markdown_cells_above(1,'## Explain what you have observed')

    def delete_last_cell(self, _=None):
        """Delete last cell-button function"""
        if self.cell_count > 0:
            self.utils.delete_cell_above()
            self.cell_count -= 1

    def clear_cells(self, _=None):
        """Clears all code cells above."""
        self.utils.clear_code_cells_above(self.cell_count)

    def run_cells(self, _=None):
        """Executes cells above and displays text area for summarization of analysis."""
        self.utils.run_cells_above(self.cell_count)

        if self.conclusion:
            self.conclusion.close()

        notes_label = self.bogui.create_label(value='Summarize your analysis:')
        self.conclusion = widgets.VBox([widgets.HBox(
                [notes_label, self.notes]),self.buttons['Ready'], self.empty_notes_error])

        display(self.conclusion)

    def start_new_analysis(self, _=None):
        """Starts new bringorder object"""
        command = 'BringOrder(data_import=False)'
        self.utils.create_and_execute_code_cell(command)

    def execute_ready(self, _=None):
        """Executes code cells after Ready button is clicked."""
        if self.check_notes():
            self.save_results()
            self.new_analysis()
        else:
            self.empty_notes_error.value = 'Summary cannot be empty'

    def save_results(self):
        """Prints notes"""
        text = f'''Inductive Analysis\n Notes:\n {self.notes.value}'''

        """tallentaminen
        
        new = InductiveSummary()
        new.add(uuid.uuid4(), 15, 'data') """
        print(text)
        self.cell_operations.close()
        self.conclusion.close()

    def check_notes(self):
        '''Checks that summarization was filled'''
        if self.notes.value == '':
            return False
        return True

    def init_buttons(self, buttons):
        """Initializes buttons needed by inductive class."""
        button_list = {}
        for button in buttons:
            new_button = self.bogui.create_button(desc=button[0],
                                                  command=button[1], style=button[2])
            button_list[button[0]] = new_button
        return button_list

    def create_cell_operations(self):
        """Displays buttons for operations in inductive analysis"""
        cell_number_label = self.bogui.create_label('Add code cells for your analysis:')

        grid = widgets.AppLayout(
            left_sidebar=widgets.HBox([cell_number_label, self.add_cells_int]),
            right_sidebar=widgets.TwoByTwoLayout(top_left=self.buttons['Open cells'],
                                                 bottom_left=self.buttons['Run cells'],
                                                 top_right=self.buttons['Delete last cell'],
                                                 bottom_right=self.buttons['Clear cells']),
            height='auto', width='70%')
        return grid

    def start_inductive_analysis(self):
        """Starts inductive analysis"""
        display(self.cell_operations)

    def new_analysis(self):
        '''Display button to start a new analysis'''
        display(self.buttons['New analysis']) #(self.new_analysis_button)

    def __repr__(self):
        return ''
