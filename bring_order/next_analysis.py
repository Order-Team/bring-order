from ipywidgets import widgets
from IPython.display import display, clear_output, Javascript

class NextAnalysis:
    def __init__(self, bogui, boutils, next_step):
        self.bogui = bogui
        self.boutils = boutils
        self.next_step = next_step
        self.buttons = self.bogui.init_buttons(self.button_list)
    
    @property
    def button_list(self):
        button_list = [
            ('new', 'New analysis', self.start_new_analysis, 'success'),
            ('prepare', 'Prepare new data', self.prepare_new_data_pressed, 'success'),
            ('done', 'All done', self.all_done, 'success'),
            ('export', 'Export to pdf', self.export_to_pdf, 'success'),
            ('close', 'Close BringOrder', self.no_export, 'success')
        ]

        return button_list
    
    def new_analysis_view(self):
        """Display buttons to start a new analysis or prepare new data for analysis"""
        grid = widgets.HBox([
            self.buttons['new'],
            self.buttons['prepare'],
            self.buttons['done']
        ])
        display(grid)
    
    def all_done(self, _=None):
        """Button function to display the export/close phase."""
        grid = widgets.HBox([
            self.buttons['export'],
            self.buttons['close']
        ])
        clear_output(wait=True)
        display(grid)

    def start_new_analysis(self, _=None):
        """Starts new analysis with old data and the same BringOrder object."""
        clear_output(wait=True)
        self.next_step[0] = 'start_analysis'

    def prepare_new_data_pressed(self, _=None):
        """Starts new analysis with importing new data, creates new BringOrder object."""
        clear_output(wait=True)
        self.next_step[0] = 'new_data'

    def export_to_pdf(self, _=None):
        """Button function to export the notebook to pdf."""
        clear_output(wait=True)
        display(Javascript('print()'))
        self.next_step[0] = 'exit'

    def no_export(self, _=None):
        """Button function to close widgets without exporting."""
        self.next_step[0] = 'exit'

    def __repr__(self):
        return ''
    