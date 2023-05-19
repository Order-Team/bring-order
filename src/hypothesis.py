from ipywidgets import widgets
from IPython.display import display

class Hypothesis:
    """_summary_
    """
    def __init__(self):
        style = {'description_width':'initial'}
        self.hypothesis = widgets.Text(value='', description='Hypothesis:', style=style)
        self.null_hypothesis = widgets.Text(value='', description='Null hypothesis:', style=style)
        save_button, clear_button = self.initialize_buttons()
        self.view1 = widgets.VBox(
            [self.hypothesis,
             self.null_hypothesis,
             widgets.HBox([save_button, clear_button])])

    def clear_button_clicked(self, _=None):
        """_summary_

        Args:
            _ (_type_, optional): _description_. Defaults to None.
        """
        self.hypothesis.value = ''
        self.null_hypothesis.value = ''

    def save_button_clicked(self, _=None):
        """_summary_

        Args:
            _ (_type_, optional): _description_. Defaults to None.
        """
        self.hypothesis = f'Hypothesis: {self.hypothesis.value}'
        self.null_hypothesis = f'Null hypothesis: {self.null_hypothesis.value}'
        self.view1.close()
        print(self.hypothesis)
        print(self.null_hypothesis)

    def initialize_buttons(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        save_button = widgets.Button(description='Save')
        clear_button = widgets.Button(description='Clear')
        save_button.on_click(self.save_button_clicked)
        clear_button.on_click(self.clear_button_clicked)
        return save_button, clear_button

    def set_hypothesis(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        display(self.view1)

instance = Hypothesis()
instance.set_hypothesis()
