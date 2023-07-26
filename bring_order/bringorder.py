"""Main class"""
import os
import sys
import time
from ipywidgets import widgets
from IPython.display import display
import pandas as pd
from jupyter_ui_poll import ui_events

wd = os.getcwd()
class_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, class_dir)
from bogui import BOGui
from bodi import Bodi
from boutils import BOUtils
from deductive import Deductive
from inductive import Inductive


class BringOrder:
    """Main class"""
    def __init__(self):
        """Class constructor"""
        self.boutils = BOUtils()
        self.bogui = BOGui()
        self.deductive = None
        self.inductive = None
        self.deductive_button = None
        self.inductive_button = None
        # next_step is passed on to classes and used to track
        # which ui module to run next.
        self.next_step = [None]
        self.bodi = Bodi(
            self.boutils,
            self.bogui,
            self.next_step)
        self.bring_order()

    def create_deductive_button(self):
        """Creates deductive button"""
        next_step = self.next_step
        def command(self):
            next_step[0] = 'deductive_analysis'
        button = self.bogui.create_button(
            desc='Test hypothesis',
            command=command)

        return button

    def create_inductive_button(self):
        """Creates inductive button"""
        next_step = self.next_step
        def command(self):
            next_step[0] = 'inductive_analysis'
        button = self.bogui.create_button(
            desc='Explore data',
            command=command)

        return button

    def close_buttons(self):
        """Hides buttons"""
        self.deductive_button.close()
        self.inductive_button.close()

    def start_deductive_analysis(self, _=None):
        """Starts deductive analysis"""

        self.close_buttons()
        if not hasattr(self, 'data_limitations'):
            self.data_limitations = self.bodi.data_limitations
        self.deductive.data_limitations = self.bodi.data_limitations
        return self.deductive.start_deductive_analysis()

    def start_inductive_analysis(self, _=None):
        """Starts inductive analysis"""
        self.close_buttons()
        return self.inductive.start_inductive_analysis()

    def bring_order(self):
        """Runs the ui modules"""
        # The different ui functions are run through a helper function
        # that returns the name of the next function to be executed.
        # First, the data import function:
        next = self.get_next(self.bodi.bodi)
        # Main analysis loop:
        while next == 'start_analysis':
            next = self.get_next(self.start_analysis)
            # Branching to deductive/inductive:    
            if next == 'deductive_analysis':
                next = self.get_next(self.start_deductive_analysis)
            elif next == 'inductive_analysis':
                next = self.get_next(self.start_inductive_analysis)
        # Close:
        if next == 'exit':
            self.boutils.delete_cell_from_current(0)
        # Import new data set:
        elif next == 'new_data':
            self.boutils.execute_cell_from_current(1, 'BringOrder()')

    def get_next(self, function):
        """Runs a function, pauses execution until next_step is updated and then returns it.
        
        Args:
            function: a function to be executed
        Returns:
            next: name of the function to be executed after this"""
        function()
        with ui_events() as ui_poll:
            while self.next_step[0] == None:
                ui_poll(10)
                time.sleep(0.1)
        next = str(self.next_step[0])
        self.next_step[0] = None
        return next

    def start_analysis(self):
        """Starts analysis phase"""
        self.deductive = Deductive(
            self.bogui,
            self.boutils,
            self.next_step
        )
        self.inductive = Inductive(
            self.bogui,
            self.boutils,
            self.next_step
        )
        self.deductive_button = self.create_deductive_button()
        self.inductive_button = self.create_inductive_button()
        display(widgets.HBox([self.deductive_button, self.inductive_button]))

    def __repr__(self):
        return ''
    