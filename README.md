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

### Dependencies 

1. Install dependencies

```bash
poetry install
```

### Execute program

1. Go into virtual environment

```bash
poetry shell
```

2. Run in project folder. A *bogui.ipynb* file should appear in /src - folder.

```bash
py2nb src/bogui.py
```

3. Run in project folder

```bash
jupyter notebook
```

4. Go to the address where the Jupyter Notebook- server is running on localhost. Navigate to **src/bogui.ipynb**


5. Add a new code line and write depending on where you are in the project folder ``` from src.bogui import BOGui ```

6. Choose deductive or inductive option

- **Decuctive**:  Insert your *hypothesis* and *null hypothesis* to the fields. E.g. *x=0* and *x>0*
- **Inductive**: 



## Run unittests

1. Run from main folder

```bash
pytest src
```

## Run style check

1. Run from main folder

```bash
pylint src
```

## Run robot tests
1. Navigate to main folder and go to virtual environment

```bash
poetry shell
```

2. Launch Jupyter Notebook

```bash
jupyter notebook
```

3. Copy one of the URLs that you find in the terminal, paste it to ${URL} variable in /src/tests/robot/resource.robot, and save changes.

4. Open another terminal tab, and activate the virtual environment again

```bash
poetry shell
```

5. Run the robot tests

```bash
robot src
```

If the first run fails, try once again. Sometimes there are some connection issues.
When you are done, you can shut down the notebook server by pressing Ctrl+C twice in the same terminal tab where you launched it.
You can exit the virtual environment with command

```bash
exit
```
