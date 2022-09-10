import pytest
import os

from exam_generator import classes
from exam_generator import funcs
from exam_generator import customExceptions


def test_pool_working():
    """
    Expects Pool class initialisation to work without errors.
    """
    directory = os.path.join(os.getcwd(), "test_directories", "pool_1")

    pool_files_A1 = funcs.pullPoolData(directory)[0][0]

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
    """
    Expects MissingFileError when there is no problems in a given pool.
    """
    pool_files_D = []
    with pytest.raises(customExceptions.MissingFileError):
        test_pool = classes.Pool("D", pool_files_D)


def test_Pool_noCorrespondingSolution():
    """
    Expects a MissingFileError when there is no solution to a problem within a pool.
    """
    pool_files_B1 = ["problem_1.tex"]
    with pytest.raises(customExceptions.MissingFileError):
        test_pool = classes.Pool("B1", pool_files_B1)


def test_Pool_pull_working():
    """
    Checking if pull() methode works.
    """
    directory = os.path.join(os.getcwd(), "test_directories", "pool_1")

    pool_files_A1 = funcs.pullPoolData(directory)[0][0]
    pool = classes.Pool("A1", pool_files_A1)

    prob_sol = pool.pull()

    stack = [
        ("problem_1.tex", "solution_1.tex"),
        ("problem_2.tex", "solution_2.tex"),
        ("problem_3.tex", "solution_3.tex"),
    ]

    prob_sol_from_stack = False
    if prob_sol in stack:
        prob_sol_from_stack = True

    stack.remove(prob_sol)

    assert prob_sol_from_stack and pool.stack_available == stack


def test_Pool_pull_exhausted():
    """
    Expects a CompilingError when more problems are pulled than available.
    """
    pool_files_CV03 = ["problem_1.tex", "solution_1.tex"]
    pool = classes.Pool("CV03", pool_files_CV03)

    pool.pull()

    with pytest.raises(customExceptions.CompilingError):
        pool.pull()
