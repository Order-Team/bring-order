'''Bring Order Data Import (and preparation). 
Creates code cells for importing and cleaning data and markdown cell to describe the limitations
and requirements of data. After code cells displays "ready to analyse" button. After button is 
pressed displays text field and "ready" button. Empty text field is not accepted.'''
from ipywidgets import widgets
from IPython.display import display, clear_output
from ipywidgets import GridspecLayout


class Bodi:
    '''Creates code cells for importing data and markdown cell(s) to describe data limitations'''
    def __init__(self, boutils, bogui, start_analysis):
        """Class constructor
        """
        self.start_analysis = start_analysis
        self.boutils = boutils
        self.bogui = bogui
        self.cell_count = 0
        self.data_description = self.bogui.create_text_area()
        self.save_description_button = self.create_save_description_button()
        self.add_cells_int = self.bogui.create_int_text()
        self.import_grid = self.data_import_grid()
        self.data_limitations = []
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
            self.boutils.create_code_cells_above(self.add_cells_int.value)

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
            if self.cell_count > 1:
                self.boutils.delete_cell_above()
                self.cell_count -= 1

        button = self.bogui.create_button(
            desc='Delete last cell',
            command=delete_last_cell,
            style='danger')

        return button
    
    def add_limitation(self, event=None):
    
        #self.check_limitations()
        if self.limitation_grid:
                self.limitation_grid.close()

        self.data_limitations.append(self.bogui.create_text_area('',f'Limitation {len(self.data_limitations)+1}: '))

        self.display_limitations()
        
    def create_add_more_limitations_button(self):
        button = self.bogui.create_button(
                'Add more limitations',
                self.add_limitation
            )
        return button
    

    def display_limitations(self):
        limitations_label = self.bogui.create_message(
                value='Identify limitations to the data: what kind of questions cannot be answered with it?')
            
        analyze_button = self.create_analysis_button()
        add_more_limitations_button = self.create_add_more_limitations_button()

        rows = len(self.data_limitations)
        if rows == 0:
            self.data_limitations.append(self.bogui.create_text_area('', f'Limitation 1: '))
            rows +=1

        grid = GridspecLayout(rows, 1)

        for i in range(rows):
            for j in range(1):
                grid[i, j] = self.data_limitations[i]
        

        self.limitation_grid = widgets.AppLayout(
            header=limitations_label,
            center=grid,
            footer=widgets.HBox([analyze_button, self.empty_limitations_error, add_more_limitations_button ])
        )

        display(self.limitation_grid)

    def create_run_button(self):
        """Creates button"""
        def run_cells(_=None):
            """Button function"""
            self.boutils.run_cells_above(
                self.cell_count)

            if self.limitation_grid:
                self.limitation_grid.close()
            
            self.display_limitations()


        button = self.bogui.create_button(
            desc='Run cells',
            command=run_cells,
            style='primary')

        return button

    def check_limitations(self, item=''):
        '''Checks that limitations have been given or commented'''
        if item == '':
            return False
        return True
        

    def call_check_limitation(self):
        for limitation in self.data_limitations:
            if not self.check_limitations(limitation.value):
                return False
        return True


    def create_analysis_button(self):
        """Creates button"""
        def start_analysis(_=None):
            """Button function"""
            if self.call_check_limitation():
                limitations = ' \\n '.join(f"Limitation {count}: {item.value} \\n" for count, item in enumerate(self.data_limitations, start=1))
                text = f'## Data limitations \\n {limitations}'
                self.boutils.create_markdown_cells_above(1, text=text)
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

    def create_save_description_button(self):
        """Creates button"""
        button = self.bogui.create_button(
            desc='Save description',
            command=self.start_data_import,
            style='success'
        )

        return button

    def start_data_import(self, _=None):
        """Creates markdown for data description and shows buttons for data import"""
        if self.data_description.value == '':
            self.bodi(error='You must give some description of the data')
        
        else:
            self.boutils.hide_current_input()
            clear_output(wait=True)
            display(self.import_grid)

            description = '<br />'.join(self.data_description.value.split('\n'))
            text = f'# Data preparation\\n## Data description\\n{description}\\n## Data import and cleaning'
            self.boutils.create_markdown_cells_above(1, text=text)
            self.cell_count += 1

    def bodi(self, error=''):
        '''Main function'''
        clear_output(wait=True)

        description_label = self.bogui.create_label('Describe your data:')
        error_message = self.bogui.create_error_message(error)

        grid = widgets.VBox([
            widgets.HBox([description_label, self.data_description]),
            error_message,
            self.save_description_button
        ])

        display(grid)
