import pytest
import os

from exam_generator import funcs
from exam_generator import customExceptions


def test_check_directory_true():
    directory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    directory_valid = funcs.check_directory(directory)
    assert directory_valid == True


def test_check_directory_error():
    directory = os.getcwd()
    with pytest.raises(customExceptions.MissingDirectoryError):
        funcs.check_directory(directory)
