from unittest import result
import pytest
import os
import json
from addict import Dict

from exam_generator import funcs, customExceptions

def test_generateTexFiles_working():
    """
    Tests if the correct list of PDF file names is returned.
    """

    # setup like the main function would do normally
    current = os.getcwd()
    root_path = os.path.join(os.getcwd(), "test_directories", "generateTexFiles_1")
    settings_path = os.path.join(root_path, "settings", "test.json")
    template_path = os.path.join(root_path, "templates")
    pool_path = os.path.join(root_path, "pool_data")

    with open(settings_path, "r") as json_file:
        settings_dictionary = json.load(json_file)

    settings = Dict(settings_dictionary)

    pool_info = funcs.pullPoolData(pool_path)

    test_list = funcs.createCustomTestList(settings.test_types, pool_info)

    tests_per_group = funcs.combiningProblems(settings.group_pairs, test_list)

    file_names_pdf = funcs.generateTexFiles(pool_path, template_path, settings.group_pairs, test_list, settings.variant_name, settings.title, settings.semester, tests_per_group)

    result = (["Exam-ET1-test1-0102.pdf"], ["Exam-ET1-test1-0102-Solution.pdf"])

    # deletinjg the created files
    os.chdir(pool_path)
    funcs.deleteCommand()
    os.chdir(current)

    assert file_names_pdf == result


def test_generateTexFiles_Error():
    """
    Expects a MissingFileError becaus eproblem/ solution template not found
    """

    # setup like the main function would do normally
    current = os.getcwd()
    root_path = os.path.join(os.getcwd(), "test_directories", "generateTexFiles_2")
    settings_path = os.path.join(root_path, "settings", "test.json")
    template_path = os.path.join(root_path, "templates")
    pool_path = os.path.join(root_path, "pool_data")

    with open(settings_path, "r") as json_file:
        settings_dictionary = json.load(json_file)

    settings = Dict(settings_dictionary)

    pool_info = funcs.pullPoolData(pool_path)

    test_list = funcs.createCustomTestList(settings.test_types, pool_info)

    tests_per_group = funcs.combiningProblems(settings.group_pairs, test_list)
    
    with pytest.raises(customExceptions.MissingFileError):
        file_names_pdf = funcs.generateTexFiles(pool_path, template_path, settings.group_pairs, test_list, settings.variant_name, settings.title, settings.semester, tests_per_group)   