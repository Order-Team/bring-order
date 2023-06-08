# bring-order
![GitHub Actions](https://github.com/Order-Team/bring-order/workflows/CI/badge.svg)
[![codecov](https://codecov.io/gh/Order-team/bring-order/branch/main/graph/badge.svg?token=e8bdd46f-46b0-410c-820b-84ffca9ca53c)](https://codecov.io/gh/Order-team/bring-order)
[![GitHub](https://img.shields.io/github/license/Order-Team/bring-order)](LICENSE.md)

The tool is aimed at helping data scientists formulate their hypotheses better. When a hypothesis has been formulated clearly, the following is expected after analysis:

- the data analysis environment can state whether the hypothesis was supported or not

- any analysis that was not directly related to hypothesis testing can be identified


## Documentation
* [Product backlog](https://docs.google.com/spreadsheets/d/1xqybqVAUIn4vhW-fBfhInQun7nY-uYH79M6l8oCiAzg/edit#gid=0)

* [Definition of Done](https://github.com/Order-Team/bring-order/blob/main/documentation/DoD.md)

* [Minutes of meetings](https://drive.google.com/drive/folders/1kwXCKbx7egHf8qYDIb4fRffNnad6Qd1t)

## Installation

### Installation from TestPypi

- Install ipywidget extension:

```bash
    pip install ipywidgets
```
- Install testbringorder extention:
```bash
    pip install -i https://test.pypi.org/simple/ testbringorder
```

### Usage

In Jupyter Notebook execute:

``` 
    from bring_order import BringOrder
    bo = BringOrder()
```

## Development

### Dependencies 

- Install dependencies

```bash
    poetry install
```

## Run unittests

1. Run from main folder

```bash
    pytest
```

## Run style check

- Run from main folder

```bash
    pylint bring_order
```

## Run robot tests

- Navigate to the main folder and go to virtual environment

```bash
    poetry shell
```

- Run robot test script

```bash
    ./run_robot_tests.sh
```

If the script won't run, give it execution rights first and try again
```bash
chmod +x run_robot_tests.sh
```

If the first run fails, try once again. Sometimes there are some connection issues.
When you are done, you can exit the virtual environment with command

```bash
exit
```

## Run tests with Invoke

The previous tests can also be run by using Invoke:

1. Go to the main folder

2. If Invoke has not been locally installed, go to Poetry shell:
```bash
poetry shell
```

3. Run Invoke with any of the following:
```bash
invoke tests
```
to run pytests
```bash
invoke lint
```
to run pylint
```bash
invoke robottests
```
to run robottests
```bash
invoke alltests
```
to run all of the above
