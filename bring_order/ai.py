"""AI assistant"""
from ipywidgets import widgets
from IPython.display import display, clear_output
import pandas as pd
import openai

class Ai:
    """AI assistant"""
    def __init__(self, bogui, utils, next_step):
        """Initializes AI-assistant class"""
        self.bogui = bogui
        self.utils = utils
        self.next_step = next_step
        self.buttons = self.bogui.init_buttons(self.button_list)
        self.natural_language_prompt = self.bogui.create_text_area()
        self.api_key_input_field = self.bogui.create_password_field()
        self.context_selection = widgets.Dropdown(
            options = ['No context', 'Include dataset', 'Enter manually']
        )
        self.context = 'You are a helpful assistant. Give the answer in one Python code block\
            indicated with ```python.'
        self.buttons = self.bogui.init_buttons(self.button_list)
        self.ai_response = ''
        self.ai_output_grid = widgets.AppLayout()
        self.ai_output = ''
        self.ai_error_message_grid = None
        self.ai_error_msg = self.bogui.create_message('')
        self.model_engine = "gpt-3.5-turbo"
        self.grid = None
        self.visible = False
        self.dataset = pd.DataFrame()

    @property
    def button_list(self):
        """Buttons for AI assistant class.

        Returns:
            list of tuples in format (tag: str, description: str, command: func, style: str)
        """
        button_list = [
            ('send_ai_btn', 'Send', self.send_ai, 'primary'),
            ('clear_ai_btn', 'Clear', self.clear_ai, 'danger'),
            ('close_ai_btn', 'Close', self.close_ai, 'warning'),
            ('send_api_key_btn','Submit key', self.initiate_ai, 'success'),
            ('disable_ai', 'Skip', self.disable_ai, 'warning'),
            ('select_context', 'Select', self.select_context, 'success'),
            ('show', 'Show response', self.show_response, 'primary'),
            ('hide', 'Hide response', self.hide_response, 'primary')
        ]
        return button_list


    def initiate_ai(self, _=None):
        self.api_key = self.api_key_input_field.value
        if not self.validate_api_key():
            clear_output(wait=True)
            self.display_ai_popup(self.ai_error_msg)
            return
               
        self.ai_context = self.context_selection.value
        
        clear_output(wait=True)
        self.next_step[0] = 'bodi'

    def disable_ai(self, _=None):
        clear_output(wait=True)
        self.next_step[0] = 'bodi'

    def send_ai(self, _=None):
        """Button function for sending input to AI API"""
        self.remove_ai_error_message()
        self.ai_output = ''
        self.display_ai_output('The AI assistant is processing your message...')
        self.buttons['show'].disabled = True
        if self.validate_npl_input():
            self.openai_api()

    def remove_ai_error_message(self):
        """Removes error messages from display"""
        self.ai_error_msg = ''
        if  self.ai_error_message_grid is not None:
            self.ai_error_message_grid.close()

    def clear_ai(self,_=None):
        """Button function for clearing input text field"""
        self.natural_language_prompt.value = ''

    def close_ai(self, _=None):
        """Button function for closing AI view"""
        self.grid.close()

    def validate_api_key(self):
        """Button function for validating API key"""
        if not self.api_key_input_field.value:
            self.ai_error_msg = 'Please enter your Open AI api key'
            return False
        
        try:
            openai.api_key = self.api_key
            content = self.natural_language_prompt.value
            response = openai.ChatCompletion.create(
            model = self.model_engine,
            messages=[
                {"role": "system", "content": self.context},
                {"role": "user", "content": content},
            ])

            if not response.choices[0]['message']['content']:
                self.ai_error_msg = f"Please enter correct OpenAI API key. You recieved no respoonse from the AI assistant."
                return False
                   
        except openai.error.AuthenticationError as err:
            self.ai_error_msg = f"{err}"
            return False 

        return True
    
    def validate_context(self):
        """Validates context"""
        if not self.ai_context:
            return False
        return True

    def validate_npl_input(self):
        """Validates nlp input"""
        if not self.natural_language_prompt.value:
            return False
        return True

    def toggle_ai(self, _=None):
        """Toggles the AI view"""
        if self.visible is False:
            self.visible = True
            self.remove_ai_error_message()
            self.display_ai()
            self.ai_output = ''
            self.display_ai_output()
        else:
            self.visible = False
            self.close_ai()
            self.ai_output_grid.close()
            self.remove_ai_error_message()

    def display_ai_popup(self, api_key_error=''):
        """" Function for displaying communication with AI assistant"""
        api_key_label = self.bogui.create_label('Enter your Open AI key here:')
        api_key_element = widgets.HBox([
            api_key_label,
            widgets.VBox([
                self.api_key_input_field,
                self.bogui.create_error_message(api_key_error, 'red')
            ]),
        ])

        self.grid = widgets.AppLayout(
            header = api_key_element,
            center = widgets.HBox([
                self.buttons['send_api_key_btn'],
                self.buttons['disable_ai']
                ]),
            footer = None,
            pane_widths=[4, 6, 4],
            pane_heights=[4, 6, 3]
        )

        display(self.grid)

    def select_context(self, _=None):
        if self.context_selection.value == 'Include dataset':
            variable_list = self.dataset.columns.values.tolist()
            variables = "Variables of the dataset are " +str(variable_list)
            self.context = variables
        elif self.context_selection.value == 'Enter manually':
            manual_context = self.bogui.create_text_area(place_holder='This is my context')
            display(manual_context)
            self.context = manual_context.value


    def display_ai(self, nlp_error= '', context_error = ''):
        '''Displays a text field for entering a question and options for includng context'''
        feature_description = self.bogui.create_message(
            'Enter a natural language prompt. The AI assistant will propose code\
            to implement your request.'
            )

        context_box = widgets.VBox([
            self.bogui.create_message(
            'Do you want to include your dataset as context or enter context manually?'),
            self.context_selection,
            self.buttons['select_context'],
            self.bogui.create_error_message(context_error, 'red')
        ])

        self.grid = widgets.AppLayout(
            header = feature_description,
            center= widgets.VBox([
                self.natural_language_prompt,
                context_box,
                self.bogui.create_error_message(nlp_error, 'red')
            ]),
            footer = widgets.HBox([
                self.buttons['send_ai_btn'],
                self.buttons['clear_ai_btn']
                ]),
            pane_widths=[1, 8, 1],
            pane_heights=[2, 6, 2]
        )

        display(self.grid)

    def display_ai_output(self, message='', hide=False):
        """Displays ai output"""

        self.ai_output_grid.close()

        self.ai_output_grid = widgets.AppLayout(
            header = self.bogui.create_message(message),
            center = self.bogui.create_message(self.ai_output),
            pane_heights = ['40px', 1, '40px']
        )

        if self.ai_response != '':
            if hide:
                self.ai_output_grid.footer = self.buttons['hide']
            else:
                self.ai_output_grid.footer = self.buttons['show']

        display(self.ai_output_grid)
    

    def display_ai_error_message(self):
        """Displays error message"""

        self.ai_output.value = ''
        self.ai_error_message_grid = widgets.AppLayout(
            center = self.bogui.create_message(self.ai_error_msg)
        )
        display(self.ai_error_message_grid)


    def openai_api(self):
        """Function to check openai api key"""

        try:
            openai.api_key = self.api_key
            model_engine = self.model_engine
            system_msg = self.context
            content = self.natural_language_prompt.value
            response = openai.ChatCompletion.create(
                model = model_engine,
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": content},
            ])

            self.ai_response = response.choices[0]['message']['content']
            code = self.utils.get_python_code_from_response(self.ai_response)
            if code == 'No Python code in the response':
                self.display_ai_output('Python code was not found in the response.')
                
            else:
                self.utils.insert_ai_code_into_new_cell(code)
                self.display_ai_output('Code inserted into a code cell above.')

            self.buttons['show'].disabled = False

        except openai.error.Timeout as err:
            self.ai_error_msg = f"OpenAI API request timed out: {err}"
            self.display_ai_error_message()

        except openai.error.APIError as err:
            self.ai_error_msg = f"OpenAI API returned an API Error: {err}"
            self.display_ai_error_message()

        except openai.error.APIConnectionError as err:
            self.ai_error_msg = f"OpenAI API request failed to connect: {err}"
            self.display_ai_error_message()

        except openai.error.InvalidRequestError as err:
            self.ai_error_msg = f"OpenAI API request was invalid: {err}"
            self.display_ai_error_message()

        except openai.error.AuthenticationError as err:
            self.ai_error_msg = f"OpenAI API request was not authorized: {err}"
            self.display_ai_error_message()

        except openai.error.PermissionError as err:
            self.ai_error_msg = f"OpenAI API request was not permitted: {err}"
            self.display_ai_error_message()

        except openai.error.RateLimitError as err:
            self.ai_error_msg = f"OpenAI API request exceeded rate limit: {err}"
            self.display_ai_error_message()

    # def display_response(self, message):
    #     """ Parses, calls formatter and displays response from AI assistant

    #     args:

    #     returns:
    #     """
    #     text = self.format_response(message['content'])
    #     return text

    def format_response(self, text):
        """ Formats AI response for html widget.

        Returns:
            formatted_text (str)
        """

        formatted_text = '<br />'.join(text.split('\n'))
        formatted_text = '<pre>' + formatted_text + '</pre>'

        return formatted_text

    def show_response(self, _=None):
        """Button function to show the complete AI response."""

        self.ai_output = self.format_response(self.ai_response)
        self.display_ai_output(message='The response from the AI assistant:', hide=True)

    def hide_response(self, _=None):
        """Button function to hide AI response."""

        self.ai_output = ''
        self.display_ai_output(message='Check the AI response by clicking the button below.')