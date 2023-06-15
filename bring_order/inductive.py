"""Class for Inductive analysis"""
import uuid
from ipywidgets import widgets
from IPython.display import display

class Inductive:
    """Class that guides inductive analysis"""
    def __init__(self, bogui, boutils):
        """Class constructor."""
        self.cell_count = 0
        self.bogui = bogui
        self.utils = boutils
        self.add_cells_int = self.bogui.create_int_text()
        self.cell_operations = self.create_cell_operations()
        self.notes = self.bogui.create_text_area()
        self.conclusion = None
        self.empty_notes_error = self.bogui.create_error_message()

    def create_open_cells_button(self):
        """Creates button"""
        def open_cells(_=None):
            """Button function"""
            self.cell_count += self.add_cells_int.value * 2
            self.utils.create_code_and_observation_cells(self.add_cells_int.value)

        button = self.bogui.create_button(
            desc='Open cells',
            command=open_cells,
            style='warning')

        return button

    def create_delete_button(self):
        """Creates button"""
        def delete_last_cell(_=None):
            """Button function"""
            if self.cell_count > 0:
                self.utils.delete_cell(self.cell_count)
                self.utils.delete_cell(self.cell_count-1)
                self.cell_count -= 2

        button = self.bogui.create_button(
            desc='Delete last cells',
            command=delete_last_cell,
            style='danger')

        return button

    def create_run_button(self):
        """Creates button"""
        def run_cells(_=None):
            """Button function"""
            self.utils.run_cells(self.cell_count)

            if self.conclusion:
                self.conclusion.close()

            notes_label = self.bogui.create_label(
                value='Summarize your analysis:')
            ready_button = self.create_ready_button()
            self.conclusion = widgets.VBox([widgets.HBox(
                    [notes_label, self.notes]),ready_button, self.empty_notes_error])

            display(self.conclusion)

        button = self.bogui.create_button(
            desc='Run cells', command=run_cells, style='primary')

        return button

    def create_clear_button(self):
        """Creates button"""
        def clear_cells(_=None):
            """Button function"""
            self.utils.clear_code_and_observation_cells(
                self.cell_count)

        button = self.bogui.create_button(
            desc='Clear cells', command=clear_cells, style='danger')
        return button

    def save_results(self):
        """Prints notes"""
        text = f'''Inductive Analysis\n Notes:\n {self.notes.value}'''

        """ tallentaminen
        
        new = InductiveSummary()
        new.add(uuid.uuid4(), 15, 'data') """
        print(text)
        self.cell_operations.close()
        self.conclusion.close()

    def create_ready_button(self):
        """Creates Ready button"""
        def execute_ready(_=None):
            if self.check_notes():
                self.save_results()
                self.new_analysis()
            else:
                self.empty_notes_error.value = 'Summary cannot be empty'

        button = self.bogui.create_button(
            desc="Ready",
            style='primary',
            command=execute_ready
        )
        return button

    def check_notes(self):
        '''Checks that summarization was filled'''
        if self.notes.value == '':
            return False
        return True

    def create_new_analysis_button(self):
        """Creates New Analysis button"""
        def start_new_analysis(_=None):
            """Button function"""
            command = 'BringOrder(data_import=False)'
            self.utils.create_and_execute_code_cell(command)

        button = self.bogui.create_button(
            desc='New analysis',
            command=start_new_analysis)

        return button

    def create_cell_operations(self):
        """Creates buttons for operations in inductive analysis"""
        cell_number_label = self.bogui.create_label(
            'Add code cells for your analysis:')

        open_cells_button = self.create_open_cells_button()
        delete_cell_button = self.create_delete_button()
        clear_cells_button = self.create_clear_button()
        run_cells_button = self.create_run_button()

        grid = widgets.AppLayout(
            left_sidebar=widgets.HBox([cell_number_label, self.add_cells_int]),
            right_sidebar=widgets.TwoByTwoLayout(
                top_left=open_cells_button,
                bottom_left=run_cells_button,
                top_right=delete_cell_button,
                bottom_right=clear_cells_button
                ),
            height='auto',
            width='70%')

        return grid

    def start_inductive_analysis(self):
        """Starts inductive analysis"""
        display(self.cell_operations)

    def new_analysis(self):
        '''Created button to start a new analysis'''
        new_button = self.create_new_analysis_button()
        display(new_button)

    def __repr__(self):
        return ''
