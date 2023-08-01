from ipywidgets import widgets
from IPython.display import display, clear_output
import openai
from getpass import getpass

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
    
    @property
    def button_list(self):
        button_list = [
            ('send_ai_btn', 'Send', self.send_ai, 'primary'),
            ('clear_ai_btn', 'Clear', self.clear_ai, 'danger'),
            ('advanced_ai_btn', 'Advanced', self.advanced_ai, 'primary'),
            ('close_ai_btn', 'Close', self.close_ai, 'warning'),

        ]
        return button_list

    #def __create_input_grid(self):
        
    def send_ai(self, _=None):
        """Button function for sending input to AI API"""
        self.api_key = self.api_key_input_field.value
        self.openai_api()
    
    def clear_ai(self,_=None):
        """Button function for clearing input text field"""

    def close_ai(self, _=None):
        """Button function for closing AI view"""

    def advanced_ai(self,_=None):
        """Button function for setting advanced options for the AI assistant"""
    
    def display_ai_assistant(self, _=None):
        """" Function for displaying communication with AI assistant"""
        feature_description = self.bogui.create_message('Enter a natural language prompt. The AI assistant will propose code to implement your request.')
    
        api_key_label = self.bogui.create_label('Enter your Open AI key here:')

        api_key_element = widgets.HBox([
            api_key_label,
            self.api_key_input_field,       
        ])
    
        grid = widgets.AppLayout(
        header = api_key_element,
        center= widgets.VBox([
            feature_description,            
            self.natural_language_prompt
          ]),
        footer = widgets.HBox([
            self.buttons['send_ai_btn'],
            self.buttons['clear_ai_btn'],
            self.buttons['advanced_ai_btn'],
            self.buttons['close_ai_btn'],
          
        ]),
        pane_widths=[2, 5, 5],
        grid_gap='10px'
        )

        display(grid)
    
    def openai_api(self, _=None):
        openai.api_key = self.api_key
        model_engine = self.model_engine

        system_msg = "You are a helpful assistant."
        content = "Placeholder, input from text field goes here. Say hello."
        response = openai.ChatCompletion.create(
            model = model_engine,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": content},
        ])

        message = response.choices[0]['message']
        ## TODO: print message into a code cell


        
        print("{}: {}".format(message['role'], message['content']))