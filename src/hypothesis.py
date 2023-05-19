from ipywidgets import widgets
from IPython.display import display

class Hypothesis:
    def __init__(self):
        style = {'description_width':'initial'}
        self.hypothesis = widgets.Text(value='', description='Hypothesis:', style=style)
        self.null_hypothesis = widgets.Text(value='', description='Null hypothesis:', style=style)
        save_button, clear_button = self._initialize_buttons()
        self.view1 = widgets.VBox(
            [self.hypothesis,
             self.null_hypothesis,
             widgets.HBox([save_button, clear_button])])

    def _clear_button_clicked(self, _=None):
        self.hypothesis.value = ''
        self.null_hypothesis.value = ''

    def _save_button_clicked(self, _=None):
        self.hypothesis = f'Hypothesis: {self.hypothesis.value}'
        self.null_hypothesis = f'Null hypothesis: {self.null_hypothesis.value}'
        self.view1.close()
        print(self.hypothesis)
        print(self.null_hypothesis)

    def _initialize_buttons(self):
        save_button = widgets.Button(description='Save')
        clear_button = widgets.Button(description='Clear')
        save_button.on_click(self._save_button_clicked)
        clear_button.on_click(self._clear_button_clicked)
        print(save_button)
        print(type(save_button))
        print(clear_button)
        print(type(clear_button))

        return save_button, clear_button

    # User should call this method to set the hypotheses
    def set_hypothesis(self):
        display(self.view1)
        return True

instance = Hypothesis()
instance.set_hypothesis()
