''' Summary '''
from ipywidgets import widgets
from IPython.display import display, Javascript
from boutils import BOUtils

class Inductive:
    """_summary_
    """
    def __init__(self, start_cell, bogui):
        """_summary_

        Args:
            bogui (_type_): _description_
        """
        self.first_cell_index = start_cell
        self.cell_count = 1
        self.utils = BOUtils()
        self.bogui = bogui
        self.add_code = self.bogui.create_button("Add code cell", self.add_code_line, 'warning')
        self.delete = self.bogui.create_button("Delete last cell", self.delete_last_cell, "danger")
        self.run = self.bogui.create_button("Run code", self.ready_button, 'primary')
        self.clean_code = self.bogui.create_button("Clean code blocks",
                                                   self.clean_code_button, 'danger')
        self.new_analysis_button = self.bogui.create_button('New analysis', self.start_new_analysis)
        self.conclusion = None
        self.notes = self.bogui.create_text_area()



    def start_inductive(self, _=None):
        """_summary_

        Args:
            _ (_type_, optional): _description_. Defaults to None.
        """
        buttons = widgets.HBox(children=[self.add_code, self.delete, self.run, self.clean_code])
        display(buttons)

    def ready_button(self, _=None):
        """ Summary """

        self.run.disabled=True
        self.add_code.disabled=True
        self.utils.run_cells(self.first_cell_index+1, self.first_cell_index+self.cell_count)
        if self.conclusion:
            self.conclusion.close()

        label = self.bogui.create_label(value="Explain what you observed:")

        self.conclusion = widgets.VBox([widgets.HBox([label, self.notes]),
                    self.new_analysis_button])
        display(self.conclusion)


    def start_new_analysis(self, _=None):
        """Button function"""
        self.save_results()

    def clean_code_button(self, _=None):
        """ Summary """
        display(Javascript(
            """
            var cells = IPython.notebook.get_cells().map(function(cell) {
                if (cell.cell_type == "code") {
                    var index = IPython.notebook.find_cell_index(cell);
                    if (index != 0) {
                        IPython.notebook.delete_cell(index);
                    }
                }
            });
            """
        ))
        self.bogui.create_code_cell()
        self.clean_code.disabled=False
        self.run.disabled=False

    def add_code_line(self, _=None):
        """ Summary """
        self.clean_code.disabled=False
        self.run.disabled=False
        self.bogui.create_code_cell()

    def delete_last_cell(self, _=None):
        """Button function"""
        self.utils.delete_cell(
            self.first_cell_index+self.cell_count-1)
        self.cell_count -= 1

    def save_results(self):
        """Prints notes"""
        text = f'''
            Inductive Analysis\n
            Notes:\n
            {self.notes.value}
            '''
        print(text)
