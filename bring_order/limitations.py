"""Data limitations manager"""
from ipywidgets import widgets

class Limitations:
    """Manages data limitations through different phases of analysis."""
    def __init__(self, bogui):
        """Class constructor."""
        self.bogui = bogui
        self.data_limitations = [self.bogui.create_input_field('', 'Limitation 1')]
        self.empty_limitations_error = self.bogui.create_error_message()

    def add_limitation(self):
        """Adds new limitation input to list."""
        self.data_limitations.append(self.bogui.create_input_field
                                    ('',f'Limitation {len(self.data_limitations)+1}'))
        self.empty_limitations_error.value = ''

    def remove_limitation(self):
        """Removes the last limitation input from list."""
        if len(self.data_limitations) > 1:
            self.data_limitations.pop()
            self.empty_limitations_error.value = ''

    def create_limitation_grid(self):
        """Returns text boxes for adding limitations"""
        limitations_label = self.bogui.create_message(
                value='Identify limitations to the data: what kind of\
                questions cannot be answered with it?')

        limitation_grid = widgets.AppLayout(
            header=limitations_label,
            center=widgets.VBox(self.data_limitations),
            pane_heights=['30px', 1, '70px'],
            grid_gap='12px'
        )

        return limitation_grid

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
        """Sets error value."""
        self.empty_limitations_error.value = text

    def get_values(self):
        """Returns a list of the limitations as stirngs."""

        return [limitation.value for limitation in self.data_limitations]

    def get_limitations_as_bullet_list(self):
        """Returns limitations as a HTML bullet list."""

        text = '<h4>Attention:</h4>\n<ul>\n'
        text += '\n'.join([
            '<li>' + limitation.value + '</li>'
            for limitation in self.data_limitations])
        text += '\n</ul>'

        return widgets.HTML(text)
