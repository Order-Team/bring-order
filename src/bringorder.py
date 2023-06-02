import os
import sys
wd = os.getcwd()
class_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, class_dir)

from analysis import Analysis


class BringOrder:
    """Main class"""
    def __init__(self):
        """Class constructor"""
        self.analyses = []

    def new_analysis(self, start_cell):
        """Starts new analysis.

        Args:
            start_cell (int): the index of the notebook cell where the method is called
        """
        current_cell = start_cell
        new_analysis = Analysis(current_cell)
        self.analyses.append(new_analysis)
        new_analysis.start_analysis()
