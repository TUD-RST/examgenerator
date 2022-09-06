from multiprocessing import pool
import pytest

from exam_generator import classes
from exam_generator import customExceptions

file_names_tex = [
    "problem_A1_1.tex",
    "problem_A1_2.tex",
    "problem_A1_3.tex",
    "problem_B1_1.tex",
    "problem_CV03_1.tex",
    "solution_A1_1.tex",
    "solution_A1_2.tex",
    "solution_A1_3.tex",
    "solution_CV03_1.tex",
]


def test_pool_working(file_names_tex):
    test_pool = classes.Pool("A1", file_names_tex)

    error = False

    if test_pool.name != "A1":
        error = True

    stack = [
        ("problem_A1_1.tex", "solution_A1_1.tex"),
        ("problem_A1_2.tex", "solution_A1_2.tex"),
        ("problem_A1_3.tex", "solution_A1_3.tex"),
    ]
    if test_pool.stack_available != stack:
        error = True

    assert error == False


def test_Pool_noData(file_names_tex):
    with pytest.raises(customExceptions.MissingFileError):
        test_pool = classes.Pool("D", file_names_tex)


def test_Pool_noCorrespondingSolution(file_names_tex):
    with pytest.raises(customExceptions.MissingFileError):
        test_pool = classes.Pool("B1", file_names_tex)


def test_Pool_pull_working(file_names_tex):
    pool = classes.Pool("A1", file_names_tex)

    prob_sol = pool.pull()

    stack = [
        ("problem_A1_1.tex", "solution_A1_1.tex"),
        ("problem_A1_2.tex", "solution_A1_2.tex"),
        ("problem_A1_3.tex", "solution_A1_3.tex"),
    ]

    prob_sol_from_stack = False
    if prob_sol in stack:
        prob_sol_from_stack = True

    stack.remove(prob_sol)

    assert prob_sol_from_stack and pool.stack_available == stack


def test_Pool_pull_exhausted():
    pool = classes.Pool("CV03", file_names_tex)

    pool.pull()

    with pytest.raises(customExceptions.CompilingError):
        pool.pull()
