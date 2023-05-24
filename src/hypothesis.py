from ipywidgets import widgets
from IPython.display import display

class Hypothesis:
    """ Class responsible for hypothesis construction.
    """
    def __init__(self):
        """ Class constructor. Creates a new hypothesis construction view.
        """
        self.hypothesis_label = widgets.Label(value='Hypothesis:',
                                              layout=widgets.Layout(justify_content='flex-end'))
        self.null_hypothesis_label = widgets.Label(value='Null hypothesis:',
                                                layout=widgets.Layout(justify_content='flex-end'))
        self.hypothesis = widgets.Text(value='')
        self.null_hypothesis = widgets.Text(value='')
        save_button, clear_button = self.initialize_buttons()
        self.field1_error_message = widgets.HTML(value='',
                                                style = {'text_color': 'red', 'font_size': '12px'})
        self.field2_error_message = widgets.HTML(value= '',
                                                style = {'text_color': 'red', 'font_size':'12px'})
        grid = widgets.GridspecLayout(5, 3, height='auto', grid_gap="0px")
        grid[0, 0] = self.hypothesis_label
        grid[0, 1] = self.hypothesis
        grid[1, 1] = self.field1_error_message
        grid[2, 0] = self.null_hypothesis_label
        grid[2, 1] = self.null_hypothesis
        grid[3, 1] = self.field2_error_message
        grid[4, 1] = widgets.HBox([save_button, clear_button])
        self.view1 = grid


    def clear_button_clicked(self, _=None):
        """ This method empties the values in variables bound to the current instance.

        Args:
            _ (Button): Clear button.
        """
        self.hypothesis.value = ''
        self.null_hypothesis.value = ''

    def save_button_clicked(self, _=None):
        """ This method does input validation on the fields, 
            saves the values to variables bound to the current instance and 
            displays them to the user.

        Args:
            _ (Button): Save button.
        """
        try:
            if not self.hypothesis.value and not self.null_hypothesis.value:
                self.field1_error_message.value = 'Hypothesis missing'
                self.field2_error_message.value = 'Null hypothesis missing'
                raise ValueError(f"{self.field1_error_message.value}" \
                                 "and {self.field2_error_message.value}")
            if not self.null_hypothesis.value:
                self.field2_error_message.value = 'Null hypothesis missing'
                raise ValueError(self.field2_error_message.value)
            if not self.hypothesis.value:
                self.field1_error_message.value = 'Hypothesis missing'
                raise ValueError(self.field1_error_message.value)

            self.hypothesis = f'Hypothesis: {self.hypothesis.value}'
            self.null_hypothesis = f'Null hypothesis: {self.null_hypothesis.value}'
            self.view1.close()
            print(self.hypothesis)
            print(self.null_hypothesis)

        except ValueError:
            pass

    def initialize_buttons(self):
        """ This method initializes the save- and clear buttons.

        Returns:
            save_button: Button which saves the user input.
            clear_button: Button which clears the user input.
        """
        save_button = widgets.Button(description='Save', button_style='success')
        clear_button = widgets.Button(description='Clear', button_style='info')
        save_button.on_click(self.save_button_clicked)
        clear_button.on_click(self.clear_button_clicked)
        return save_button, clear_button

    def set_hypothesis(self):
        """ This method displays the view for constructing the hypothesis.
        """
        display(self.view1)

instance = Hypothesis()
instance.set_hypothesis()
