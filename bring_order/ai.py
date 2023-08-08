
from ipywidgets import widgets
from IPython.display import display
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
        self.ai_output_grid = None
        self.ai_output = self.bogui.create_message('')
        self.ai_error_message_grid = None
        self.ai_error_msg = self.bogui.create_message('')
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
        self.remove_ai_error_message()
        if self.validate_api_key() and self.validate_npl_input():
            self.openai_api()
    
    def remove_ai_error_message(self):
        self.ai_error_msg = ''
        if  self.ai_error_message_grid is not None:
            self.ai_error_message_grid.close()

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
            self.remove_ai_error_message()
            self.display_ai()
            self.display_ai_output()
        else:
            self.visible = False
            self.close_ai()
            self.ai_output_grid.close()
            self.remove_ai_error_message()

    
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
        footer =
            widgets.HBox([
            self.buttons['send_ai_btn'],
            self.buttons['clear_ai_btn'],
            self.buttons['advanced_ai_btn']
        ]),
        pane_widths=[3, 3, 6],
        pane_heights=[4, 6, 2]
    
        )

        display(self.grid)
        
    
    def display_ai_output(self, _=None):

        self.ai_output_grid = widgets.AppLayout(
            center = self.ai_output
        )
        display(self.ai_output_grid)

    
    def display_ai_error_message(self, _=None):

        self.ai_error_message_grid = widgets.AppLayout(
            center = self.bogui.create_message(self.ai_error_msg)
        )
        display(self.ai_error_message_grid)


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
            self.ai_output.value = self.display_response(message)
      


        except openai.error.Timeout as e:
            self.ai_error_msg = f"OpenAI API request timed out: {e}"
            self.display_ai_error_message()
            pass

        except openai.error.APIError as e:
            self.ai_error_msg = f"OpenAI API returned an API Error: {e}"
            self.display_ai_error_message()
            pass

        except openai.error.APIConnectionError as e:
            self.ai_error_msg = f"OpenAI API request failed to connect: {e}"
            self.display_ai_error_message()
            pass


        except openai.error.InvalidRequestError as e:
            self.ai_error_msg = f"OpenAI API request was invalid: {e}"
            self.display_ai_error_message()
            pass

        except openai.error.AuthenticationError as e:
            self.ai_error_msg = f"OpenAI API request was not authorized: {e}"
            self.display_ai_error_message()
            pass

        except openai.error.PermissionError as e:
            self.ai_error_msg = f"OpenAI API request was not permitted: {e}"
            self.display_ai_error_message()
            pass

        except openai.error.RateLimitError as e:
            self.ai_error_msg = f"OpenAI API request exceeded rate limit: {e}"
            self.display_ai_error_message()
            pass

  
    def display_response(self, message):
        """ Parses, calls formatter and displays response from AI assistant 
        
        """     
        text = self.format_response(message['content'])
        return text
    


    def format_response(self, text):
        """ Formats data description for html widget
        
        Returns:
            formatted_text (str)
        """
   
        formatted_text = '<br />'.join(text.split('\n'))
        code = '<pre>' + formatted_text + '</pre>'

        return code
                

         