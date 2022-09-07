import pytest
import os

from exam_generator import funcs
from exam_generator import customExceptions


def test_check_directory_true():
    directory = os.path.join(os.getcwd(), "test_directories", "checkDirectory_1")
    directory_valid = funcs.check_directory(directory)
    assert directory_valid == True


def test_check_directory_error1():
    directory = os.path.join(os.getcwd(), "test_directories", "checkDirectory_2")
    with pytest.raises(customExceptions.MissingDirectoryError):
        funcs.check_directory(directory)


def test_check_directory_error2():
    directory = os.path.join(os.getcwd(), "test_directories", "checkDirectory_3")
    with pytest.raises(customExceptions.MissingDirectoryError):
        funcs.check_directory(directory)
