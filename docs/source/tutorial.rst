Tutorial
===========

Introduction
-----------------

This tutorial will explain the process behind creating an exam with the exam generator.

Alongside two different examples you will learn step by step how to make use of this project.


Example 1: Basics
-------------------

Our first example is a simple math exam consisting of three different problem types/ pools.
Goal of this first example is to understand the basic setup/ execution of this project.

Setup
^^^^^^^^^^^^^^^^^^^

As mentioned in the user documentation this project requires a specific directory setup.
Since we would like to create an exam with three different pools, we firstly need to create three subdirectories
in the ``pool_data`` directory. Secondly, we provide each pool with at least as many problem/ solution pairs as
the number of different groups we would like to have. In this case we provide three problem/solution pairs for each
pool, therefore allowing a maximum of three different groups. 
Lastly, we create our ``Math1.json`` settings file in the ``settings`` directory.

Our requirements result in the following structure:


::

    C:.                                 ← Our current working directory                  
    ├───pool_data                       ← Directory for all different pool directories                
    │   ├───MC_easy                     ← Pool with easy multiple choice questions
    │   │       problem_1.tex
    │   │       problem_2.tex
    │   │       problem_3.tex
    │   │       solution_1.tex
    │   │       solution_2.tex
    │   │       solution_3.tex
    │   │
    │   ├───MC_hard                     ← Pool with hard multiple choice questions
    │   │       problem_4.tex
    │   │       problem_5.tex
    │   │       problem_6.tex
    │   │       solution_4.tex
    │   │       solution_5.tex
    │   │       solution_6.tex
    │   │
    │   └───proofs                      ← Pool with proof problems
    │           problem_7.tex
    │           problem_8.tex
    │           problem_9.tex
    │           solution_7.tex
    │           solution_8.tex
    │           solution_9.tex
    │
    ├───settings                        
    │       Math1.json                  ← Settings file 
    │
    └───templates                       ← LaTeX Templates 


Settings
^^^^^^^^^^^^^^^^^^^

Now it is time to configure our settings in ``Math1.json``.

::
                   
    "group_pairs": 3,                   ← Let's choose our maximum amount of possible groups                   
    "title": "Exam for Math 1 (MA1)",   ← The title that will be displayed on the exam
    "variant_name": "Math1",            ← Short handle displayed in the file names
    "semester": "WS 2022/23",           ← Current semester

    "sumo":                           
    "pages_per_sheet_test": 2,          ← Students will get their tests printed out in A4 format      
    "sumo_problem_copies": 5,           ← Amount of copies of each group, total here is 5 copies *3 groups -> 15 students
    "pages_per_sheet_solution": 2,      ← Solution will be printed in A4 as well
    "sumo_solution_copies": 1           ← There is only one solution copy required

    "data":
    "generate_single_pdfs": true,       ← We would like the option to look at the problems for each group seperately
    "generate_sumo_pdf": true,          ← We would like a sumo file
    "delete_temp_data": true            ← Deleteing temporary data is always usefull
    
    "test_types":                       ← Our exam is created here
    "MathExam": [                       ← Name of the exam
    "MC_easy",                          ← Pool for first problem
    "proofs",                           ← Pool for second problem
    "MC_hard"                           ← Pool for last problem
    ]



Creating the Exam
^^^^^^^^^^^^^^^^^^^

Now that our setup is complete, it is time to create the exam.
Firstly, we have to ensure, we are in the correct working directory - the same
in which our ``settings``, ``pool_data`` and ``templates`` directories lie.

Now in our terminal we can execute the following command:

-a exam_generator -ct .\\settings\\Math1.json

A new directory with all requested exams will be created:

:: 

    C:.
    ├───Exams-Math1-WS202223
    │       Exam-Math1-PracticeExam-0102-Solution.pdf
    │       Exam-Math1-PracticeExam-0102.pdf
    │       Exam-Math1-PracticeExam-0304-Solution.pdf
    │       Exam-Math1-PracticeExam-0304.pdf
    │       Exam-Math1-PracticeExam-0506-Solution.pdf
    │       Exam-Math1-PracticeExam-0506.pdf
    │       Sumo-Math1-Problems.pdf
    │       Sumo-Math1-Solutions.pdf
    │
    ├───pool_data
    │
    ├───settings
    │
    └───templates


We achieved our goal of creating a simple math exam with three groups.


Example 2: Multiple Exams
---------------------------

Our second example focuses on creating multiple exams at once.
It will go into further detail regarding the project settings.

We would like to create three exams for three different lab experiments for 
electrical engineers in their 2nd semester.
There is a total of 30 students attending each test and we would like to have
two different groups. Since all of our problems/ solutions are already finalized,
we can create a sumo file containing all three exams and enough copies for each student.

Setup
^^^^^^^^^^^^^^^^^^^

There is a total of eigth pools required for our three exams.
Each pool contains at least two problem/ solution pairs. 

::

    C:.
    ├───pool_data               
    │   ├───A2                          ← Starting problems 
    │   │
    │   ├───B2                          ← Followup problems
    │   │
    │   ├───CV03                        ← Problems for lab 03
    │   │
    │   ├───CV08                        ← Problems for lab 08
    │   │
    │   ├───CV15                        ← Problems for lab 15
    │   │
    │   ├───CV21                        ← Problems for lab 21
    │   │
    │   ├───DV08                        ← Bonus problem for lab 08
    │   │
    │   └───DV15                        ← Bonus problem for lab 15
    │
    ├───settings
    │       ET2.json                    ← Settings file
    │
    └───templates


Settings
^^^^^^^^^^^^^^^^^^^

Our lab exams have the following requirements:
- The first problem is always one of pool *A2*
- The second problem is always one of pool *B2*
- There needs to be at least one lab specific problem 

Furthermore, we need copies for 30 students. With two groups for each test,
that leaves us with 15 copies for our sumo file.

::

    "group_pairs": 2,
    "title": "Lab Control Theory 2 (ET)",
    "variant_name": "ET2",
    "semester": "WS 2022/23",

    "sumo": 
    "pages_per_sheet_test": 4,              ← Students will receive their exams in A5 format
    "sumo_problem_copies": 15,              ← 15*2 -> 30 total copies
    "pages_per_sheet_solution": 2,          ← Solutions in A4 format
    "sumo_solution_copies": 1
    
    "data": 
    "generate_single_pdfs": false,          ← We do not need the tests for each group separately
    "generate_sumo_pdf": true,
    "delete_temp_data": true

    "test_types": 
    "Lab03": [                              ← First exam
    "A2",
    "B2",
    "CV03"
    ],
    "Lab08": [                              ← Second exam
    "A2",
    "B2",
    "CV08",
    "DV08"
    ],
    "Lab15": [      	                    ← Third exam
    "A2",
    "B2",
    "CV15",
    "DV15"
    ]


You could add exams to your liking as long as you follow the json file format structure.

Creating the Exam
^^^^^^^^^^^^^^^^^^^

Lastly, all there is left to do again is execute the following command in the correct directory:

-a exam_generator -ct .\\settings\\ET2.json

Our exam directory will be created and the result is the following:

::  
    
    C:.
    ├───Exams-ET2-WS202223
    │       Sumo-ET2-Problems.pdf
    │       Sumo-ET2-Solutions.pdf
    │
    ├───pool_data
    │
    ├───settings
    │
    └───templates


We created sumo files containing all exams for every lab and every group.
Now you can simply print in your chosen format.
