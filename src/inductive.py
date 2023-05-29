from ipywidgets import widgets
from IPython.display import display

class Inductive:
    """_summary_
    """
    def __init__(self, bogui):
        """_summary_

        Args:
            bogui (_type_): _description_
        """
        self.cntr = widgets.Layout(display='flex',
                                   align_items='center',
                                   flex_flow='row',
                                   width='100%')
        self.bogui = bogui
        self.__init_buttons()

    def __init_buttons(self):
        """intializes buttons used by Inductive Analysis"""
        self.add_code = self.bogui.create_button("Add code cell", self.add_code_line, 'warning')
        self.ready = self.bogui.create_button("Ready", self.ready_button, 'primary')

    def start_inductive(self, _=None):
        """_summary_

        Args:
            _ (_type_, optional): _description_. Defaults to None.
        """
        buttons = widgets.HBox(children=[self.add_code, self.ready],
                               layout=self.cntr)
        display(buttons)

    def ready_button(self, _=None):
        """ Summary """
        self.ready.disabled=True
        self.add_code.disabled=True
        label = widgets.Label(value="Explain what you observed:")
        evaluation = widgets.Textarea(value='',layout={'width': '80%'})
        display(widgets.HBox([label,evaluation]))

    def add_code_line(self, _=None):
        ''' This method opens new code cell in Jupyter Notebook'''
        self.bogui.create_code_cell()
