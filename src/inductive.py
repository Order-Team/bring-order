from ipywidgets import widgets
from IPython.display import display

class Inductive:
    def __init__(self, bogui):
        self.cntr = widgets.Layout(display='flex', align_items='center', flex_flow='row', width='100%')
        self.bogui = bogui
        self.__init_buttons()

    def __init_buttons(self):
        """intializes buttons used by Inductive Analysis"""
        self.add_code = self.bogui.create_button("Add code line", self.add_code_line, "success")
        self.ready = self.bogui.create_button("Ready", self.ready_button, "success")
    
    def start_inductive(self, _=None):      
        buttons = widgets.HBox(children=[self.add_code, self.ready], layout=self.cntr)
        display(buttons)

    def ready_button(self, _=None):
        """ This method open comment field for explanations.
        """
        self.bogui.create_markdown_cell()
    
    def add_code_line(self, _=None):
        ''' This method open new code line'''
        self.bogui.create_code_cell()

