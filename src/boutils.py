from ipywidgets import widgets
from IPython.display import display, Javascript


class BOUtils:
    """Helpful Javascript methods"""
    def __init__(self):
        """Class constructor"""
        pass

    def create_code_cells(self, n):
        """Creates n code cells below the current cell"""
        for _ in range(n):
            command = 'IPython.notebook.insert_cell_below("code")'
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
        self.create_code_cells(how_many)

    def delete_cell(self, index):
        """Deletes code cell with given index"""
        command = f'''
        const cells = IPython.notebook.get_cells();
        IPython.notebook.delete_cell({index});
        '''
        display(Javascript(command))

    def run_cells(self, first_index, last_index):
        """Runs cells from first to last index"""
        command = f'''
        IPython.notebook.execute_cell_range({first_index}, {last_index});
        '''
        display(Javascript(command))

    def create_and_execute_code_cell(self, code=''):
        """Creates a new cell at the bottom with given code and runs it"""
        command = f'''
        var code = IPython.notebook.insert_cell_at_bottom('code');
        code.set_text("{code}");
        Jupyter.notebook.execute_cells([-1]);
        '''
        display(Javascript(command))

    # Todo: Figure out how to access the updated cell_idx value in the same code block.
    # As it is, Notebook seems to execute the full Python code before Javascript has a
    # chance to set cell_idx via kernel.execute().
    def set_cell_idx(self):
        """Sets cell_idx to the index of the code cell in which this function is called"""
        command = """
        var cell_idx = IPython.notebook.get_selected_index();
        IPython.notebook.kernel.execute(`
            cell_idx = ${cell_idx}
            `);            
            console.log('Current cell index: ' + cell_idx)
        """
        display(Javascript(command))

