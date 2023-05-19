# bring-order
![GitHub Actions](https://github.com/Order-Team/bring-order/workflows/CI/badge.svg)
[![GitHub](https://img.shields.io/github/license/Order-Team/bring-order)](LICENSE.md)

## Documentation
* [Product backlog](https://docs.google.com/spreadsheets/d/1xqybqVAUIn4vhW-fBfhInQun7nY-uYH79M6l8oCiAzg/edit#gid=0)

## Installation

### Dependencies 

2. Install [**Jupyter**](https://jupyter.org/install)

```bash
poetry add notebook
```

3. Add [**py2nb**](https://github.com/williamjameshandley/py2nb)

```bash
poetry add py2nb
```

### Execute program

1. Go into virtual environment

```bash
poetry shell
```

2. Run in project folder. A *hypothesis.ipynb* file should appear in /src - folder.

```bash
py2nb src/hypothesis.py
```

3. Run in project folder

```bash
jupyter notebook
```

4. Go to the address where the Jupyter Notebook- server is running on localhost. Navigate to **src/hypothesis.ipynb**


5. Push the **|>** button in the up left corner. Wait for kernel to start. 


6. Insert your *hypothesis* and *null hypothesis* to the fields. E.g. *x=0* and *x>0*



## Run unittests

1. Run from main folder

```bash
pytest src
```