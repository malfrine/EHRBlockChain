# EHRBlockChain

For more information regarding the purpose of this document, please see "report.pdf"

## Running the program
Using the IDE of your choice (preferrably PyCharm Community Edition) configure the interpreter to run "main.py."

Ensure you have the following libraries:
  - pandas
  - os
  - timeit

The folder "venv" already has a virtual environment and interpreter with the required libraries installed.

"main.py" required .csv data. The data can be accessed in the following way:
  - if you have access to MIMIC-III run the command in "queries.txt" and export the resultant table as a .csv using DataGrip
    replace data source in "main.py" from "test100.csv" to the name of the .csv file you just exported.

## Program results
The program outputs the following data:
  - "timer.txt"
  - "result.csv" which contains the parsed linked list data based on the project question.
