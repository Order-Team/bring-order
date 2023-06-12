"""Helpful Javascript methods"""
from IPython.display import display, Javascript


class BOUtils:
    """Helpful Javascript methods"""
    def __init__(self):
        """Class constructor"""

    def create_code_cells_below(self, how_many):
        """Creates the given number of code cells below the current cell"""
        for _ in range(how_many):
            command = 'IPython.notebook.insert_cell_below("code")'
            display(Javascript(command))

    def create_markdown_cells_below(self, how_many):
        """Creates the given number of code cells below the current cell"""
        for _ in range(how_many):
            command = 'IPython.notebook.insert_cell_below("markdown")'
            display(Javascript(command))

    def create_code_cells_at_bottom(self, how_many):
        """Creates the given number of code cells at the bottom of notebook"""
        for _ in range(how_many):
            command = 'IPython.notebook.insert_cell_at_bottom("code")'
            display(Javascript(command))

    def create_markdown_cells_at_bottom(self, how_many, text=''):
        """Creates the given number of markdown cells at the bottom of notebook
        
        Args:
            how_many (int): the number of cells to be opened
            text (str): default text to be shown in the new cells
        """
        for _ in range(how_many):
            command = f'''
            var cell = IPython.notebook.insert_cell_at_bottom("markdown");
            cell.set_text("{text}");
            '''
            display(Javascript(command))

    def create_code_and_observation_cells(self, how_many):
        """Creates new code and markdown cells on top of each other.
        
        Args:
            how_many (int): the number of cell pairs to be opened
        """
        for _ in range(how_many):
            command = '''
            IPython.notebook.insert_cell_at_bottom("code");
            var markdown = IPython.notebook.insert_cell_at_bottom("markdown");
            markdown.set_text("### Observations");
            '''
            display(Javascript(command))

    def clear_code_and_observation_cells(self, how_many):
        """Clears the given number of code and observation cells below the active cell"""
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

        self.create_code_and_observation_cells(how_many//2)

    def clear_code_cells_below(self, how_many):
        """Clears the given number of code cells below the active cell"""
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
        self.create_code_cells_at_bottom(how_many)

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
        """Runs cells below the active cell.
        
        Args:
            cell_count (int): the number of cells to be run
        """
        command = f'''
        var first_index = IPython.notebook.get_selected_index() + 1;
        var last_index = first_index + {cell_count};
        IPython.notebook.execute_cell_range(first_index, last_index);
        '''
        display(Javascript(command))

    def create_and_execute_code_cell(self, code=''):
        """Creates a new cell at the bottom with given code and runs it"""
        command = f'''
        var code = IPython.notebook.insert_cell_at_bottom("code");
        code.set_text("{code}");
        Jupyter.notebook.execute_cells([-1]);
        '''
        display(Javascript(command))
