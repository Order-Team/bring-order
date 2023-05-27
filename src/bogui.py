import base64
from ipywidgets import widgets
from IPython.display import display
from IPython.display import Javascript
from IPython.core.getipython import get_ipython
from hypothesis import Hypothesis

class BOGui:
    """Bring order GUI"""
    def __init__(self):
        self.cntr = widgets.Layout(display='flex', align_items='center', flex_flow='row', width='100%')
        self.__init_buttons()
        self.bring_order()

    def create_button(self, desc: str, command, style="success", tooltip=''):
        """ Method for creating buttons.
    
        Args:
            desc: Name/description of the button.
            command: Method executed by the button on click
            style: Style of the button : success', 'info', 'warning', 'danger' or ''
            tooltip: String, that is shown when cursor hovering over button.
    
        Returns:
            button initialized by given arguments.
    """
        newbutton = widgets.Button(description=desc, button_style=style, tooltip=tooltip)
        newbutton
        newbutton.on_click(command)
        return newbutton
    
    def __init_buttons(self):
        """intializes buttons used by BOGui"""
        self.new_analysis_button = self.create_button("New Analysis", self.bring_order, "success")
        self.deduct = self.create_button("Deductive analysis", self.deductive, "success")
        self.induct = self.create_button("Inductive analysis", self.inductive, "success")
        
        
    def deductive(self, _):
        new_hypo = Hypothesis()
        new_hypo.set_hypothesis()
        self.new_analysis_button.disabled=False
        self.new_analysis()

    def inductive(self, _):
        print("Here will be a call for inductive class...")
        self.new_analysis_button.disabled=False
        self.new_analysis()
        self.create_code_cell()
        self.create_markdown_cell()

        
    def new_analysis(self, _=None):
        #self.new_analysis = self.create_button("New Analysis", self.bring_order, "success")
        button = widgets.HBox(children=[self.new_analysis_button], layout=self.cntr)
        self.deduct.disabled=True
        self.induct.disabled=True
        display(button)

    def bring_order(self, _=None):
        self.new_analysis_button.disabled=True
        self.deduct.disabled=False
        self.induct.disabled=False
        buttons = widgets.HBox(children=[self.deduct, self.induct], layout=self.cntr)
        display(buttons)

    def create_code_cell(self):
        display(Javascript("""
        IPython.notebook.insert_cell_below('code')
        """))
    
    def create_markdown_cell(self):
        display(Javascript("""
        IPython.notebook.insert_cell_below('markdown')
        """))

BOGui()
