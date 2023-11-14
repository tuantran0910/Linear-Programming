# Linear Programming

## Introduction

This practical final project is part of the Linear Programming course in the field of Data Science at VNUHCM - University of Science.

## Usage

### Installation

To install the correct version of Python (version 3.8 or higher) for this project, you can visit the following [link](https://www.python.org/downloads/release/python-380/) to download and install.

To install the necessary libraries, you can use the following command:

```bash
pip install -r ~/requirements.txt
```

This project use the library ```streamlit``` for user interface. To provide the input data for your project, please follow the instructions provided at [How to provide input data]

To start the project:

```bash
python -m streamlit run ~/src/main.py
```

### How to provide input data

First, enter the number of variables and the number of constraints for the linear programming problem. Please make sure to enter each value on a new line.

```text
3
3
```

Enter the objective function according to the following formula: ```min/max c1x1 c2x2 ... cnxn```.

>Please note that when entering the coefficients accompanying the variables in the objective function, separated by a blank space. Use the following convention:
>- For positive coefficients, enter the integer value directly.
>- For negative coefficients, enter the integer value with a "-" sign.

```text
min x1 3x2 2x3
```

Next, enter each constraint of the linear programming problem on separate lines. Enter the coefficients accompanying the variables in the objective function, following the convention where positive coefficients are entered directly as integers and negative coefficients are entered with a "-" sign.

For example, if you have the constraint "2x1 - 3x2 + 4x3 <= 5", you would enter the coefficients as follows:

```text
2x1 -3x2 4x3 <= 5
```

Next, enter the constraint signs for the linear programming problem. Enter the condition for each variable on separate lines, and do not enter anything for variables that are unrestricted.

>For each variable, enter one of the following conditions on separate lines:
>- "<=" for less than or equal to
>- ">=" for greater than or equal to
>- "=" for equality

```text
x1 >= 0
x2 <= 0
```

Finally, click on the "Solve" button to perform the linear programming problem solving.
