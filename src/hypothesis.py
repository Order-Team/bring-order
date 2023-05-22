from ipywidgets import widgets
from IPython.display import display

class Hypothesis:
    """_summary_
    """
    def __init__(self):
        self.hypothesis_label = widgets.Label(value='Hypothesis:',
                                              layout=widgets.Layout(justify_content='flex-end'))
        self.null_hypothesis_label = widgets.Label(value='Null hypothesis:',
                                                layout=widgets.Layout(justify_content='flex-end'))
        self.hypothesis = widgets.Text(value='')
        self.null_hypothesis = widgets.Text(value='')
        save_button, clear_button = self.initialize_buttons()
        grid = widgets.GridspecLayout(3, 3, height='auto')
        grid[0, 0] = self.hypothesis_label
        grid[0, 1] = self.hypothesis
        grid[1, 0] = self.null_hypothesis_label
        grid[1, 1] = self.null_hypothesis
        grid[2, 1] = widgets.HBox([save_button, clear_button])
        self.view1 = grid


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
        save_button = widgets.Button(description='Save', button_style='success')
        clear_button = widgets.Button(description='Clear', button_style='info')
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
