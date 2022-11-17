import pytest
import os
import random

from exam_generator import funcs
from exam_generator import classes
from exam_generator import customExceptions


def test_create_custom_test_list_correct():
    """
    Expects create_custom_test_list() to compile a correct list.
    """

    directory = os.path.join(os.getcwd(), "test_directories", "createCustomTestList_1")

    pool_info = funcs.pull_pool_data(directory)

    # test_types resembling the json data
    test_types_dic = {
        "test1": ["A1", "B1", "CV03"],
        "test2": ["A1", "B1"],
    }

    # expected data for comparison
    poolA1 = classes.Pool("A1", pool_info[0][0])
    poolB1 = classes.Pool("B1", pool_info[1][0])
    poolCV03 = classes.Pool("CV03", pool_info[2][0])

    pool_list1 = (poolA1, poolB1, poolCV03)
    pool_list2 = (poolA1, poolB1)

    # checking the function
    custom_test_list = funcs.create_custom_test_list(test_types_dic, pool_info)

    error = False

    if len(custom_test_list) != 2:
        error = True

    # checking first testtype
    testtype1 = custom_test_list[0]

    # TestType name check
    if testtype1.name != "test1":
        error = True

    # TestType pools length check
    if len(testtype1.pools) != len(pool_list1):
        error = True

    pool_list_test1 = testtype1.pools

    # checks if name of random pool in list is correct
    index = random.randint(0, len(pool_list_test1) - 1)

    if pool_list_test1[index].name != pool_list1[index].name:
        error = True

    # checking second testtype
    testtype2 = custom_test_list[1]

    # TestType name check
    if testtype2.name != "test2":
        error = True

    # TestType pools length check
    if len(testtype2.pools) != len(pool_list2):
        error = True

    pool_list_test2 = testtype2.pools

    # checks if name of random pool in list is correct
    new_index = random.randint(0, len(pool_list_test2) - 1)

    if pool_list_test2[new_index].name != pool_list2[new_index].name:
        error = True

    assert error == False


def test_create_custom_test_list_noEntries():
    """
    Expects a SettingsError when no custom test was provided in the json data.
    """
    directory = os.path.join(os.getcwd(), "test_directories", "createCustomTestList_1")

    pool_info = funcs.pull_pool_data(directory)

    # dic representing the json data
    test_types_dic = {}
    with pytest.raises(customExceptions.SettingsError):
        funcs.create_custom_test_list(test_types_dic, pool_info)


def test_create_custom_test_list_pool_error():
    """
    Expects a PoolError when being executed since pool does not contain enough problems
    """
    directory = os.path.join(os.getcwd(), "test_directories", "createCustomTestList_1")

    pool_info = funcs.pull_pool_data(directory)

    # test_types resembling the json data (A1 and B1 are pulled 3 times but do only
    # contain 2 tests)
    test_types_dic = {
        "test1": ["A1", "B1", "CV03"],
        "test2": ["A1", "B1"],
        "test3": ["A1", "B1"],
    }

    # checking the function
    with pytest.raises(customExceptions.PoolError):
        funcs.create_custom_test_list(test_types_dic, pool_info)
