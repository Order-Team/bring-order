from ipywidgets import widgets
from IPython.display import display

class Hypotheses:
    def __init__(self):
        self.hypotheses = widgets.Text(value='', description='Hypotheses:')
        self.null_hypotheses = widgets.Text(value='', description='Null hypotheses:')
        save_button, clear_button = self._initialize_buttons()
        self.view1 = widgets.VBox(
            [self.hypotheses,
             self.null_hypotheses,
             widgets.HBox([save_button, clear_button])])

    def _clear_button_clicked(self, _):
        self.hypotheses.value = ''
        self.null_hypotheses.value = ''

    def _save_button_clicked(self, _):
        self.hypotheses = f'Hypotheses: {self.hypotheses.value}'
        self.null_hypotheses = f'Null hypotheses: {self.null_hypotheses.value}'
        self.view1.close()
        print(self.hypotheses)
        print(self.null_hypotheses)

    def _initialize_buttons(self):
        save_button = widgets.Button(description='Save')
        clear_button = widgets.Button(description='Clear')
        save_button.on_click(self._save_button_clicked)
        clear_button.on_click(self._clear_button_clicked)

        return save_button, clear_button

    # User should call this method to set the hypotheses
    def set_hypotheses(self):
        display(self.view1)
