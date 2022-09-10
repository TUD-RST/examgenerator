import pytest
import os

from exam_generator import funcs


def test_combineFileNames():
    """
    Expects combineFileNames to create the correct joined list.
    """
    
    directory = os.path.join(os.getcwd(), "test_directories", "combineFileNames_1")

    pool_info = funcs.pullPoolData(directory)

    result = [
        "problem_1.tex",
        "solution_1.tex",
        "problem_1.tex",
        "solution_1.tex",
    ]

    assert funcs.combineFileNames(pool_info) == result
