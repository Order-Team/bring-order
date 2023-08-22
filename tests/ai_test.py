import unittest
from ipywidgets import widgets
from bring_order.boutils import BOUtils
from bring_order.bogui import BOGui
from bring_order.bodi import Bodi
from bring_order.ai import Ai
from unittest.mock import Mock, MagicMock
import pandas as pd


class TestAi(unittest.TestCase):

    def setUp(self):
        next_step = [None]
        self.instance = Ai(
                            BOGui(),
                            BOUtils(),
                            dataset_variables=[['sepallength', 'sepalwidth', 'petallength', 'petalwidth', 'class']],
                            ai_disabled = [False],
                            next_step=next_step
                            )
        self.instance.boutils = Mock()
        self.instance.bogui = Mock()
        self.instance.context_selection = Mock()
        self.instance.bogui.create_message = lambda value: widgets.HTML(value=value)
        self.instance.bogui.create_error_message = lambda value, color: widgets.HTML(value=value)

    def test_correct_amount_of_buttons_is_created(self):
        self.assertEqual(len(self.instance.buttons), 7)

    def test_add_instructions_contains_dataset_variables(self):
        test_instructions = self.instance.add_instructions()
        correct = 'The user wants to process a dataset with Python code.\
        The dataset has certain variables. Refer to these given variables where appropriate.\
        Variables of the dataset are: sepallength, sepalwidth, petallength, petalwidth, class'
        self.assertEqual(test_instructions, correct)

    def test_send_ai_disables_show_button(self):
        self.instance.buttons['show'].disabled = False
        self.instance.send_ai()
        self.assertTrue(self.instance.buttons['show'])

    def test_send_ai_sets_correct_message_with_empty_input(self):
        self.instance.send_ai()
        self.assertEqual(
            self.instance.ai_output_grid.header.value,
            'Write a message for the AI assistant before sending.'
        )

    def test_send_ai_sets_correct_message_with_valid_input(self):
        self.instance.openai_api = MagicMock()
        self.instance.natural_language_prompt.value = 'How to create a sample from standard\
            normal distribution in Python code?'
        self.instance.send_ai()
        self.assertEqual(
            self.instance.ai_output_grid.header.value,
            'The AI assistant is processing your message...'
        )

    def test_send_ai_resets_error_message(self):
        self.instance.openai_api = MagicMock()
        self.instance.natural_language_prompt.value = 'How to create a sample from standard\
            normal distribution in Python code?'
        self.instance.send_ai()
        self.assertEqual(self.instance.ai_error_msg, '')

    def test_toggle_ai_creates_correct_output_grid_in_the_beginning(self):
        self.instance.context_selection = widgets.Dropdown()
        self.instance.toggle_ai()
        self.assertEqual(self.instance.ai_output_grid.header.value, '')
        self.assertEqual(self.instance.ai_output_grid.center.value, '')
        self.assertIsNone(self.instance.ai_output_grid.footer)

    def test_toggle_ai_creates_correct_output_grid_later(self):
        self.instance.context_selection = widgets.Dropdown()
        self.instance.ai_response = 'Hi, I am a helpful AI assistant'
        self.instance.toggle_ai()
        self.assertEqual(
            self.instance.ai_output_grid.header.value,
            'Check the previous response by clicking the button below.'
        )
        self.assertEqual(self.instance.ai_output_grid.center.value, '')
        self.assertEqual(
            self.instance.ai_output_grid.footer,
            self.instance.buttons['show']
        )

    def test_display_ai_output_shows_correct_button(self):
        self.instance.display_ai_output()
        self.assertIsNone(self.instance.ai_output_grid.footer)
        self.instance.ai_response = 'Hi, I am a helpful AI assistant'
        self.instance.display_ai_output()
        self.assertEqual(
            self.instance.ai_output_grid.footer,
            self.instance.buttons['show']
        )
        self.instance.display_ai_output(ai_output=self.instance.ai_response)
        self.assertEqual(
            self.instance.ai_output_grid.footer,
            self.instance.buttons['hide']
        )

    def test_display_ai_output_sets_correct_message_and_output(self):
        self.instance.ai_response = 'Hi, I am a helpful AI assistant'
        self.instance.display_ai_output()
        self.assertEqual(self.instance.ai_output_grid.header.value, '')
        self.assertEqual(self.instance.ai_output_grid.center.value, '')
        self.instance.display_ai_output(
            message='The AI assistant says:',
            ai_output=self.instance.ai_response
        )
        self.assertEqual(
            self.instance.ai_output_grid.header.value,
            'The AI assistant says:'
        )
        self.assertEqual(
            self.instance.ai_output_grid.center.value,
            'Hi, I am a helpful AI assistant'
        )

    def test_format_response_returns_correct_string(self):
        response = ("Here's an example code snippet that accomplishes this:\n"
                    "```python\n"
                    "import numpy as np\n"
                    "# Generate sample from standard normal distribution\n"
                    "sample = np.random.normal(loc=0, scale=1, size=1000)\n"
                    "# Calculate sample mean and variance\n"
                    "sample_mean = np.mean(sample)\n"
                    "sample_variance = np.var(sample)\n"
                    "```\n"
                    "\n"
                    "Finally, the calculated mean and variance are printed to the console.")

        correct = ("<pre>"
                   "Here's an example code snippet that accomplishes this:<br />"
                   "```python<br />"
                   "import numpy as np<br />"
                   "# Generate sample from standard normal distribution<br />"
                   "sample = np.random.normal(loc=0, scale=1, size=1000)<br />"
                   "# Calculate sample mean and variance<br />"
                   "sample_mean = np.mean(sample)<br />"
                   "sample_variance = np.var(sample)<br />"
                   "```<br />"
                   "<br />"
                   "Finally, the calculated mean and variance are printed to the console."
                   "</pre>")
        
        self.assertEqual(self.instance.format_response(response), correct)

    def test_show_response_formats_response_for_html(self):
        self.instance.format_response = MagicMock(return_value='')
        self.instance.ai_response = 'Hi, I am a helpful AI assistant'
        self.instance.show_response()
        self.instance.format_response.assert_called_with(self.instance.ai_response)

    def test_show_response_sets_correct_message_output_and_button(self):
        self.instance.ai_response = 'Hi, I am a helpful AI assistant'
        self.instance.show_response()
        self.assertEqual(
            self.instance.ai_output_grid.header.value,
            'The response from the AI assistant:'
        )
        self.assertEqual(
            self.instance.ai_output_grid.center.value,
            '<pre>Hi, I am a helpful AI assistant</pre>'
        )
        self.assertEqual(
            self.instance.ai_output_grid.footer,
            self.instance.buttons['hide']
        )

    def test_hide_response_sets_correct_message_output_and_button(self):
        self.instance.ai_response = 'Hi, I am a helpful AI assistant'
        self.instance.show_response()
        self.instance.hide_response()
        self.assertEqual(
            self.instance.ai_output_grid.header.value,
            'Check the previous response by clicking the button below.'
        )
        self.assertEqual(self.instance.ai_output_grid.center.value, '')
        self.assertEqual(
            self.instance.ai_output_grid.footer,
            self.instance.buttons['show']
        )
