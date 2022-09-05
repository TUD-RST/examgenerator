User Doc
===========

This script creates tests based on given problems and settings
From a pool of problems, test will be created in  a way, that there will be no
repetition for all experiments and groups.
There is two LaTeX templates in the Templates Directory:
One for the problems and one for the sample solution and evaluation.
In these templates there is placeholders, which will be replaced by
this script.
The problems are located in the Aufgaben directory which is furthermore separated into
the main pools (PoolA, PoolB, PoolC, PoolD). They usually differ between general problems,
that are used in every test, and problems, that are specific for the given experiment.
Tests are combined via instances of the class TestTyp and managed via instances of the class Pool.
Solutions are saved in separate files.
Files for problems have the prefix "aufgabe_", solutions the prefix "loesung_".
The scheme is the following: 
 aufgabe_A1_2.tex -> 2. problem of type A1
or for an experiment:
 aufgabe_CV03_1.tex -> 2. problem from experiment (V) number 03 of type C
for a more detailed breakdown of the nomenclature view the read.me file in the Aufgaben folder
Please avoid using combinations of more than one capital letter describing your pools
except for combinations with V (which stands for experiment) since this could lead to 
problems during the compiling process.
Subtasks of a problem should be structured in an enumerate-surrounding.
Within the solution files the solution text has to be written in between
\begin{Loesung} \end{Loesung}. The solution of every subtask starts with the 
key \lsgitem.
It is possible to assign points to problems and solutions with the macro \Pkte{n}.
During the compiling process the given points will be added automatically for the entire test
Optionally, all tests and sample solutions can be combined into one "sumo-file". 
This allows creating the tests for the entire semester in one go. However, this
is only useful if the problems and solutions are final and will not have to be corrected
afterwards.
There is the following options for the test creation, which can be configured in a
json settings file:
  
 * group_pairs:
 Determines the amount of group pairs
 for example:  6 => group pairs 01-12
  
 * variant_name:
 Name of the variant/ degree the test is created for 
 There already exists prefactored tests for:
 * ET1
 * ET2
 * MT
 * RES
 If you would like to create a custom test, you have a free choice with the name
  
 * semester:
 Current Semester
 for example: WS 2021/22
  
 * pages_per_page_test:
 4 - double paged A5
  
 * sumo_number_copies:
 Number of copies per test
  
 * pages_per_page_solution:
 4 - double paged A5
  
 * sumo_solution_copies:
 Number of solution copies
  
 * generate_single_pdfs:
 Should individual pdf files be created for each problem/ solution (true/ false)
  
 * generate_sumo_pdf:
 Should a sumo-file be created (true/ false)
  
 * delete_temp_data:
 Should temporary data be deleted (true; false)
 true is recommended unless there is issues with compiling
  
 * use_custom_test:
 Should a custom test with self-defined test types and lists be created? (true/ false)
 If you would like to use a prefactored test, this setting has to be on false!
  
 If you would like to create a custom test, you will have to provide the test types
 as lists in the json settings file. 
 The first argument of the list is the name of the test type and all following arguments
 are the pools to be used for the test.
  
  
Calling Syntax:
-------------
This script can either be called with the help of a python interpreter
or --in case python is not installed on the working computer-- as a
stand-alone application. The second scenario only works on Windows.
**Syntax when using a python interpreter**::
  
 python etest_generator.py [-h] [-ct] SETTINGS_FILE [-ma] [-mp] POOL [-ms] PROBLEM
  
**Syntax for the stand-alone application**::
  
 etest_generator.exe [-h] [-ct] SETTINGSFILE [-ma] [-mp] POOL [-ms] PROBLEM
  
Based on the sample template it is possible to create as many settings templates to your
liking. They have to be saved in the Einstellung directory.
With these it is now possible to easily create tests:
  
 * -ct [name of the chosen settings file.json] (--create_test [name of the chosen settings file.json])
 creates a folder in which the created tests, based on the provided settings, are saved
  
Additionally, the script can help with the creation/ review of problems/ solutions:
  
 * -ma (--make_all) 
 creates a folder Previews in which a file with a preview for every problem/ solution is displayed
  
 * -mp [Pool] (--make_pool [Pool]) 
 creates a preview file for all problems/ solutions for the given pool
  
 * -ms [name of the problem] (--make_specific [name of the problem]) 
 creates a preview file for the given problem
 name of the problem without ".tex"
In order to receive help type:
  
 * -h (--help)
This script uses operating commands, which are currently only implemented on Windows.