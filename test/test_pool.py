from multiprocessing import pool
import pytest

from exam_generator import classes
from exam_generator import customExceptions


def test_pool_working():

    pool_files_A1 = [
        "problem_1.tex",
        "problem_2.tex",
        "problem_3.tex",
        "solution_1.tex",
        "solution_2.tex",
        "solution_3.tex",
    ]

    test_pool = classes.Pool("A1", pool_files_A1)

    error = False

    if test_pool.name != "A1":
        error = True

    stack = [
        ("problem_1.tex", "solution_1.tex"),
        ("problem_2.tex", "solution_2.tex"),
        ("problem_3.tex", "solution_3.tex"),
    ]
    if test_pool.stack_available != stack:
        error = True

    assert error == False


def test_Pool_noData():
    pool_files_D = []
    with pytest.raises(customExceptions.MissingFileError):
        test_pool = classes.Pool("D", pool_files_D)


def test_Pool_noCorrespondingSolution():
    pool_files_B1 = ["problem_1.tex"]
    with pytest.raises(customExceptions.MissingFileError):
        test_pool = classes.Pool("B1", pool_files_B1)


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
    pool_files_CV03 = ["problem_1.tex", "problem_2.tex", "solution_1.tex"]
    pool = classes.Pool("CV03", pool_files_CV03)

    pool.pull()

    with pytest.raises(customExceptions.CompilingError):
        pool.pull()
