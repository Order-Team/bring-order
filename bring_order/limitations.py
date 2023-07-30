from ipywidgets import widgets
from IPython.display import display, clear_output
import pandas as pd
from scipy import stats

class Limitations:

    def __init__(self, bogui, boutils):
        self.bogui = bogui
        self.boutils = boutils
        self.buttons = self.bogui.init_buttons(self.button_list)
        self.data_limitations = [self.bogui.create_input_field('', 'Limitation 1')]
        self.limitation_grid = None
        self.empty_limitations_error = self.bogui.create_error_message()

    @property
    def button_list(self):
        """Buttons for Limitations class.
        Returns:
            list of tuples in format (tag: str, description: str, command: func, style: str)
        """
        button_list = [
            ('add', 'Add limitation', self.add_limitation, 'primary'),
            ('remove', 'Remove limitation', self.remove_limitation, 'warning')
        ]    
        return button_list

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

    def set_error_value(self, text):
        self.empty_limitations_error.value = text