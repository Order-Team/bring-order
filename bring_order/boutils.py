"""Helpful Javascript methods"""
from IPython.display import display, Javascript


class BOUtils:
    """Helpful Javascript methods"""
    def __init__(self):
        """Class constructor"""
        pass

    def create_code_cells(self, how_many):
        """Creates n code cells below the current cell"""
        for _ in range(how_many):
            command = 'IPython.notebook.insert_cell_below("code")'
            display(Javascript(command))

    def clear_code_cells_below(self, how_many):
        """Clears the given number of code cells starting from given index"""
        command = f'''
        var first_cell = IPython.notebook.get_selected_index() + 1;
        var cells = IPython.notebook.get_cells().reverse();
        cells.forEach(function(cell) {{
                var index = IPython.notebook.find_cell_index(cell);
                if(index >= first_cell && index < first_cell + {how_many}) {{
                    IPython.notebook.delete_cell(index);
                }}
        }});
        '''
        display(Javascript(command))
        self.create_code_cells(how_many)

    def delete_cell(self, cell_count):
        """Deletes code cell with given index"""
        command = f'''
        var first_index = IPython.notebook.get_selected_index();
        var last_index = first_index + {cell_count};
        const cells = IPython.notebook.get_cells();
        IPython.notebook.delete_cell(last_index);
        '''
        display(Javascript(command))

    def run_cells(self, cell_count):
        """Runs cells from first to last index"""
        command = f'''
        var first_index = IPython.notebook.get_selected_index() + 1;
        var last_index = first_index + {cell_count};
        IPython.notebook.execute_cell_range(first_index, last_index);
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
