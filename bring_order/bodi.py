'''Bring Order Data Import (and preparation). 
Creates code cells for importing and cleaning data and markdown cell to describe the limitations
and requirements of data. After code cells displays "ready to analyse" button. After button is 
pressed displays text field and "ready" button. Empty text field is not accepted.'''
from boutils import BOUtils

class Bodi:
    '''Creates code cells for importing data and markdown cell(s) to describe data limitations'''
    def __init__(self):
        self.boutils = BOUtils()

    def add_code_cell(self):
        '''display code cells for importing and cleaning data'''
        self.boutils.create_code_cells(2)

    def data_limits(self):
        '''method to display text field and ready button 

        returns:
            string typed into text field'''
        self.boutils.create_markdown_cell()
        return "Hello World!"

    def bodi(self):
        '''main function'''
        print("Import and prepare your data.")
        '''1. Display 2 code cells and "ready to analyse"-button
        2. After button is pressed, opens text area and "ready"-button.
        3. returns string typed into text area.'''
        return "Hello world!"
