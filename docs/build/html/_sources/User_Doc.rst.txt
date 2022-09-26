User Doc
========

Introduction
-----------------
exam_generator is a script which is designed to create exams/ tests from 
pools of problems while ensuring that there will be no repetition amongst
different groups. 
The exams/ tests are based off of two major components:
the LaTeX basis (problems, solutions, templates) and user defined settings.


Content Generation
-----------------------


LaTeX Templates
^^^^^^^^^^^^^^^^^^^^^^^
There are two LaTeX templates in the ``templates`` Directory: One for the problems 
and one for the sample solution and evaluation. In these templates there is 
placeholders, which will later be replaced by this script.

Problems/ Solutions
^^^^^^^^^^^^^^^^^^^^^^^

Pools
""""""""""""""""""""""""
Problems and solutions are located in the
``pool_data`` directory which is furthermore separated into *pools*. 
Pools are sets of problems/ solutions of a specfic type. They can for example differ between general
problems, that are used in every test, and problems, that are specific for a given experiment. However,
you may create as many pools following any category/ rule as you like. Pools are the small puzzle pieces
that in the end will decide over the content of your exam. Names can range from *A1* to *ExperimentXYZ*.
You have the freedom of choice.

Naming Scheme
""""""""""""""""""""""""

Problems and solutions are saved in separate files. Files for problems have the prefix ``problem\_``,
solutions the prefix ``solution\_``. 

You may follow up the prefix with any name to your liking, however mind that problem/ solution pairs
have to have the exact same description following the prefix. 

Additionally, please refrain from using "\\" or "/" in your filenames since this will cause compiling errors.

File Content
""""""""""""""""""""""""
Subtasks of a problem should be structured in the ``Problem`` surrounding.
The problem text has to be written between ``\begin{Problem}``, ``\end{Problem}``.
Every subtask starts with the ``\item`` key. 

Within the solution files the solution text has
to be written in between ``\begin{Solution}``, ``\end{Solution}``. 
The solution of every subtask starts with the key
``\solitem``. 

It is possible to assign points to problems and
solutions with the macro ``\Pts{n}``. Where ``n`` is the number of points given at that exact spot.
During the compiling process the given points will be added automatically for the entire test.
Please be aware that if you would like to show points both on the exam and the solutions,
you will have to manually input points in the problem and solution file.

Problem example:
::
   
   This is an example problem.
   \begin{Problem}
   \item What is 2+2? \Pts{1}
   \item Are you happy? \Pts{10}
   \end{Problem}


Solution example:
::

   The solution is the following:
   \begin{Solution}
   \solitem 2+2=4 \Pts{1}
   \solitem Are you happy? - Yes \Pts{10}
   \end{Solution}


Settings
--------------------

There are the following options for the exam creation, which can be configured 
in a json settings file:

-  *group_pairs*: Determines the number of groups.


-  *variant_name*: Typically the name of the degree/ lab the exam is created for.
   This will only show in the created file names, not on the actual exams.


-  *semester*: Current Semester for example: "WS 2022/23"


-  *pages_per_sheet_test*: Set this according on the planned printing format:
   input 2 is intended for an A4 print, 4  for double a  paged A5 print.


-  *sumo_number_copies*: Number of copies per exam in the sumo file


-  *pages_per_page_solution*: Set this according on the planned printing format:
   input 2 is intended for an A4 print, 4  for double a  paged A5 print.


-  *sumo_solution_copies*: Number of solution copies in the sumo file


-  *generate_single_pdfs*: Should individual pdf files be created for each
   exam (true/ false) 


-  *generate_sumo_pdf*: Should a sumo-file be created (true/ false)

.. hint::
   Enabling *generate_sumo_pdf* allows creating the tests for the entire semester in
   one go. However, this is only useful if the problems and solutions are
   final and will not have to be corrected afterwards. 

-  *delete_temp_data*: Should temporary data be deleted (true; false) true
   is recommended unless there is issues during the compiling process

- *test_types*: This is where you will be able to build your exams out of your pools.
   For example: "TestExam": ["A1", "B", "CV03"] will create an exam called TestExam consisting 
   of 3 problems randomly newly drawn from the given pools for each group_pair. A more detailed 
   example of how to create exams is provided in the tutorial.

Directory setup
---------------------
Following everything mentioned previously, your directory has to contain at least the following:

::
   
   ├───pool_data
   │   └───examplePool_1
   │           problem_example1.tex
   │           solution_example1.tex
   │
   ├───settings
   │       settings_example.json
   │
   └────templates                            
           template_problem.tex
           template_solution.tex

However, the number of pools and saved settings files is unlimited.

Features
--------------------

After fighting through the setup process, it is time for fun.
Based on the given settings template it is possible to create as many settings
templates to your liking. They have to be saved in the ``settings``
directory. With these it is now possible to easily create exams:

-  *-ct* [path to the chosen settings file] (–create_test [path to
   the chosen settings file]) creates a folder in which the created
   tests, based on the provided settings, are saved

If you would like to select a new random seed, allowing for different results
when creating the same exam:

- *-rs* [seed]

.. Hint::
   This only works in combination with creating an exam (-ct).


Additionally, the script can help with the creation/ review of problems/
solutions:

-  *-ma* (–make_all) creates a folder Previews in which a file with a
   preview for every problem/ solution is displayed

-  *-mp* [Pool] (–make_pool [POOLPATH]) creates a preview file for all
   problems/ solutions for the given pool

-  *-ms* [PROBLEMPATH] (–make_specific [PROBLEMPATH])
   creates a preview file for the given problem name of the problem
   
  

-  *-h* (–help) for help

Calling Syntax
---------------

After installing the exam_generator with pip:

``pip install exam_generator``

It is now possible to execute the program in every directory, following
the requirements given before. It is recommed to clone the `github repository <https://github.com/TUD-RST/examgenerator>`_.
The repository contains all necessary directories and a few more examples on top.

At the root directory you can now call:

**Syntax when using a python interpreter**


exam_generator [-h] [-ct] SETTINGSPATH [-ma] [-mp] POOLPATH
[-ms] PROBLEMPATH [-rs] SEED


**Syntax for the stand-alone application**

exam_generator.exe [-h] [-ct] SETTINGSPATH [-ma] [-mp] POOLPATH [-ms]
PROBLEMPATH [-rs] SEED

