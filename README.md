[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Exam Generator

Exam_generator is a script which is designed to create exams/ tests from 
pools of problems while ensuring that there will be no repetition amongst
different groups.

## Current Status and Issues

This project is currently in the development process and is set to release at the end of October 2022.

You can find the current issues [here](https://github.com/TUD-RST/examgenerator/issues)

## Documentation

Documentation for this project including a detailed user guide, tutorials and the API doc is available
in this repository.

## Example

The exam generator allows quick creation of tests and exams.

With the following *directory setup*...

    C:.                                 ← Our current working directory                  
    ├───pool_data                       ← Directory for all different pool directories                
    │   ├───MC_easy                     ← Pool with easy multiple choice questions
    │   │       problem_1.tex
    │   │       problem_2.tex
    │   │       solution_1.tex
    │   │       solution_2.tex
    │   │
    │   └───MC_hard                     ← Pool with hard multiple choice questions
    │           problem_4.tex
    │           problem_5.tex
    │           solution_4.tex
    │           solution_5.tex 
    │
    ├───settings                        
    │       Math1.json                  ← Settings file 
    │
    └───templates                       ← LaTeX Templates
            template_problem.tex
            template_solution.tex 

in combination with these *settings*...

```
    {            
    "group_pairs": 2,                   ← Let's choose our maximum amount of possible groups                   
    "title": "Exam for Math 1 (MA1)",   ← The title that will be displayed on the exam
    "variant_name": "Math1",            ← Short handle displayed in the file names
    "semester": "WS 2022/23",           ← Current semester

    "sumo":{                           
        "pages_per_sheet_test": 2,       ← Students will get their tests printed out in A4 format      
        "sumo_problem_copies": 1,        ← Amount of copies of each group
        "pages_per_sheet_solution": 2,   ← Solution will be printed in A4 as well
        "sumo_solution_copies": 1        ← There is only one solution copy required
    },

    "data":{
        "generate_single_pdfs": true,    ← We would like the option to look at the problems for each group seperately
        "generate_sumo_pdf": true,       ← We would like a sumo file
        "delete_temp_data": true         ← Deleteing temporary data is always usefull
    },

    "test_types":{                       ← Our exam is created here
        "MathExam": [                    ← Name of the exam
        "MC_easy",                       ← Pool for first problem
        "proofs"                         ← Pool for second problem
        ]
    }
    }
```

we can easily create an exam, looking like this:

![Problem](./docs/readme/problem.png)



