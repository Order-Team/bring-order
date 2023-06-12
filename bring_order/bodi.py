'''Bring Order Data Import (and preparation). 
Creates code cells for importing and cleaning data and markdown cell to describe the limitations
and requirements of data. After code cells displays "ready to analyse" button. After button is 
pressed displays text field and "ready" button. Empty text field is not accepted.'''
from ipywidgets import widgets
from IPython.display import display
from boutils import BOUtils
from bogui import BOGui


class Bodi:
    '''Creates code cells for importing data and markdown cell(s) to describe data limitations'''
    def __init__(self, start_analysis):
        """Class constructor
        """
        self.start_analysis = start_analysis
        self.boutils = BOUtils()
        self.bogui = BOGui()
        self.cell_count = 1
        self.add_cells_int = self.bogui.create_int_text()
        self.import_grid = self.data_import_grid()
        self.data_limitations = self.bogui.create_text_area()
        self.limitation_grid = None
        self.empty_limitations_error = self.bogui.create_error_message()

    def data_import_grid(self):
        """Creates widget grid"""
        cell_number_label = self.bogui.create_label(
            'Add code cells for data preparation:')

        open_cells_button = self.create_open_cells_button()
        delete_cell_button = self.create_delete_button()
        run_cells_button = self.create_run_button()

        grid = widgets.HBox([
            cell_number_label,
            self.add_cells_int,
            open_cells_button,
            run_cells_button,
            delete_cell_button
        ])

        return grid

    def create_open_cells_button(self):
        """Creates button for opening new code cells for analysis.

        Returns:
            button
        """
        def open_cells(_=None):
            """Button function"""
            self.cell_count += self.add_cells_int.value
            self.boutils.create_code_cells_at_bottom(self.add_cells_int.value)

        button = self.bogui.create_button(
            desc='Open cells',
            command=open_cells,
            style='warning')

        return button

    def create_delete_button(self):
        """Creates button for deleting the last code cell

        Returns:
            button
        """
        def delete_last_cell(_=None):
            """Button function"""
            if self.cell_count > 2:
                self.boutils.delete_cell(
                    self.cell_count)
                self.cell_count -= 1

        button = self.bogui.create_button(
            desc='Delete last cell',
            command=delete_last_cell,
            style='danger')

        return button

    def create_run_button(self):
        """Creates button"""
        def run_cells(_=None):
            """Button function"""
            self.boutils.run_cells(
                self.cell_count)

            if self.limitation_grid:
                self.limitation_grid.close()

            limitations_label = self.bogui.create_message(
                value='Data limitations:')
            analyze_button = self.create_analysis_button()
            self.limitation_grid = widgets.AppLayout(
                left_sidebar=limitations_label,
                center=self.data_limitations,
                footer=widgets.HBox([analyze_button, self.empty_limitations_error])
            )

            display(self.limitation_grid)

        button = self.bogui.create_button(
            desc='Run cells',
            command=run_cells,
            style='primary')

        return button
    
    def check_limitations(self):
        if self.data_limitations.value == '':
            return False
        return True
    
    def create_analysis_button(self):
        """Creates button"""
        def start_analysis(_=None):
            """Button function"""
            if self.check_limitations():
                limitations = f'''Data limitations:\n{self.data_limitations.value}'''
                print(limitations)
                self.import_grid.close()
                self.limitation_grid.close()
                self.start_analysis()

            else:
                self.empty_limitations_error.value = 'Data limitations cannot be empty'

        button = self.bogui.create_button(
            'Start analysis',
            start_analysis
        )

        return button

    def bodi(self):
        '''Main function'''
        self.boutils.create_markdown_cells_at_bottom(1, text="## Data description")
        self.cell_count += 1
        display(self.import_grid)
