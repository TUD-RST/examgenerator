Tutorial
===========

Introduction
-----------------

This tutorial will explain the process behind creating an exam with the exam generator.

Alongside three different examples you will learn step by step how to make use of this project.


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
            template_problem.tex
            template_solution.tex 


Settings
^^^^^^^^^^^^^^^^^^^

Now it is time to configure our settings in ``Math1.json``.

::

    {            
    "title": "Exam for Math 1 (MA1)",   ← The title that will be displayed on the exam
    "variant_name": "Math1",            ← Short handle displayed in the file names
    "semester": "WS 2022/23",           ← Current semester
    "number_of_groups": 3,              ← Let's choose our maximum amount of possible groups
    "copies": 1                         ← We are not using parametirization, therefore copies is set to 1                   
    "page_format_exam": "A4",           ← Students will get their tests printed out in A4 format      
    "page_format_solution": "A5",       ← Solution will be printed in A5 

    "options":{
        "generate_single_pdfs": true,   ← We would like the option to look at the problems for each group seperately
        "generate_sumo_pdf": true,      ← We would like a sumo file
        "delete_temp_data": true        ← Deleteing temporary data is always usefull
    },

    "sumo_options":{                           
        "exam_copies": 15,              ← Total number of students taking the exam
        "solution_copies": 1            ← There is only one solution copy required
    },


    "exams":{                           ← Our exam is created here
        "MathExam": [                   ← Name of the exam
        "MC_easy",                      ← Pool for first problem
        "proofs",                       ← Pool for second problem
        "MC_hard"                       ← Pool for last problem
        ]
    }
    }


Creating the Exam
^^^^^^^^^^^^^^^^^^^

Now that our setup is complete, it is time to create the exam.
Firstly, we have to ensure, we are in the correct working directory - the same
in which our ``settings``, ``pool_data`` and ``templates`` directories lie.

Now in our terminal we can execute the following command:

exam_generator -ct .\\settings\\Math1.json

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

    {
    "title": "Lab Control Theory 2 (ET)",
    "variant_name": "ET2",
    "semester": "WS 2022/23",
    "number_of_groups": 2,
    "copies": 1                             ← No parameterization used
    "page_format_exam": "A5",               ← Students will receive their exams in A5 format
    "page_format_solution": "A4",           ← Solutions in A4 format

    "options":{ 
        "generate_single_pdfs": false,      ← We do not need the tests for each group separately
        "generate_sumo_pdf": true,
        "delete_temp_data": true
    },
    
    "sumo_options":{ 
        "sumo_problem_copies": 30,          ← 30 students
        "sumo_solution_copies": 1
    },
    

    "exams":{ 
        "Lab03": [                          ← First exam
        "A2",
        "B2",
        "CV03"
        ],
        "Lab08": [                          ← Second exam
        "A2",
        "B2",
        "CV08",
        "DV08"
        ],
        "Lab15": [      	                ← Third exam
        "A2",
        "B2",
        "CV15",
        "DV15"
        ]
    }
    }

You could add exams to your liking as long as you follow the json file format structure.

Creating the Exam
^^^^^^^^^^^^^^^^^^^

Lastly, all there is left to do again is execute the following command in the correct directory:

exam_generator -ct .\\settings\\ET2.json

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

Example 3: Parameterization
-----------------------------
Now that you are finally familiar with the basics, we can get to the fun stuff: creating exams with paramaters.
This example will focus on how to implement parameters in your LaTeX problem/ solution files and how you will have 
to adapt your settings to its usage.

Let's again create a very simple math exam, using paramaters.

Setup
^^^^^^^^^^^^^^^^^^^
Our directory setup is exavtly the same as before. We only need to focus on the content of the problem/ solutions files
in which we would like to implement randomly generated numbers. 
In this example we will look at problem_2.tex and its solution.
::

    C:.                                 ← Our current working directory                  
    ├───pool_data                       ← Directory for all different pool directories                
    │   └───easy_calculations           ← Pool with easy multiple choice questions
    │           problem_1.tex           
    │           problem_2.tex           ← Problem with parameters
    │           problem_3.tex           
    │           solution_1.tex
    │           solution_2.tex          ← Solution to parameter problem
    │           solution_3.tex
    │
    ├───settings                        
    │       Math2.json                  ← Settings file 
    │
    └───templates                       ← LaTeX Templates
            template_problem.tex
            template_solution.tex

Problem/ Solution Files
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Our problem will consist of three different smaller problems or ``items``, increasing in difficulty.
Firstly, the students have to guess the correct number (randomly generated in the solution) between one and ten.
Secondly, they are asked to calculate the sum of two numbers.
Lastly, they need find the product of two large numbers.

Since the both the first parameters called in the second and third item are provided with the same key and 
bounds, it will generate replace them with the same exact number.

Content of problem_2.tex:
::

    \begin{Problem}
    Answer the following problems!
    \item I am thinking of a number between 1 and 10. What is that number? \Pts{1}
    \item ${{context.rnum(__KEY1__, 1000, 2000)}} + {{context.rnum(__KEY2__, 20, 30)}}$ =   ? \Pts{2}
    \item ${{context.rnum(__KEY1__, 1000, 2000)}} \cdot {{context.rnum(__KEY3__, 55555, 66666)}}$ =    ? \Pts{2}
    \end{Problem}

Please note that you have to include ``$`` at the beginning *and* the end of each expression in order for the compiler
to be able to properly do its job.

Now to our solution file, where we would like to not only include the question, but also the answer.

Content of solution_2.tex:
::

    \begin{Solution}
    The solution is the following:
    \item I am thinking of a number between 1 and 10. What is that number? - ${{context.rnum(__KEY4__, 1, 10)}}  \Pts{1}
    \item ${{context.rnum(__KEY1__, 1000, 2000)}} + {{context.rnum(__KEY2__, 20, 30)}} = {{context.rnum(__KEY1__, 1000, 2000)} + {context.rnum(__KEY2__, 20, 30)}}$ \Pts{2}
    \item ${{context.rnum(__KEY1__, 1000, 2000)}} \cdot {{context.rnum(__KEY3__, 55555, 66666)}} = {{context.rnum(__KEY1__, 1000, 2000)} * {context.rnum(__KEY3__, 55555, 66666)}} \Pts{2}
    \end{Problem}

It is important to notice that when actually performing calculations with the given values the placement of the curly braces ``{{}}`` changes.
One bracket pair always wraps around the *context.rnum* function call, while the other wraps around the entire ,to be calculated, expression.
This is very well seen when looking at the third item of our solution.

.. hint::
    
    Every student will have different randomly generated values in their exam. Even within groups, these values will differ.

Settings
^^^^^^^^^^^^^^^^^^^

Let's create an exam with three problems from *the easy_calculations* pool for a total of 30 students and
three different groups. Since we only have three problem/ solution pairs, every group will have the same problems,
but in a different order.

::

    {
    "title": "Math for Beginners (MA)",
    "variant_name": "MA 2",
    "semester": "WS 2022/23",
    "number_of_groups": 2,
    "copies": 30                            ← We have 30 total students and are using parametirization
    "page_format_exam": "A5",               ← Students will receive their exams in A5 format
    "page_format_solution": "A4",           ← Solutions in A4 format

    "options":{ 
        "generate_single_pdfs": true,       ← We will have the tests for each group
        "generate_sumo_pdf": true,
        "delete_temp_data": true
    },
    
    "sumo_options":{ 
        "exam_copies": 1,                   ← When using parameterization this should be set to 1!
        "solution_copies": 1                ← We only need one copy of the solutions
    },
    

    "exams":{ 
        "Math 101": [                          
        "easy_calculations",
        "easy_calculations",
        "easy_calculations"
        ]
    }

Creating the Exam
^^^^^^^^^^^^^^^^^^^

Lastly, all there is left to do again is execute the following command in the correct directory:

exam_generator -ct .\\settings\\Math2.json

Our exam directory will be created and the result is the following:

::  

    C:.
    ├───Exams-ET2-WS202223
    │       Exam-MA2-Math101-1-Solution.pdf    ←  Solution for group one
    │       Exam-MA2-Math101-1.pdf             ←  Exams for group one
    │       Exam-MA2-Math101-2-Solution.pdf
    │       Exam-MA2-Math101-2.pdf
    │       Exam-MA2-Math101-3-Solution.pdf
    │       Exam-MA2-Math101-3.pdf
    │       Sumo-MA2-Problems.pdf              ←  Sumo with all problems with every group of the exam
    │       Sumo-MA2-Solutions.pdf             ←  Sumo with all solutions
    │
    ├───pool_data
    │
    ├───settings
    │
    └───templates


We succesfully created an exam with paramaters!
Now you can simply print everything in the format of your choice.