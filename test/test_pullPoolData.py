import pytest
import os

from exam_generator import funcs
from exam_generator import customExceptions

directory1 = os.path.join(os.getcwd(), "test_directories", "pullPoolData_1")


def test_pullPoolData_correct(directory1):
    result = [
        (["problem_A1_1.tex", "solution_A1_1.tex"], "poolA"),
        (["problem_B1_1.tex", "solution_B1_1.tex"], "poolB"),
    ]

    assert funcs.pullPoolData(directory1) == result


directory2 = os.path.join(os.getcwd(), "test_directories", "pullPoolData_2")


def test_pullPoolData_ignoringFile(directory2):
    result = [
        (["problem_A1_1.tex", "solution_A1_1.tex"], "poolA"),
        (["problem_B1_1.tex", "solution_B1_1.tex"], "poolB"),
    ]

    assert funcs.pullPoolData(directory2) == result


directory3 = os.path.join(os.getcwd(), "test_directories", "pullPoolData_3")


def test_pullPollData_noPools(directory3):
    with pytest.raises(customExceptions.MissingDirectoryError):
        funcs.pullPoolData(directory3)


directory4 = os.path.join(os.getcwd(), "test_directories", "pullPoolData_4")


def test_pullPollData_noPools(directory4):
    with pytest.raises(customExceptions.CompilingError):
        funcs.pullPoolData(directory4)
