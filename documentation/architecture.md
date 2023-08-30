# Software Architecture

## Overview
The code base has been divided into several classes that have their own methods and purposes.
The main class is `BringOrder` and it takes the execution forward by calling other classes.
Data analysis starts with data import that is handled by the `Bodi` class and followed by either hypothesis testing or explorative analysis. The `Deductive` class takes care of the former and the `Inductive` class of the latter. The `NextAnalysis` class has methods for starting new analysis and closing BringOrder. 

The `Bodi` class depends on `Limitations` and `Stattests` classes. `Limitations` manages data limitations throughout the analysis, and `Stattests` is used to perform some statistical tests on the data under examination.

The `BOVal` class handles the validation of text inputs, and the`Ai` class provides an interface to OpenAI.

Most of the classes depend on the `BOGui` class that consists of general methods for creating Jupyter widgets, and the `BOUtils` class that has methods for executing Javascript inside Jupyter Notebook.

## Class Diagram
In this simple class diagram of BringOrder, the main class is coloured red, the classes handling the analysis phases are green, the support classes are purple, and interface class is blue.

![Class diagram](./pictures/classdiag_simple.png)

More detailed class diagrams:

- [Class diagram with functions](./pictures/classdiag_with_functions.png)
- [Full Class diagram with class variables and functions](./pictures/class_diagram_plain.png)

## Class Responsibilities

### BringOrder
Creating a [BringOrder](https://github.com/Order-Team/bring-order/blob/main/bring_order/bringorder.py) object inside Jupyter Notebook launches a graphical user interface that takes data analysis forward step by step. This class creates objects of other classes and contains the main loop that takes care of the program execution.

### Bodi
The [Bodi](https://github.com/Order-Team/bring-order/blob/main/bring_order/bodi.py) (BringOrder data import) class begins the analysis workflow by collecting the basic information of the study, importing the data, loading the configuration file (bringorder.cfg, optional), and checking data limitations.

### Deductive
The [Deductive](https://github.com/Order-Team/bring-order/blob/main/bring_order/deductive.py) class guides the user through hypothesis testing. The steps include summarizing theory, setting the hypotheses, running some analysis code, and drawing a conclusion.

### Inductive
The [Inductive](https://github.com/Order-Team/bring-order/blob/main/bring_order/inductive.py) class guides the user through explorative analysis, which includes stating the preconceptions, running some analysis code, submitting observations and summarizing them, and finally, evaluating the analysis.

### Ai
The [Ai](https://github.com/Order-Team/bring-order/blob/main/bring_order/ai.py) class is an interface to [OpenAI](https://openai.com/about), and it also provides the user interface for the AI assistant. BringOrder creates an Ai object and switches control to it whenever the user opens the AI assistant.

### BOGui
The [BOGui](https://github.com/Order-Team/bring-order/blob/main/bring_order/bogui.py) (BringOrder GUI) class has methods for creating customized Jupyter widgets, such as buttons and input fields, that the user can interact with.
The implementation is based on the [ipywidgets](https://ipywidgets.readthedocs.io/en/stable/) package.
A BOGui object is created automatically with a BringOrder object and then shared with all the Bodi, Deductive, Inductive, Ai, NextAnalysis, Limitations, and Stattests objects.

### BOUtils
The [BOUtils](https://github.com/Order-Team/bring-order/blob/main/bring_order/boutils.py) class consists mainly of methods that run Javascript inside Jupyter Notebook. They are used to, for example, create, run, and delete code and Markdown cells. There are also methods for creating a PowerPoint presentation of the analysis and for extracting Python code from the AI response and formatting it so that it can be inserted into a code cell. 
A BOUtils object is also created automatically with a BringOrder object and shared with other created objects.

### BOVal
The [BOVal](https://github.com/Order-Team/bring-order/blob/main/bring_order/boval.py) (BringOrder Validation) class validates text inputs: it checks that the input fields are not left blank and that they don't contain certain special characters. Within the Deductive class, it is also used to analyze sentence structure using the language model en_core_web_sm-3.6.0.

### NextAnalysis
The [NextAnalysis](https://github.com/Order-Team/bring-order/blob/main/bring_order/next_analysis.py) class handles the switch from one analysis to another. It also includes the methods needed in the closing phase: saving/deleting the PowerPoint presentation, and exporting the notebook to pdf.

### Stattests
The [Stattests](https://github.com/Order-Team/bring-order/blob/main/bring_order/stattests.py) class handles some statistical testing for imported data. It checks the normal distribution of numerical data and provides an option for testing the independency of categorical variables.


## Description of functionality
When BringOrder is called, it starts with initialization (see [Sequence diagram of initialization](./pictures/BO_init_seqdiag.png)) where also the supporting class objects of BOGui, BOUtils, BOVal, and NextAnalysis, as well as the Ai class, are initialized. After this, BringOrder starts by calling the bring_order function. This starts the main loop and initializes a Bodi object with Stattests and Limitations objects.


- [Sequence diagram of initialization](./pictures/BO_init_seqdiag.png)
- [Sequence diagram of Bodi](./pictures/BO_Bodi_seqdiag.png)
- [Sequence diagram of the mainloop in BringOrder](./pictures/BO_mainloop_seqdiag.png)
