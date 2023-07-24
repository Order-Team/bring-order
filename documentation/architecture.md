# Software Architecture

## Overview
The code base has been divided into several classes that have their own methods and purposes.
The main class is `BringOrder` and it takes the execution forward by calling other classes.
Data analysis starts with data import that is handled by the `Bodi` class and
followed by either hypothesis testing or explorative analysis.
The `Deductive` class takes care of the former and the `Inductive` class of the latter.
All these classes depend on the `Bogui` class that consists of general methods for creating Jupyter widgets
and the `Boutils` class that has methods for executing Javascript inside Jupyter Notebook.

## Class Diagram
Image coming up...

## Class details
### BringOrder

### Bodi

### Deductive

### Inductive

### Bogui

### Boutils

