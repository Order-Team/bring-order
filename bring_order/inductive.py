"""Class for Inductive analysis"""
from ipywidgets import widgets
from IPython.display import display, clear_output, Javascript

class Inductive:
    """Class that guides inductive analysis"""

    def __init__(self, bogui, boutils, next_step):
        """Class constructor."""

        self.bogui = bogui
        self.utils = boutils
        self.next_step = next_step
        self._cell_count = 0
        self.buttons = self.bogui.init_buttons(self.button_list)
        self.preconceptions = [self.bogui.create_input_field('', 'Preconception 1')]
        self._add_cells_int = self.bogui.create_int_text()
        self._notes = self.bogui.create_text_area()
        self.conclusion = None
        self.summary = self.bogui.create_text_area('', 'Summary')
        self.empty_notes_error = self.bogui.create_error_message()
        self.observations = []

    @property
    def button_list(self):
        """Buttons for Inductive class.

        Returns:
            list of tuples in format (tag: str, description: str, command: func, style: str)
        """

        button_list = [
            ('add', 'Add preconception', self._add_preconception, 'primary'),
            ('save', 'Save preconceptions', self._save_preconceptions, 'success'),
            ('open', 'Open cells', self._open_cells, 'warning'),
            ('delete', 'Delete last cell', self._delete_last_cell, 'danger'),
            ('clear', 'Clear cells', self._clear_cells, 'danger'),
            ('run', 'Run cells', self._run_cells, 'primary'),
            ('ready', 'Ready to summarize', self._execute_ready, 'primary'),
            ('submit_obs', 'Submit observation', self._new_observation, 'warning'),
            ('submit_sum', 'Submit summary', self._submit_summary, 'success'),
            ('lock', 'Lock evaluation', self._lock_evaluation_pressed, 'success'),
            ('save_results', 'Save', self._save_results, 'success')
        ]

        return button_list

    def start_inductive_analysis(self):
        """Starts inductive analysis."""

        self.utils.create_markdown_cells_above(1, '## Data exploration')
        display(self._create_preconception_grid())

    def _add_preconception(self, _=None):
        """Button function to add new preconception."""

        self.preconceptions.append(
            self.bogui.create_input_field('', f'Preconception {len(self.preconceptions) + 1}')
        )

        clear_output(wait=True)
        display(self._create_preconception_grid())

    def _check_preconceptions(self):
        """Checks that at least one of the preconceptions has a non-empty value."""

        for item in self.preconceptions:
            if item.value != '':
                return True

        return False

    def _format_preconceptions(self):
        """Formats preconceptions for markdown.

        Returns:
            formatted_preconceptions (str)
        """

        formatted_preconceptions = '### Preconceptions\\n'
        for item in self.preconceptions:
            preconception_text = f'- {item.value}\\n'
            formatted_preconceptions += preconception_text

        formatted_preconceptions += '### Data analysis'
        return formatted_preconceptions

    def _save_preconceptions(self, _=None):
        """Button function to save preconceptions as markdown and show cell operation buttons."""

        clear_output(wait=True)

        if self._check_preconceptions():
            # Remove empty preconceptions from the list
            self.preconceptions = list(filter(
                lambda text_input: text_input.value != '',
                self.preconceptions
            ))

            self.utils.create_markdown_cells_above(
                how_many=1,
                text=self._format_preconceptions()
            )

            display(self._create_cell_operations())

        else:
            display(self._create_preconception_grid(
                error='You must name at least one preconception')
            )

    def _create_preconception_grid(self, error=''):
        """Creates the grid with input fields and buttons to add and save preconceptions."""

        preconceptions_label = self.bogui.create_message(
                value='Write about your preconceptions concerning the data set:')

        preconception_grid = widgets.AppLayout(
            header=preconceptions_label,
            center=widgets.VBox(self.preconceptions),
            footer=widgets.VBox([
                self.bogui.create_error_message(error),
                widgets.HBox([
                    self.buttons['add'],
                    self.buttons['save']
                ])
            ]),
            pane_heights=['30px', 1, '70px'],
            grid_gap='12px'
        )

        return preconception_grid

    def _open_cells(self, _=None):
        """Open cells button function that opens the selected number of code cells."""

        if self._add_cells_int.value > 0:
            self._cell_count += self._add_cells_int.value
            self.utils.create_code_cells_above(self._add_cells_int.value)

    def _delete_last_cell(self, _=None):
        """Delete last cell button function."""

        if self._cell_count > 0:
            self.utils.delete_cell_above()
            self._cell_count -= 1

    def _clear_cells(self, _=None):
        """Clears all code cells above."""

        self.utils.clear_code_cells_above(self._cell_count)

    def _buttons_disabled(self, disabled):
        """Activates/deactivates buttons.
        
        Args:
            disbled (bool): True to disable, False to activate
        """

        self.buttons['open'].disabled = disabled
        self.buttons['clear'].disabled = disabled
        self.buttons['delete'].disabled = disabled
        self.buttons['ready'].disabled = disabled

    def _run_cells(self, _=None):
        """Executes cells above and displays text area for observations of analysis."""

        if self._cell_count <= 0:
            return

        self.utils.run_cells_above(self._cell_count)
        if self.conclusion:
            self.conclusion.close()

        self._buttons_disabled(True)

        notes_label = self.bogui.create_label(value='Explain what you observed:')
        self.conclusion = widgets.VBox([
            widgets.HBox([notes_label, self._notes]),
            self.empty_notes_error,
            self.buttons['submit_obs']
        ])

        display(self.conclusion)

    def _get_first_words(self, word_list):
        """Takes a word list and returns a string that has the first sentence or
        the first five words and three dots if the sentence is longer.
        
        Args:
            word_list (list)
            
        Returns:
            first_words (str)
        """

        first_words = f'{word_list[0]}'

        for word in word_list[1:5]:
            first_words += f' {word}'
            if any(mark in word for mark in ['.', '?', '!']):
                return first_words.strip('.')

        first_words.strip('.').strip(',')
        if len(word_list) > 5:
            first_words += '...'

        return first_words

    def _format_observation(self):
        """Formats observation for markdown.
        
        Returns:
            formatted_obs (str)
        """

        formatted_obs = f'#### Observation {len(self.observations)}: '

        notes_list = self._notes.value.split('\n')
        first_line_list = notes_list[0].split(' ')
        first_words = self._get_first_words(first_line_list)
        formatted_obs += f'{first_words}\\n'

        notes = '<br />'.join(notes_list)
        formatted_obs += notes

        return formatted_obs

    def _new_observation(self, _=None):
        """Checks new observation, saves it, and resets cell count."""

        if self._check_value_not_empty(self._notes.value):
            self.observations.append(self._notes.value)
            text = self._format_observation()
            self.utils.create_markdown_cells_above(1, text=text)
            self._buttons_disabled(False)
            self.empty_notes_error.value = ''
            self.conclusion.close()
            self._notes.value = ''
            self._cell_count = 0

        else:
            self.empty_notes_error.value = 'Observation field can not be empty'

    def _execute_ready(self, _=None):
        """Button function for Ready to summarize button."""

        self._display_summary()

    def _display_summary(self, error=''):
        """Prints all observations and asks for summary."""

        observations = "<ul>\n"
        observations += "\n".join(["<li>" + observation + "</li>"
                                 for observation in self.observations])
        observations += "\n</ul>"

        observation_list = widgets.HTML(
            '</br>'+'<h4>All your observations from the data:</h4>'+observations)

        summary_label = self.bogui.create_label('What do these observations mean?')
        error_message = self.bogui.create_error_message(value=error)
        grid = widgets.VBox([
            observation_list,
            widgets.HBox([summary_label, self.summary]),
            error_message,
            self.buttons['submit_sum']
        ])

        clear_output(wait=True)
        display(grid)

    def _format_summary(self):
        """Formats summary for markdown.
        
        Returns:
            formatted_summary (str)
        """

        formatted_summary = '### Summary: '

        summary_list = self.summary.value.split('\n')
        first_line_list = summary_list[0].split(' ')
        first_words = self._get_first_words(first_line_list)
        formatted_summary += f'{first_words}\\n'

        summary = '<br />'.join(summary_list)
        formatted_summary += summary

        return formatted_summary

    def _submit_summary(self, _=None):
        """Button function to submit summary."""

        if not self._check_value_not_empty(self.summary.value):
            self._display_summary(error='You must write some kind of summary')
            return

        text = self._format_summary()
        self.utils.create_markdown_cells_above(1, text=text)
        self._evaluation_of_analysis()

    def _evaluation_of_analysis(self, _=None):
        self.buttons['submit_sum'].disabled = True
        clear_output(wait=False)
        grid = widgets.AppLayout(
            header = self.bogui.create_message(
                        'Evaluate how confident you are that analysis meet preconceptions?'),
            center = widgets.IntSlider(value=50, min=0, max=100, step=5,
                                        description='', disabled=False,
                                        continuous_update=False,
                                        orientation='horizontal',
                                        readout=True, readout_format='d'
                                        ),
            right_sidebar = self.buttons['lock'],
            footer = None
            )
        display(grid)

    def _lock_evaluation_pressed(self, _=None):
        clear_output(wait=False)
        label = self.bogui.create_message('Did the analysis meet preconceptions?')
        checkboxes = [widgets.Checkbox(
                        description=prec.value, value=False,) for prec in self.preconceptions]
        output = widgets.VBox(checkboxes)
        display(label, output)
        grid = widgets.AppLayout(
            header = self.bogui.create_message('Overall how satisfied you are in the analysis?'),
            center = widgets.SelectionSlider(
                options=['Very dissatisfied','Dissatisfied','Neutral','Satisfied','Very satisfied'],
                value = 'Neutral',
                description='',
                disabled=False, continuous_update=False,
                orientation='horizontal', readout=True
            ),
            footer = None)
        display(grid)
        display(self.buttons['save_results'])
    
    def _save_results(self, _=None):
        clear_output(wait=True)
        self.next_step[0] = 'analysis_done'

    def _checkbox_preconceptions(self):
        clear_output(wait=False)
        checkboxes = [self.bogui.create_checkbox(prec) for prec in self.preconceptions]
        output = widgets.VBox(children=checkboxes)
        display(output)

    def _check_value_not_empty(self, value):
        """Checks that text field was filled.
            Args: string
            Returns:
                True: if string not empty
                False: if string is empty
        """
        if value == '':
            return False

        return True

    def _create_cell_operations(self):
        """Displays buttons for operations in inductive analysis."""

        self.buttons['ready'].disabled = True
        cell_number_label = self.bogui.create_label('Add code cells for your analysis:')

        cell_buttons = widgets.TwoByTwoLayout(
            top_left=self.buttons['open'],
            bottom_left=self.buttons['run'],
            top_right=self.buttons['delete'],
            bottom_right=self.buttons['clear']
        )

        grid = widgets.GridspecLayout(2, 3, height='auto', width='100%')
        grid[0, 0] = widgets.HBox([cell_number_label, self._add_cells_int])
        grid[:, 1] = cell_buttons
        grid[1, 2] = self.buttons['ready']

        return grid

    def __repr__(self):
        return ''
