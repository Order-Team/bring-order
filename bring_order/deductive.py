"""Deductive class"""
import spacy
import os
#import en_core_web_sm
from ipywidgets import widgets
from IPython.display import display, Javascript, clear_output

class Deductive:
    """Class that guides deductive analysis"""
    def __init__(self, bogui, boutils, next_step):
        """Class constructor
        
        Args:
            bogui (BOGui)
            boutils (BOUtils)
            next_step ([]): State variable that tracks the next step for the program 
        """
        self.cell_count = 0
        self.next_step = next_step
        self.bogui = bogui
        self.boutils = boutils
        self.buttons = self.bogui.init_buttons(self.button_list)
        self.theory_desc = self.bogui.create_text_area('','Theory')
        #List of hypotheses: 0 = hypothesis, 1 = null hypothesis
        self.hypotheses = [
            self.bogui.create_input_field(),
            self.bogui.create_input_field()
        ]
        self.add_cells_int = self.bogui.create_int_text()
        self.conclusion = None
        self.data_limitations = [self.bogui.create_input_field('Data limitations missing')]
        self.result_description = self.bogui.create_text_area('','Results')
        wd = os.getcwd()
        cache_dir=os.getenv("cache_dir", wd)
        model_path="en_core_web_sm/en_core_web_sm-3.6.0"
        self.nlp = spacy.load(os.path.join(cache_dir,model_path))

    @property
    def button_list(self):
        """Buttons for deductive class.

        Returns:
            list of tuples in format (tag: str, description: str, command: func, style: str)
        """

        button_list = [
            ('open', 'Open cells', self.open_cells, 'primary'),
            ('delete', 'Delete last cell', self.delete_last_cell, 'danger'),
            ('save', 'Save and continue', self.submit_theory_and_hypotheses, 'success'),
            ('validate', 'Validate input', self.__validate_theory_and_hypotheses, 'primary'),
            ('clear_hypo', 'Clear hypotheses', self.clear_hypotheses, 'warning'),
            ('yes', 'Yes', self.save_theory_and_hypotheses, 'success'),
            ('no', 'No', self.bad_hypotheses, 'warning'),
            ('run', 'Run cells', self.run_cells, 'warning'),
            ('clear', 'Clear cells', self.clear_cells, 'danger'),
            ('clear_theory', 'Clear theory', self.clear_theory, 'warning'),
            ('save_results', 'Save', self.save_results, 'success')
        ]

        return button_list

    def __create_hypotheses_grid(self, hypo_error='',
                                null_error='',
                                hypo_error_color='red',
                                null_error_color='red'):
        """Creates the view for setting hypotheses
        
        Args:
            empty_hypo_error (str): error message for empty hypothesis, optional
            empty_null_error (str): error message for empty null hypothesis, optional
        """
        grid = widgets.AppLayout(
            header = self.bogui.create_message('Set the hypotheses:'),
            left_sidebar = widgets.VBox([
                self.bogui.create_label('Hypothesis (H1):'),
                self.bogui.create_label('Null hypothesis (H0):')
            ]),
            center = widgets.VBox([
                widgets.HBox([
                    self.hypotheses[0],
                    self.bogui.create_error_message(hypo_error, hypo_error_color)

                ]),
                widgets.HBox([
                    self.hypotheses[1],
                    self.bogui.create_error_message(null_error, null_error_color)

                ]),
                self.buttons['clear_hypo']
            ]),
            footer = widgets.HBox([self.buttons['validate'], self.buttons['save']]),
            pane_widths = [1, 6, 0],
            grid_gap = '18px'
        )

        return grid

    def __create_theory_grid(self, error='', color='red'):
        """Creates the view for summarizing theory
        
        Args:
            error (str): error message, optional
        """
        grid = widgets.AppLayout(
            header=self.bogui.create_message('Describe the theory and insights:'),
            center=widgets.VBox([
                self.theory_desc,
                self.bogui.create_error_message(error, color),
                self.buttons['clear_theory']
            ]),
            pane_widths=[1, 6, 0],
            grid_gap='12px'
        )

        return grid

    def start_deductive_analysis(self, _=None):
        """Button function for deductive analysis"""
        theory_grid = self.__create_theory_grid()
        hypotheses_grid = self.__create_hypotheses_grid()

        clear_output(wait=True)
        display(theory_grid)
        display(hypotheses_grid)
        self.theory_desc.focus()

    def clear_theory(self, _=None):
        """Function for clearing theory and insights"""
        self.theory_desc.value = ''
        self.theory_desc.focus()

    def focus_first_empty(self, input_list):
        """Sets focus to the first widget on the list that has empty value
        
        Args:
            input_list (list): list of input widgets

        Retruns:
            item (widget): the item that was focused (or None if no empty item on the list)
        """
        focused = None
        for item in input_list:
            if item.value == '':
                item.focus()
                focused = item
                break

        return focused

    def _get_error_messages(self):

        theory_error = 'The theory must be at least 8 characters and\
             not contain special characters'
        hypo_error= 'The hypothesis must be at least 8 characters and\
             not contain special characters'
        null_error = 'The null hypothesis must be at least 8 characters and\
             not contain special characters'

        if self._is_min_length(self.theory_desc.value)\
            and self._is_not_al_num(self.theory_desc.value):
            theory_error = ''
        if self._is_min_length(self.hypotheses[0].value)\
            and self._is_not_al_num(self.hypotheses[0].value):
            hypo_error = ''
        if self._is_min_length(self.hypotheses[1].value)\
            and self._is_not_al_num(self.hypotheses[1].value):
            null_error = ''

        return (theory_error, hypo_error, null_error)

    def _get_warning_messages(self):
        """Calls functions that validate that both theory, hypothesis,
        and null hypothesis includes a subject, a predicate and an object.
        Returns error messages based on nlp validation.
        
        Returns:
            errors (tuple)
        """
        theory_warning = 'Warning! The theory does not fill criteria of\
             including a subject, a predicate and an object.'
        hypo_warning = 'Warning! The hypothesis does not fill criteria of\
             including a subject, a predicate and an object.'
        null_warning = 'Warning! The null hypothesis does not fill criteria of\
             including a subject, a predicate and an object.'

        subject = 'nsubj'
        subject_passive = 'nsubjpass'
        predicate = 'V'
        prep_object = 'pobj'
        direct_object = 'dobj'

        if self._nlp(self.theory_desc.value, subject, subject_passive)\
            and self._nlp_predicate(self.theory_desc.value, predicate)\
            and self._nlp(self.theory_desc.value, prep_object, direct_object):
            theory_warning = ''
        if self._nlp(self.hypotheses[0].value, subject, subject_passive)\
            and self._nlp_predicate(self.hypotheses[0].value, predicate)\
            and self._nlp(self.hypotheses[0].value, prep_object, direct_object):
            hypo_warning = ''
        if self._nlp(self.hypotheses[1].value, subject, subject_passive)\
            and self._nlp_predicate(self.hypotheses[1].value, predicate)\
            and self._nlp(self.hypotheses[1].value, prep_object, direct_object):
            null_warning = ''

        return (theory_warning, hypo_warning, null_warning)

    def __create_limitation_prompt(self):
        """Creates limitation prompt grid"""

        hypothesis_text = self.bogui.create_message(
            f'You have set hypothesis (H1): {self.hypotheses[0].value}'
        )
        null_text = self.bogui.create_message(
            f'You have set null hypothesis (H0): {self.hypotheses[1].value}'
        )

        limitations = "<ul>\n"
        limitations += "\n".join(["<li>" + limitation.value + "</li>"
                                 for limitation in self.data_limitations])
        limitations += "\n</ul>"

        limitation_prompt_text = widgets.HTML(
            '</br>'+ '<h4> Do the hypotheses fit within the limitations of the data set? </h4>' 
             + limitations)

        limitation_prompt = widgets.VBox([
            hypothesis_text,
            null_text,
            limitation_prompt_text,
            widgets.HBox([self.buttons['yes'], self.buttons['no']])
        ])

        return limitation_prompt

    def __implement_error_messages(self, error, warning):

        if error:
            return (error, 'red')
        if warning:
            return (warning, 'orange')
        return ('','red')

    def submit_theory_and_hypotheses(self, _=None):
        """Calls check theory and hypothesis -
            function with paramenter False indicating Save -button is clicked
        """
        self.check_theory_and_hypotheses(False)

    def __validate_theory_and_hypotheses(self, _=None):
        """Calls check theory and hypothesis -
            function with paramenter False indicating Validate input -button is clicked
        """
        self.check_theory_and_hypotheses(True)

    def check_theory_and_hypotheses(self, is_validate):
        """Checks theory and hypotheses and displays the prompt for
        the check against data limitations
        
        Returns:
            True/False: True if theory, hypothesis, and null hypothesis are all filled
        """
        empty_theory_error, empty_hypo_error, empty_null_error = self._get_error_messages()
        theory_warning, hypo_warning, null_warning = self._get_warning_messages()

        theory_error, theory_error_color = self.__implement_error_messages(empty_theory_error,
                                                                        theory_warning)
        hypo_error, hypo_error_color = self.__implement_error_messages(empty_hypo_error,
                                                                    hypo_warning)
        null_error, null_error_color = self.__implement_error_messages(empty_null_error,
                                                                    null_warning)

        theory_grid = self.__create_theory_grid(theory_error, theory_error_color)
        hypotheses_grid = self.__create_hypotheses_grid(hypo_error, null_error,
                                                        hypo_error_color, null_error_color)

        is_show_limitation_prompt = True

        # If errors exist in any of the fields
        if len(empty_theory_error + empty_hypo_error + empty_null_error) > 0:
            is_show_limitation_prompt=False

        # If Validate - button is clicked and warnings exist
        elif is_validate:
            if len(theory_warning + hypo_warning + null_warning ) > 0:
                is_show_limitation_prompt=False

        # Show errors or/and warnings
        if not is_show_limitation_prompt:
            clear_output(wait=True)
            display(theory_grid)
            display(hypotheses_grid)
            self.focus_first_empty([self.theory_desc] + self.hypotheses)
            return False

        # Show limitation prompt - all values are ok
        limitation_prompt = self.__create_limitation_prompt()
        clear_output(wait=True)
        display(limitation_prompt)

        return True

    def bad_hypotheses(self, _=None):
        """Closes the data limitation check prompt and calls clear_hypotheses()"""
        theory_grid = self.__create_theory_grid()
        hypotheses_grid = self.__create_hypotheses_grid('Hypotheses must fit data limitations')
        clear_output(wait=True)
        display(theory_grid)
        display(hypotheses_grid)
        self.clear_hypotheses()

    def _format_hypotheses_and_theory(self):
        """Formats hypotheses and theory for markdown
        
        Returns:
            formatted_text (str)
        """
        formatted_text = f'## Testing hypothesis: {self.hypotheses[0].value}\\n'
        formatted_theory = '<br />'.join(self.theory_desc.value.split('\n'))
        formatted_text += f'### Theory and insights\\n{formatted_theory}\\n'
        hypotheses = f'- Hypothesis (H1): {self.hypotheses[0].value}\
        \\n- Null hypothesis (H0): {self.hypotheses[1].value}'
        formatted_text += f'### Hypotheses\\n{hypotheses}\\n### Data analysis'

        return formatted_text

    def save_theory_and_hypotheses(self, _=None):
        """Saves theory and hypotheses and displays buttons for running code"""
        text = self._format_hypotheses_and_theory()
        self.boutils.create_markdown_cells_above(1, text=text)
        cell_operations = self.__create_cell_operations_grid()
        clear_output(wait=True)
        display(cell_operations)
        self.add_cells_int.focus()

    def clear_hypotheses(self, _=None):
        """Button function for resetting hypothesis and null hypothesis inputs"""
        self.hypotheses[0].value = ''
        self.hypotheses[1].value = ''
        self.hypotheses[0].focus()

    def open_cells(self, _=None):
        """Button function for opening new code cells"""
        if self.add_cells_int.value > 0:
            self.cell_count += self.add_cells_int.value
            self.boutils.create_code_cells_above(self.add_cells_int.value)

    def delete_last_cell(self, _=None):
        """Button function for deleting the last code cell"""
        if self.cell_count > 0:
            self.boutils.delete_cell_above()
            self.cell_count -= 1

    def deactivate_cell_operations(self):
        """Deactivates buttons after runnig code block"""
        self.buttons['open'].disabled = True
        self.buttons['clear'].disabled = True
        self.buttons['delete'].disabled = True

    def __create_conclusion_grid(self):
        question = self.bogui.create_message(value='What happened?')
        conclusion_label = self.bogui.create_message(value='Accepted hypothesis:')
        self.conclusion = self.bogui.create_radiobuttons(
            options=[f'H1: {self.hypotheses[0].value}',
                     f'H0: {self.hypotheses[1].value}'])

        notes_label = self.bogui.create_message(value='Describe your results here:')

        grid = widgets.AppLayout(
            header=question,
            left_sidebar=conclusion_label,
            center=self.conclusion,
            footer=widgets.VBox([
                notes_label,
                self.result_description,
                self.buttons['save_results']
            ]),
            pane_widths=['150px', 1, 0],
            pane_heights=['20px', '40px', 1],
            grid_gap='12px'
        )

        return grid

    def run_cells(self, _=None):
        """Runs code cells, deactivates cell operations, and shows radiobuttons"""
        self.boutils.run_cells_above(
            self.cell_count)
        self.deactivate_cell_operations()

        clear_output(wait=True)
        cell_operations = self.__create_cell_operations_grid()
        conclusion = self.__create_conclusion_grid()
        display(cell_operations)
        display(conclusion)
        conclusion.focus()

    def clear_cells(self, _=None):
        """Clear button function to clear cells above"""
        self.boutils.clear_code_cells_above(self.cell_count)

    def __create_cell_operations_grid(self):
        """Creates widget grid"""
        cell_number_label = self.bogui.create_label('Add code cells for your analysis:')

        grid = widgets.GridspecLayout(2, 2, justify_items='center',
                                     width='70%', align_items='center')
        grid[1, 0] = widgets.HBox([cell_number_label, self.add_cells_int])
        grid[1, 1] = widgets.TwoByTwoLayout(
            top_left=self.buttons['open'],
            bottom_left=self.buttons['run'],
            top_right=self.buttons['delete'],
            bottom_right=self.buttons['clear'])

        return grid

    def save_results(self, _=None):
        """Prints results as markdown and hides widgets"""
        clear_output(wait=True)
        text = (f'## Conclusion\\n### Accepted hypothesis: {self.conclusion.value[4:]}\\n'
                f'The hypotheses were:\\n- Hypothesis (H1): {self.hypotheses[0].value}\\n'
                f'- Null hypothesis (H0): {self.hypotheses[1].value}\\n')

        if self.result_description.value:
            formatted_description = '<br />'.join(self.result_description.value.split('\n'))
            text += f'### Notes\\n {formatted_description}'

        self.boutils.create_markdown_cells_above(1, text=text)
        self.next_step[0] = 'analysis_done'

    def _is_min_length(self, text):
        if not text:
            return False
        text.replace(" ", "")
        if len(text) < 8:
            return False
        return True

    def _is_not_al_num(self, text):
        if not text:
            return False
        special_characters = "[{]}@#^\\*()+_=<>/"
        if any(c in special_characters for c in text):
            return False
        return True

    def _nlp_predicate(self, text, sentence_element):
        '''Checks that string contains at least one predicate.

            Args:
                text(str)
            Return:
                true: if sentence contain at least one verb
                false: if value is empty or not contain verb
        '''
        words = self.nlp(text)
        if any(word.tag_[0] == sentence_element for word in words):
            return True

        return False

    def _nlp(self, text, sentence_element1, sentence_element2):
        '''Checks that string contains at least one of the desired sentence elements.

            Args:
                text(str)
            Return:
                true: if sentence contain at least one verb
                false: if value is empty or not contain verb
        '''
        words = self.nlp(text)
        if any(word.dep_ == sentence_element1 or sentence_element2 for word in words):
            return True

        return False

    def __repr__(self):
        return ''
