''' Summary '''
import os
import sys
class_dir = os.path.dirname(os.path.realpath(__file__)) # directory of the class
sys.path.insert(1, class_dir)   #insert directory of the class into path.

from ipywidgets import widgets
from IPython.display import display
from bogui import BOGui
from inductive import Inductive
from deductive import Deductive

class BringOrder():
    ''' Summary '''
    def __init__(self):
        self.bogui = BOGui()
        self.new_analysis_button = self.bogui.create_button("New Analysis", self.bring_order)
        self.deduct = self.bogui.create_button("Deductive analysis", self.deductive)
        self.induct = self.bogui.create_button("Inductive analysis", self.inductive)
        self.bring_order()


    def bring_order(self, _=None):
        """_summary_

        Args:
            _ (_type_, optional): _description_. Defaults to None.
        """
        self.new_analysis_button.disabled=True
        self.deduct.disabled=False
        self.induct.disabled=False
        buttons = widgets.HBox(children=[self.deduct, self.induct])
        display(buttons)


    def deductive(self, _):
        """_summary_

        Args:
            _ (_type_): _description_
        """
        new_hypo = Deductive(1, self.bogui)
        new_hypo.start_deductive_analysis()
        self.new_analysis_button.disabled=False
        self.new_analysis()


    def inductive(self, _):
        """_summary_

        Args:
            _ (_type_): _description_
        """
        new_inductive = Inductive(1, self.bogui)
        new_inductive.start_inductive()


    def new_analysis(self, _=None):
        """_summary_

        Args:
            _ (_type_, optional): _description_. Defaults to None.
        """
        button = widgets.HBox(children=[self.new_analysis_button])
        self.deduct.disabled=True
        self.induct.disabled=True
        display(button)
