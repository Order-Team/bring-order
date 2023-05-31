from ipywidgets import widgets
from IPython.display import display, Javascript, HTML
from IPython import get_ipython

class Hypothesis:
    """ Class responsible for hypothesis construction.
    """
    def __init__(self):
        """ Class constructor. Creates a new hypothesis construction view.
        """
        self.current_shell=0
        self.hypothesis_label = widgets.Label(value='Hypothesis:',
                                              layout=widgets.Layout(justify_content='flex-end'))
        self.null_hypothesis_label = widgets.Label(value='Null hypothesis:',
                                                layout=widgets.Layout(justify_content='flex-end'))
        self.hypothesis = widgets.Text(value='')
        self.null_hypothesis = widgets.Text(value='')
        save_button, clear_button, ready_button, clean_code_button = self.initialize_buttons()
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

        self.evaluation_action = widgets.HTML(
            value= 'Ready to run your code to check your hypothesis?',
            style = {'font_size': '15px'})
        grid2 = widgets.GridspecLayout(3, 3, height='auto', wifth="500px", grid_gap="0px")
        grid2[0, 0] = self.evaluation_action
        grid2[1, 0] = widgets.HBox([ready_button, clean_code_button])
        self.view2 = grid2

        self.radiobuttons = widgets.RadioButtons(
         options=[],
         description='What happended?',
         disabled=False,
         font_size ="20px"

        )
        self.view3 = self.radiobuttons

    def clear_button_clicked(self, _=None):
        """ This method empties the values in variables bound to the current instance.

        Args:
            _ (Button): Clear button.
        """
        self.hypothesis.value = ''
        self.null_hypothesis.value = ''
        self.field1_error_message.value = ''
        self.field2_error_message.value = ''

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
                self.field1_error_message.value = ''
                self.field2_error_message.value = 'Null hypothesis missing'
                raise ValueError(self.field2_error_message.value)

            if not self.hypothesis.value:
                self.field1_error_message.value = 'Hypothesis missing'
                self.field2_error_message.value = ''
                raise ValueError(self.field1_error_message.value)

            self.radiobuttons.options = [self.hypothesis.value, self.null_hypothesis.value]
            display_hypothesis = f'Hypothesis: {self.hypothesis.value}'
            display_null_hypothesis = f'Null hypothesis: {self.null_hypothesis.value}'
            self.view1.close()
            print(display_hypothesis)
            print(display_null_hypothesis)
            self.create_five_code_cells()
            self.evaluation()

        except ValueError:
            pass

    def ready_button_clicked(self, _=None):
        """_summary_

        Args:
            _ (_type_, optional): _description_. Defaults to None.
        """

        #3 add code her to run code in cells?
        display(self.view3)

    def clean_code_button_clicked(self, _=None):
        """_summary_

        Args:
            _ (_type_, optional): _description_. Defaults to None.
        """
        n = self.current_shell
        js_code = """
        var cells = IPython.notebook.get_cells();
        cells.forEach(function(cell) {{
                var index = IPython.notebook.find_cell_index(cell);
                if(index >= {0}){{
                    IPython.notebook.delete_cell(index);
                }}
        }})
        ;
        """.format(n)
        display(Javascript(js_code))
        self.create_five_code_cells()


    def create_five_code_cells(self):
        '''Create new empty code cell'''
        for _ in range(0,5):
            display(Javascript("""
            IPython.notebook.insert_cell_below('code')
            """))


    def evaluation(self):
        """_summary_
        """
        self.current_shell = get_ipython().execution_count
        display(self.view2)
        #print(self.current_shell)

    def initialize_buttons(self):
        """ This method initializes the save- and clear buttons.

        Returns:
            save_button: Button which saves the user input.
            clear_button: Button which clears the user input.
        """
        save_button = widgets.Button(description='Save', button_style='success')
        clear_button = widgets.Button(description='Clear', button_style='info')
        ready_button = widgets.Button(description='Ready', button_style='primary')
        clean_code_button = widgets.Button(description='Clean code blocks above',
                                            button_style='danger')
        save_button.on_click(self.save_button_clicked)
        clear_button.on_click(self.clear_button_clicked)
        ready_button.on_click(self.ready_button_clicked)
        clean_code_button.on_click(self.clean_code_button_clicked)

        return save_button, clear_button, ready_button, clean_code_button

    def set_hypothesis(self):
        """ This method displays the view for constructing the hypothesis.
        """
        display(self.view1)

#instance = Hypothesis()
#instance.set_hypothesis()
