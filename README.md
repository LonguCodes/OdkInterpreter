# ODK Interpreter

## Introduction

ODK is the name I gave to a programming notation designed by dr. Zdzisław Onderka of AGH University of Science and Technology.
The notation description and examples can be found [here](#)

### Base use cases

This program WON'T check if your program is written according to the task.
It will only check if it returns if the code is written according to the notation and execute it.

### Disclaimer

There may be errors! The Interpreter should execute every correct syntax but also may execute some incorrect ones! You can post issues when you find that kind of problem.

The interpreter may also have some other problem. Reporting any issues will be helpful.

## Usage

You can download compiled version for windows and linux from the releases tab.

To you the program, open the command line and execute the program with `--file <PATH TO THE FILE>` where `<PATH TO THE FILE>` should be replaced with the relative/absolute path to the file where the script is.
The results will be in `results.txt` file next to the program. 

You can also add `--output <PATH TO THE RESULTS>` which will place the results in a different file, where `<PATH TO THE RESULTS>` is the path where you want the results.

### Results

The results file will have final values of every variable that was in the notation.

## Code 

I will write some description here. Someday