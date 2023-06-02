''' Helper functions for Bring Order '''
from ipywidgets import widgets
from IPython.display import display, Javascript

class BOUtils:
    """General methods for creating widgets"""
    def __init__(self):
        """Class constructor"""
        pass

    def run_cells(self, first_index, last_index):
        """Rund cells from first to last index"""
        command = f'''
        IPython.notebook.execute_cell_range({first_index}, {last_index});
        '''
        display(Javascript(command))

    def delete_cell(self, index):
        """Deletes code cell with given index"""
        command = f'''
        const cells = IPython.notebook.get_cells();
        IPython.notebook.delete_cell({index});
        '''
        display(Javascript(command))


    def clear_code_cells_below(self, first_cell, how_many):
        """Clears the given number of code cells starting from given index"""
        command = f'''
        var cells = IPython.notebook.get_cells().reverse();
        cells.forEach(function(cell) {{
                var index = IPython.notebook.find_cell_index(cell);
                if(index >= {first_cell} && index < {first_cell+how_many}) {{
                    IPython.notebook.delete_cell(index);
                }}
        }});
        '''
        display(Javascript(command))
