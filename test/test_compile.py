import pytest
import os
import json
import platform
import subprocess
from addict import Dict

from exam_generator import funcs


def test_compile():
    """
    Expects no error while compiling.
    """
    current = os.getcwd()
    root_path = os.path.join(os.getcwd(), "test_directories", "compile")
    pool_path = os.path.join(root_path, "pool_data")
    settings_path = os.path.join(root_path, "settings", "test.json")

    with open(settings_path, "r") as json_file:
        settings_dictionary = json.load(json_file)

    settings = Dict(settings_dictionary)

    pool_info = funcs.pull_pool_data(pool_path)

    test_list = funcs.create_custom_test_list(settings.exams, pool_info)

    tests_per_group = funcs.combining_problems(settings.number_of_groups, test_list)

    exam_name = (
        "Exams-{}-{}".format(settings.variant_name, settings.semester)
        .replace(" ", "")
        .replace("/", "")
    )
    test_directory = os.path.join(
        root_path,
        exam_name,
    )

    funcs.compile(test_directory, pool_path, settings.data.delete_temp_data)

    # deleting temporary data
    os.chdir(root_path)

    if platform.system() == "Windows":
        command = f"rmdir /s /q {test_directory}"
    elif platform.system() == "Linux":
        command = f"rm -r {test_directory}"

    process = subprocess.Popen(command, shell=True)
    process.wait()

    # switching back to required working directory
    os.chdir(current)
