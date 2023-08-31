# bring-order
![GitHub Actions](https://github.com/Order-Team/bring-order/workflows/CI/badge.svg)
[![codecov](https://codecov.io/gh/Order-team/bring-order/branch/main/graph/badge.svg?token=e8bdd46f-46b0-410c-820b-84ffca9ca53c)](https://codecov.io/gh/Order-team/bring-order)
[![GitHub](https://img.shields.io/github/license/Order-Team/bring-order)](LICENSE.md)

The tool is aimed at guiding data scientists with their analysis using custom widgets inside Jupyter Notebook.
User can import and prepare data for analysis, add limitations and perform deductive or inductive analysis.
Deductive analysis asks the user to set the hypothesis and null hypothesis, run their analysis, and confirm one of the hypotheses.
Inductive analysis is an option to perform explorative analysis and write notes about it.


## Documentation
* [Product backlog](https://docs.google.com/spreadsheets/d/1xqybqVAUIn4vhW-fBfhInQun7nY-uYH79M6l8oCiAzg/edit#gid=0)

* [Definition of Done](https://github.com/Order-Team/bring-order/blob/main/documentation/DoD.md)

* [Minutes of meetings](https://drive.google.com/drive/folders/1kwXCKbx7egHf8qYDIb4fRffNnad6Qd1t)

## Installation
### Installation from PyPi

### Linux

- If you don't have Jupyter Notebook installed, install it with
```bash
    pip install notebook
```

- If you don't have ipywidgets installed, install it with

```bash
    pip install ipywidgets
```

- If you have an old version of ipywidgets installed, upgrade it with

```bash
    pip install --upgrade ipywidgets
```

- Install bring-order extension:
```bash
    pip install bring-order
```

### Windows

- If you don't have PIP installed, it is recommended to use Anaconda environment

- Install Anaconda with [Anaconda download](https://www.anaconda.com/download)

- Use Anaconda Powershell prompt instead of regular Powershell or Command prompt

- Install bring-order extension:
```bash
    pip install bring-order
```

### MacOS
- If you don't have ipywidgets installed, install it with
```bash
    python3 -m pip install "ipywidgets"
```
- If you have an old version of ipywidgets installed, upgrade it with
```bash
    python3 -m pip install --upgrade ipywidgets
```
- Install bring-order extension:
```bash
    python3 -m pip install "bring-order"
```

### Usage

- Open Jupyter Notebook with
```bash
    jupyter notebook
```

- In Jupyter Notebook execute

``` 
    from bring_order import BringOrder
    BringOrder()
```

A more detailed user manual can be found in the [User Guide](https://github.com/Order-Team/bring-order/blob/main/documentation/user_guide.md)

## Development and Testing

### Links to development documentation

[Architecture](https://github.com/Order-Team/bring-order/blob/main/documentation/architecture.md)

[Testing report](https://github.com/Order-Team/bring-order/blob/main/documentation/testing_report.md)

[Suggestions for improvements](https://github.com/Order-Team/bring-order/blob/main/documentation/suggestions_for_improvement.md)

### Dependencies
- Clone the project and install dependencies in the main folder

```bash
    poetry install
```
- Navigate to main folder and go to the virtual environment

```bash
    poetry shell
```

### Testing

#### Run unit tests

```bash
    pytest tests
```
or use Invoke

```bash
    invoke tests
```
or generate Covegare report
```bash
    invoke coverage
```

#### Run style check

```bash
    pylint bringorder
```
or use Invoke

```bash
    invoke lint
```

#### Run robot tests

```bash
    ./run_robot_tests.sh
```
or use Invoke
```bash
    invoke robottests
```
#### Run pylint, unit tests, and robot tests at once

```bash
invoke alltests
```
