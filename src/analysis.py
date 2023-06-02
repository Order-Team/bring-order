from ipywidgets import widgets
from IPython.display import display
from bo_utils import BOUtils
from deductive import Deductive
from inductive import Inductive


class Analysis:
    """Class that starts deductive or inductive analysis according to user's choise"""
    def __init__(self, start_cell):
        """Class constructor.
        
        Args:
            start_cell (int): the index of the notebook cell where the method is called
        """
        self.utils = BOUtils()
        self.deductive = Deductive(start_cell)
        self.inductive = Inductive(start_cell)
        self.deductive_button = self.utils.create_button(
            desc='Deductive',
            command=self.start_deductive_analysis)
        self.inductive_button = self.utils.create_button(
            desc='Inductive',
            command=self.start_inductive_analysis)

    def start_analysis(self):
        """Shows buttons"""
        display(widgets.HBox([self.deductive_button, self.inductive_button]))

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
        