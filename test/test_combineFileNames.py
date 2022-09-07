import pytest

from exam_generator import funcs


def test_combine_file_names():
    pool_info = [
        (["problem_A1_1.tex", "solution_A1_1.tex"], "poolA"),
        (["problem_B1_1.tex", "solution_B1_1.tex"], "poolB"),
    ]

    result = [
        "problem_A1_1.tex",
        "solution_A1_1.tex",
        "problem_B1_1.tex",
        "solution_B1_1.tex",
    ]

    assert funcs.combineFileNames(pool_info) == result
