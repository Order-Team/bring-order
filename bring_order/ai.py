from getpass import getpass
from ipywidgets import widgets
from IPython.display import display, clear_output
import openai


class Ai:
    def __init__(self, bogui, utils, next_step):
        self.bogui = bogui
        self.utils = utils
        self.next_step = next_step
        self.buttons = self.bogui.init_buttons(self.button_list)
        self.natural_language_prompt = self.bogui.create_text_area()
        self.api_key_input_field = self.bogui.create_input_field()
        self.buttons = self.bogui.init_buttons(self.button_list)
        self.api_key = ""
        self.model_engine = "gpt-3.5-turbo"
        self.grid = None
        self.visible = False

    @property
    def button_list(self):
        button_list = [
            ('send_ai_btn', 'Send', self.send_ai, 'primary'),
            ('clear_ai_btn', 'Clear', self.clear_ai, 'danger'),
            ('advanced_ai_btn', 'Advanced', self.advanced_ai, 'primary'),
            ('close_ai_btn', 'Close', self.close_ai, 'warning')
        ]
        return button_list

    #def __create_input_grid(self):

    def send_ai(self, _=None):
        """Button function for sending input to AI API"""
        self.api_key = self.api_key_input_field.value
        self.openai_api()

    def clear_ai(self,_=None):
        """Button function for clearing input text field"""
        self.natural_language_prompt.value = ''

    def close_ai(self, _=None):
        """Button function for closing AI view"""
        self.grid.close()

    def advanced_ai(self,_=None):
        """Button function for setting advanced options for the AI assistant"""

    def toggle_ai(self, _=None):
        """Toggles the AI view"""
        if self.visible is False:
            self.visible = True
            self.display_ai()
        else:
            self.visible = False
            self.close_ai()

    def display_ai(self, _=None):
        """" Function for displaying communication with AI assistant"""
        feature_description = self.bogui.create_message(
            'Enter a natural language prompt. The AI assistant will propose code to implement your request.'
            )

        api_key_label = self.bogui.create_label('Enter your Open AI key here:')

        api_key_element = widgets.HBox([
            api_key_label,
            self.api_key_input_field,
        ])

        self.grid = widgets.AppLayout(
        header = api_key_element,
        center= widgets.VBox([
            feature_description,
            self.natural_language_prompt
          ]),
        footer = widgets.HBox([
            self.buttons['send_ai_btn'],
            self.buttons['clear_ai_btn'],
            self.buttons['advanced_ai_btn'],
            #self.buttons['close_ai_btn'],

        ]),
        pane_widths=[2, 5, 5],
        grid_gap='10px'
        )

        display(self.grid)

    def openai_api(self, _=None):
        openai.api_key = self.api_key
        model_engine = self.model_engine

        system_msg = "You are a helpful assistant."
        content = self.natural_language_prompt.value
        response = openai.ChatCompletion.create(
            model = model_engine,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": content},
        ])

        message = response.choices[0]['message']
        ## TODO: print message into a code cell



        print("{}: {}".format(message['role'], message['content']))
