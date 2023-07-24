# Software Architecture

## Overview
The code base has been divided into several classes that have their own methods and purposes.
The main class is `BringOrder` and it takes the execution forward by calling other classes.
Data analysis starts with data import that is handled by the `Bodi` class and followed by either hypothesis testing or explorative analysis.
The `Deductive` class takes care of the former and the `Inductive` class of the latter.
All these classes depend on the `BOGui` class that consists of general methods for creating Jupyter widgets and the `BOUtils` class that has methods for executing Javascript inside Jupyter Notebook.

## Class Diagram
Image coming up...

## Class Details
### BringOrder
Creating a [BringOrder](https://github.com/Order-Team/bring-order/blob/main/bring_order/bringorder.py) object inside Jupyter Notebook launches a graphical user interface that takes data analysis forward step by step.

### Bodi
The [Bodi](https://github.com/Order-Team/bring-order/blob/main/bring_order/bodi.py) class takes care of the data import phase.

### Deductive
The hypothesis testing option is handled by the [Deductive](https://github.com/Order-Team/bring-order/blob/main/bring_order/deductive.py) class.

### Inductive
The methods needed in the explorative analysis option can be found in the [Inductive](https://github.com/Order-Team/bring-order/blob/main/bring_order/inductive.py) class.

### BOGui
The [BOGui](https://github.com/Order-Team/bring-order/blob/main/bring_order/bogui.py) class has methods for creating customized Jupyter widgets, such as buttons and input fields, that the user can interact with.
The implementation is based on the [ipywidgets](https://ipywidgets.readthedocs.io/en/stable/) package.
A BOGui object is created automatically with a BringOrder object and then shared with all the Bodi, Deductive, and Inductive objects that this BringOrder object creates.

Methods:
- create_button
- init_buttons
- create_message
- create_error_message
- create_input_field
- create_text_area
- create_label
- create_placeholder
- create_grid
- create_int_text
- create_radiobuttons
- create_file_chooser

### BOUtils
The [BOUtils](https://github.com/Order-Team/bring-order/blob/main/bring_order/boutils.py) class consists of methods that run Javascript inside Jupyter Notebook. They are used to, for example, create, run, and delete code and Markdown cells.
A BOUtils object is also created automatically with a BringOrder object and shared with other created objects.

