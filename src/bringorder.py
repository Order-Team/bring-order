import os
import sys
wd = os.getcwd()
class_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, class_dir)

from ipywidgets import widgets
from IPython.display import display
from bogui import BOGui
from deductive import Deductive
from inductive import Inductive

from boutils import BOUtils

class BringOrder:
    """Main class"""
    def __init__(self, start_cell):
        """Class constructor"""
        self.start_cell = start_cell
        
        #Testing set_cell_idx, only logs current cell index for now
        self.boutils = BOUtils()
        self.boutils.set_cell_idx()

        self.bogui = BOGui()
        self.deductive = Deductive(start_cell)
        self.inductive = Inductive(start_cell)
        self.deductive_button = self.bogui.create_button(
            desc='Deductive',
            command=self.start_deductive_analysis)
        self.inductive_button = self.bogui.create_button(
            desc='Inductive',
            command=self.start_inductive_analysis)
        self.bring_order()

    def close_buttons(self):
        """Hides buttons"""
        self.deductive_button.close()
        self.inductive_button.close()

    def start_deductive_analysis(self, _=None):
        """Starts deductive analysis"""
        self.inductive = False
        self.close_buttons()
        self.deductive.start_deductive_analysis()

    def start_inductive_analysis(self, _=None):
        """Starts inductive analysis"""
        self.deductive = False
        self.close_buttons()
        self.inductive.start_inductive_analysis()

    def bring_order(self):
        display(widgets.HBox([self.deductive_button, self.inductive_button]))

    def __repr__(self):
        return 'New Analysis'
