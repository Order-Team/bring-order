from ipywidgets import widgets
from IPython.display import display
from bo_utils import BOUtils


class Inductive:
    """Class that guides inductive analysis"""
    def __init__(self, start_cell):
        """Class constructor.

        Args:
            start_cell (int): the index of the notebook cell where the method is called
        """
        self.first_cell_index = start_cell
        self.cell_count = 1
        self.utils = BOUtils()
        self.add_cells_int = self.utils.create_int_text()
        self.notes = self.utils.create_text_area()
        self.conclusion = None

    def create_open_cells_button(self):
        """Creates button"""
        def open_cells(_=None):
            """Button function"""
            self.cell_count += self.add_cells_int.value
            self.utils.create_code_cells(self.add_cells_int.value)

        button = self.utils.create_button(
            desc='Open cells',
            command=open_cells,
            style='warning')

        return button

    def create_delete_button(self):
        """Creates button"""
        def delete_last_cell(_=None):
            """Button function"""
            self.utils.delete_cell(
                self.first_cell_index+self.cell_count-1)
            self.cell_count -= 1

        button = self.utils.create_button(
            desc='Delete last cell',
            command=delete_last_cell,
            style='danger')

        return button

    def create_run_button(self):
        """Creates button"""
        def run_cells(_=None):
            """Button function"""
            self.utils.run_cells(
                self.first_cell_index+1,
                self.first_cell_index+self.cell_count)

            if self.conclusion:
                self.conclusion.close()

            notes_label = self.utils.create_label(
                value='Write notes about your analysis:')
            new_button = self.create_new_analysis_button()
            self.conclusion = widgets.VBox(
                [widgets.HBox(
                    [notes_label, self.notes]),
                    new_button])

            display(self.conclusion)

        button = self.utils.create_button(
            desc='Run cells',
            command=run_cells,
            style='primary')

        return button

    def create_clear_button(self):
        """Creates button"""
        def clear_cells(_=None):
            """Button function"""
            self.utils.clear_code_cells_below(
                self.first_cell_index+1,
                self.cell_count-1)

        button = self.utils.create_button(
            desc='Clear cells',
            command=clear_cells,
            style='danger')
        return button

    def save_results(self):
        """Prints notes"""
        text = f'''
        Inductive Analysis\n
        Notes:\n
        {self.notes.value}
        '''
        print(text)

    def create_new_analysis_button(self):
        """Creates button"""
        def start_new_analysis(_=None):
            """Button function"""
            self.save_results()
            # Todo: start new analysis, close widgets

        button = self.utils.create_button(
            desc='New analysis',
            command=start_new_analysis)

        return button

    def start_inductive_analysis(self):
        """Starts inductive analysis"""
        cell_number_label = self.utils.create_label(
            'Add code cells for your analysis:')

        open_cells_button = self.create_open_cells_button()
        delete_cell_button = self.create_delete_button()
        clear_cells_button = self.create_clear_button()
        run_cells_button = self.create_run_button()

        grid = widgets.AppLayout(
            left_sidebar=widgets.HBox(
                [cell_number_label, self.add_cells_int]),
            right_sidebar=widgets.TwoByTwoLayout(
                top_left=open_cells_button,
                bottom_left=run_cells_button,
                top_right=delete_cell_button,
                bottom_right=clear_cells_button
            ),
            height='auto',
            width='70%')

        display(grid)
