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

Furthermore, this script allows you to create problems with randomly generated paramaters. 
In order to implement a random number within given bounds, you can call ``${{context.rnum(__KEY__, lower_bound, upper_bound)}}$``.
The ``KEY`` gives you the option to reuse the same number within a problem/ solution. It follows a simple structure: ``__KEY{number}__``.
Therefore, in order to reuse a number you can for example provide ``__KEY1__`` within all calls of the context.rnum function, 
where the same value is required. While those random values do transfer over to the according solution files, they do not affect unlinked problems.
This paramaterization can also be used to calculate the solutions for your given problems, simply by providing your formula with the according
random values. More information on how to implement paramaterization into your exams is given in our third tutorial. 
   

Problem example:
::
   
   This is an example problem.
   \begin{Problem}
   \item Are you happy? \Pts{10}
   \item What is ${{context.rnum(__KEY1__, 1, 100)}} + {{context.rnum(__KEY2__, 1, 100)}}$? \Pts{5}
   \end{Problem}


Solution example:
::

   The solution is the following:
   \begin{Solution}
   \solitem Are you happy? - Yes \Pts{10}
   \solitem ${{context.rnum(__KEY1__, 1, 100)}} + {{context.rnum(__KEY2__, 1, 100)}} = {{context.rnum(__KEY1__, 1, 100) + context.rnum(__KEY2__, 1, 100)}}$ \Pts{5}
   \end{Solution}

.. hint::
   This problem/ solution pair will ask the student to evaluate the sum of two random numbers between 1 and 100 and will provide
   the solution file with the correctly calculated solution.

Settings
--------------------

There are the following options for the exam creation, which can be configured 
in a json settings file:

-  *title*: Title of the exam

-  *variant_name*: Typically the name of the degree/ lab the exam is created for.
   This will only show in the created file names, not on the actual exams.

-  *semester*: Current Semester for example: "WS 2022/23"

-  *number_of_groups*: Determines the number of different groups.

-  *copies*: When using paramaterization, this is the number of students who are taking the exam. 
   
-  *page_format_exam*: Set this according on the planned printing format - Opions are "A4" or "A5"

-  *page_format_solution*: Set this according on the planned printing format - Opions are "A4" or "A5"

- options
   -  *generate_single_pdfs*: Should individual pdf files be created for each
      exam (true/ false) 
   -  *generate_sumo_pdf*: Should a sumo-file be created (true/ false)

   -  *delete_temp_data*: Should temporary data be deleted (true; false) true
      is recommended unless there is issues during the compiling process

.. hint::
   Enabling *generate_sumo_pdf* allows creating the tests for the entire semester in
   one go. However, this is only useful if the problems and solutions are
   final and will not have to be corrected afterwards. 

- sumo_options
   -  *solution_copies*: Number of solution copies in the sumo file
   -  *exam_copies*: Number of copies per exam in the sumo file. 

.. hint::
   The final amount of copies is determined by the product of *copies* and *exam_copies*.

   When using *paramaterization* in any of your exam problems, ``copies`` is determined by the total 
   number of students taking the exam and ``exam_copies```should therefore be set to 1, unless you would
   like to have more copies of the entire exam.
   On the other hand when **not** using paramaterization, copies should be set to 1 and exam_copies should 
   be set to the total amount of students taking the exam. This allows you to print every individual exam as
   often as you like, without having to always print all questions for a predetermined amount of students.

- *exams*: This is where you will be able to build your exams out of your pools.
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

