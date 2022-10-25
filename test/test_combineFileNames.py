import pytest
import os

from exam_generator import funcs


def test_combine_file_names():
    """
    Expects combine_file_names to create the correct joined list.
    """

    directory = os.path.join(os.getcwd(), "test_directories", "combineFileNames_1")

    pool_info = funcs.pull_pool_data(directory)

    result = [
        "problem_1.tex",
        "solution_1.tex",
        "problem_1.tex",
        "solution_1.tex",
    ]

    assert funcs.combine_file_names(pool_info) == result
