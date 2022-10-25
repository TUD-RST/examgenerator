from unittest import result
import pytest
import os
import json
from addict import Dict

from exam_generator import funcs, customExceptions

# Currently not running since problem content creation works with os.getcwd() leading to wrong directory when testing
"""
def test_generate_tex_files_working():
    
    Tests if the correct list of PDF file names is returned.
    

    # setup like the main function would do normally
    current = os.getcwd()
    root_path = os.path.join(os.getcwd(), "test_directories", "generate_tex_files_1")
    settings_path = os.path.join(root_path, "settings", "test.json")
    template_path = os.path.join(root_path, "templates")
    pool_path = os.path.join(root_path, "pool_data")

    with open(settings_path, "r") as json_file:
        settings_dictionary = json.load(json_file)

    settings = Dict(settings_dictionary)

    pool_info = funcs.pull_pool_data(pool_path)

    test_list = funcs.create_custom_test_list(settings.exams, pool_info)

    tests_per_group = funcs.combining_problems(settings.number_of_groups, test_list)

    copies_per_group = funcs.determine_copies_per_group(settings.number_of_groups, settings.copies)

    funcs.generate_tex_files(
        pool_path,
        template_path,
        settings.number_of_groups,
        test_list,
        settings.variant_name,
        settings.title,
        settings.semester,
        tests_per_group,
        copies_per_group
    )
    # deletinjg the created files
    os.chdir(pool_path)
    funcs.delete_command()
    os.chdir(current)"""


def test_generate_tex_files_Error():
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

    pool_info = funcs.pull_pool_data(pool_path)

    test_list = funcs.create_custom_test_list(settings.exams, pool_info)

    tests_per_group = funcs.combining_problems(settings.number_of_groups, test_list)

    copies_per_group = funcs.determine_copies_per_group(
        settings.number_of_groups, settings.copies
    )

    with pytest.raises(customExceptions.MissingFileError):
        file_names_pdf = funcs.generate_tex_files(
            pool_path,
            template_path,
            settings.number_of_groups,
            test_list,
            settings.variant_name,
            settings.title,
            settings.semester,
            tests_per_group,
            copies_per_group,
        )
