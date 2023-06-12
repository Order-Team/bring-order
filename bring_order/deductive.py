"""Deductive class"""
from ipywidgets import widgets
from IPython.display import display
from bogui import BOGui
from boutils import BOUtils


class Deductive:
    """Class that guides deductive analysis"""
    def __init__(self):
        """Class constructor."""
        self.cell_count = 0
        self.bogui = BOGui()
        self.utils = BOUtils()
        self.hypothesis_input = self.bogui.create_input_field()
        self.empty_hypo_error = self.bogui.create_error_message()
        self.null_input = self.bogui.create_input_field()
        self.empty_null_error = self.bogui.create_error_message()
        self.hypotheses_grid = self.create_hypotheses_grid()
        self.add_cells_int = self.bogui.create_int_text()
        self.confirmed_grid = None
        self.conclusion = None
        self.limitation_prompt = None
        self.start_deductive_analysis()

    def create_hypotheses_grid(self):
        """Creates widgets"""
        hypothesis_label = self.bogui.create_label('Hypothesis:')
        null_label = self.bogui.create_label('Null hypothesis:')
        save_button = self.bogui.create_button(
            desc='Save',
            command=self.check_data_limitations)
        clear_button = self.bogui.create_button(
            desc='Clear',
            command=self.clear_hypotheses,
            style='primary')
        empty = self.bogui.create_placeholder()

        grid = self.bogui.create_grid(
            5,
            2,
            [empty,
             self.empty_hypo_error,
             hypothesis_label,
             self.hypothesis_input,
             null_label,
             self.null_input,
             empty,
             self.empty_null_error,
             empty,
             widgets.HBox(
                [save_button, clear_button])
            ])

        return grid

    def start_deductive_analysis(self, _=None):
        """Button function for deductive analysis"""
        display(self.hypotheses_grid)
        self.hypothesis_input.focus()

    def check_data_limitations(self, _=None):
        """Displays the prompt for the check against data limitations"""
        self.limitation_prompt_text = widgets.HTML(
            'Do the hypotheses fit within the limitations of the data set?' 
            + '<br>TODO: get data limitations from bodi class and print them here')
        valid_hypotheses_button = self.bogui.create_button(
            desc='Yes',
            command=self.valid_hypotheses
        )
        bad_hypotheses_button = self.bogui.create_button(
            desc='No',
            command=self.bad_hypotheses,
            style='warning'
        )
        self.limitation_prompt = widgets.VBox(
            [
            self.limitation_prompt_text, 
            widgets.HBox([
                valid_hypotheses_button, bad_hypotheses_button
                ])
            ]
        )
        display(self.limitation_prompt)
    
    def valid_hypotheses(self, _=None):
        """Closes the data limitation check prompt and calls save_hypotheses()"""
        self.limitation_prompt.close()
        self.save_hypotheses()

    def bad_hypotheses(self, _=None):
        """Closes the data limitation check prompt and calls clear_hypotheses()"""
        # TODO: set some error message for a hypothesis that doesn't fit 
        # data limitations and ask the user for a better one
        self.limitation_prompt.close()
        self.clear_hypotheses()

    def check_hypotheses(self):
        """Checks that hypothesis and null hypothesis are not empty.

        Returns:
            True/False
        """
        if len(self.hypothesis_input.value) > 0 and len(self.null_input.value) > 0:
            return True

        if self.hypothesis_input.value == '':
            self.empty_hypo_error.value = 'Hypothesis missing'
        else:
            self.empty_hypo_error.value = ''

        if self.null_input.value == '':
            self.empty_null_error.value = 'Null hypothesis missing'
        else:
            self.empty_null_error.value = ''

        return False

    def save_hypotheses(self, _=None):
        """Saves hypotheses and displays buttons for running code"""
        if self.check_hypotheses():
            confirmed_hypothesis = self.bogui.create_message(
                value=f'Hypothesis: {self.hypothesis_input.value}')
            confirmed_null = self.bogui.create_message(
                value=f'Null hypothesis: {self.null_input.value}')
            self.confirmed_grid = self.create_confirmed_grid(
                confirmed_hypothesis,
                confirmed_null)
            self.hypotheses_grid.close()
            display(self.confirmed_grid)

    def clear_hypotheses(self, _=None):
        """Button function for resetting hypothesis and null hypothesis inputs"""
        self.hypothesis_input.value = ''
        self.null_input.value = ''
        self.empty_hypo_error.value = ''
        self.empty_null_error.value = ''
        self.hypothesis_input.focus()

    def create_open_cells_button(self):
        """Creates button for opening new code cells for analysis.

        Returns:
            button
        """
        def open_cells(_=None):
            """Button function"""
            self.cell_count += self.add_cells_int.value
            self.utils.create_code_cells_at_bottom(self.add_cells_int.value)

        button = self.bogui.create_button(
            desc='Open cells',
            command=open_cells,
            style='warning')

        return button

    def create_delete_button(self):
        """Creates button for deleting the last code cell

        Returns:
            button
        """
        def delete_last_cell(_=None):
            """Button function"""
            if self.cell_count > 0:
                self.utils.delete_cell(
                    self.cell_count)
                self.cell_count -= 1

        button = self.bogui.create_button(
            desc='Delete last cell',
            command=delete_last_cell,
            style='danger')

        return button

    def create_run_button(self, hypothesis, null_hypothesis):
        """Creates button"""
        def run_cells(_=None):
            """Button function"""
            self.utils.run_cells(
                self.cell_count)

            if self.conclusion:
                self.conclusion.close()

            conclusion_label = self.bogui.create_message(
                value='Accepted hypothesis:')
            conclusion = self.bogui.create_radiobuttons(
                options=[hypothesis.value, null_hypothesis.value])
            new_button = self.create_new_analysis_button(
                hypothesis,
                null_hypothesis,
                conclusion)
            self.conclusion = widgets.AppLayout(
                left_sidebar=conclusion_label,
                center=conclusion,
                footer=new_button)

            display(self.conclusion)

        button = self.bogui.create_button(
            desc='Run cells',
            command=run_cells,
            style='primary')

        return button

    def create_clear_button(self):
        """Creates button"""
        def clear_cells(_=None):
            """Button function"""
            self.utils.clear_code_cells_below(
                self.cell_count)

        button = self.bogui.create_button(
            desc='Clear cells',
            command=clear_cells,
            style='danger')
        return button

    def save_results(self, hypothesis, null_hypothesis, confirmed):
        """Prints results and hides widgets"""
        text = f'''
        Deductive Analysis\n
        {hypothesis.value}\n
        {null_hypothesis.value}\n
        Accepted: {confirmed.value}
        '''
        print(text)
        self.confirmed_grid.close()
        self.conclusion.close()

    def create_new_analysis_button(self, hypo, null, radio):
        """Creates button"""
        def start_new_analysis(_=None):
            """Button function"""
            self.save_results(hypo, null, radio)
            command = 'BringOrder(data_import=False)'
            self.utils.create_and_execute_code_cell(command)

        button = self.bogui.create_button(
            desc='New analysis',
            command=start_new_analysis)

        return button

    def create_confirmed_grid(self, hypothesis, null_hypothesis):
        """Creates widget grid"""
        cell_number_label = self.bogui.create_label(
            'Add code cells for your analysis:')

        open_cells_button = self.create_open_cells_button()
        delete_cell_button = self.create_delete_button()
        run_cells_button = self.create_run_button(hypothesis, null_hypothesis)
        clear_cells_button = self.create_clear_button()

        grid = widgets.GridspecLayout(
            3,
            2,
            justify_items='center',
            width='70%',
            align_items='bottom')
        grid[0, :] = widgets.VBox(
            [hypothesis, null_hypothesis])
        grid[1, 0] = widgets.HBox(
            [cell_number_label, self.add_cells_int])
        grid[1, 1] = widgets.TwoByTwoLayout(
            top_left=open_cells_button,
            bottom_left=run_cells_button,
            top_right=delete_cell_button,
            bottom_right=clear_cells_button)

        return grid

    def __repr__(self):
        return ''
    