"""Main class"""
import os
import sys
from ipywidgets import widgets
from IPython.display import display, Javascript

wd = os.getcwd()
class_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, class_dir)
from bogui import BOGui
from bodi import Bodi
from boutils import BOUtils


class BringOrder:
    """Main class"""
    def __init__(self, data_import=True):
        """Class constructor"""
        self.boutils = BOUtils()
        self.bogui = BOGui()
        self.deductive_button = self.bogui.create_button(
            desc='Deductive',
            command=self.start_deductive_analysis)
        self.inductive_button = self.bogui.create_button(
            desc='Inductive',
            command=self.start_inductive_analysis)
        self.bodi = Bodi(
            self.boutils,
            self.bogui,
            self.start_analysis)
        if data_import:
            self.bring_order()
        else:
            self.start_analysis()

    def close_buttons(self):
        """Hides buttons"""
        self.deductive_button.close()
        self.inductive_button.close()

    def start_deductive_analysis(self, _=None):
        display(
            Javascript('IPython.notebook.kernel.execute("from bring_order.deductive import Deductive")')
        )
        self.close_buttons()
        self.boutils.create_markdown_cells_at_bottom(1, "## Deductive analysis")
        if not (hasattr(self, 'data_limitations')):
            self.data_limitations = self.bodi.data_limitations.value
        self.boutils.create_and_execute_code_cell(f'Deductive(data_limitations="{self.data_limitations}")')

    def start_inductive_analysis(self, _=None):
        """Starts inductive analysis"""
        display(
            Javascript('IPython.notebook.kernel.execute("from bring_order.inductive import Inductive")')
        )
        self.close_buttons()
        self.boutils.create_markdown_cells_at_bottom(1, "## Inductive analysis")
        self.boutils.create_and_execute_code_cell('Inductive()')

    def bring_order(self):
        """Starts data import phase"""
        self.boutils.create_markdown_cells_at_bottom(1, "# New analysis")
        self.bodi.bodi()
    
    def start_analysis(self):
        display(widgets.HBox([self.deductive_button, self.inductive_button]))

    def __repr__(self):
        return ''
