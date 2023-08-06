
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
        self.api_key_input_field = self.bogui.create_password_field()
        self.context_input_field = self.bogui.create_input_field()
        self.buttons = self.bogui.init_buttons(self.button_list)
        self.ai_output = None
        self.model_engine = "gpt-3.5-turbo"
        self.grid = None
        self.visible = False

    @property
    def button_list(self):
        button_list = [
            ('send_ai_btn', 'Send', self.send_ai, 'primary'),
            ('clear_ai_btn', 'Clear', self.clear_ai, 'danger'),
            ('advanced_ai_btn', 'Advanced', self.advanced_ai, 'primary'),
            ('close_ai_btn', 'Close', self.close_ai, 'warning'),
             ('insert_code_to_cell', 'Insert code to cell', self.insert_code_to_cell, 'primary'),
            
        ]
        return button_list

    #def __create_input_grid(self):

    def send_ai(self, _=None):
        """Button function for sending input to AI API"""
        if self.validate_api_key() and self.validate_npl_input():
            self.openai_api()

    def clear_ai(self,_=None):
        """Button function for clearing input text field"""
        self.natural_language_prompt.value = ''

    def close_ai(self, _=None):
        """Button function for closing AI view"""
        self.grid.close()

    def advanced_ai(self,_=None):
        """Button function for setting advanced options for the AI assistant"""
    
    def validate_api_key(self):
        """Button function for validating API key"""
        if not self.api_key_input_field.value:
            return False
        return True
    
    def validate_npl_input(self):
        if not self.natural_language_prompt.value:
            return False
        return True
            
        
    def toggle_ai(self, _=None):
        """Toggles the AI view"""
        if self.visible is False:
            self.visible = True
            self.display_ai()
        else:
            self.visible = False
            self.close_ai()

    
    def display_ai(self, _=None, api_key_error='', nlp_error= '', context_error = ''):
        """" Function for displaying communication with AI assistant"""
        feature_description = self.bogui.create_message(
            'Enter a natural language prompt. The AI assistant will propose code to implement your request.'
            )

        api_key_label = self.bogui.create_label('Enter your Open AI key here:')

        api_key_element = widgets.HBox([
            api_key_label, 
            widgets.VBox([
                    self.api_key_input_field,
                    self.bogui.create_error_message(api_key_error, 'red')

                ]),
        ])


        context_label = self.bogui.create_label('Enter your context for the AI assistant here:')
        self.context_input_field.value = 'You are a helpful assistant.'

        context_element = widgets.HBox([
            context_label, 
            widgets.VBox([
                    self.context_input_field,
                    self.bogui.create_error_message(context_error, 'red')

                ]),
        ])

        self.grid = widgets.AppLayout(
        header = api_key_element,
        center= widgets.VBox([
            context_element,
            self.bogui.create_error_message(context_error, 'red'),
            feature_description,
            self.natural_language_prompt,
            self.bogui.create_error_message(nlp_error, 'red')
          ]),
        footer = widgets.HBox([
            self.buttons['send_ai_btn'],
            self.buttons['clear_ai_btn'],
            self.buttons['advanced_ai_btn']
         

        ]),
        pane_widths=[3, 5, 5],
        grid_gap='12px'
        )

        display(self.grid)

       

    def openai_api(self, _=None):

        try:
            openai.api_key = self.api_key_input_field.value
            model_engine = self.model_engine

            system_msg = self.context_input_field.value 
            content = self.natural_language_prompt.value
            response = openai.ChatCompletion.create(
                model = model_engine,
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": content},
            ])

            message = response.choices[0]['message']
            self.display_markdown(message)

        except openai.error.Timeout as e:
            message = self.bogui.create_message(
            f"OpenAI API request timed out: {e}")
            display(message)
            pass

        except openai.error.APIError as e:
            message = self.bogui.create_message(
            f"OpenAI API returned an API Error: {e}")
            display(message)
            pass

        except openai.error.APIConnectionError as e:
            message = self.bogui.create_message(
            f"OpenAI API request failed to connect: {e}")
            display(message)
            pass

    
        except openai.error.InvalidRequestError as e:
            message = self.bogui.create_message(
            f"OpenAI API request was invalid: {e}")
            display(message)
            pass

        except openai.error.AuthenticationError as e:
            message = self.bogui.create_message(
            f"OpenAI API request was not authorized: {e}")
            display(message)
            pass

        except openai.error.PermissionError as e:
            message = self.bogui.create_message(
            f"OpenAI API request was not permitted: {e}")
            display(message)
            pass

        except openai.error.RateLimitError as e:
            message = self.bogui.create_message(
            f"OpenAI API request exceeded rate limit: {e}")
            display(message)
            pass
                

    def display_markdown(self, message):

        print(f"{message['content']}")
    
        # markdown_to_code_btn = self.buttons['insert_code_to_cell']
        
        # content_to_markdown =  """{}""".format(message['content'])
        # self.ai_output = self.utils.create_markdown_cells_below_with_text(1, text = content_to_markdown)
        
        # display(markdown_to_code_btn)
        # display(self.ai_output)
      
    
    def insert_code_to_cell(self, _=None):
        pass
 
        # content = self.ai_output.value
        # first = content.split('```python')[1]
        # second = first.split('```')[0]
        # code = '<code>' + second.strip() + '</code>'
        # print(code)
      
         