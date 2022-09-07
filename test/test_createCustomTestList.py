import pytest

from exam_generator import funcs
from exam_generator import classes
from exam_generator import customExceptions

file_names_tex = [
    "problem_A1_1.tex",
    "solution_A1_1.tex",
    "problem_B1_1.tex",
    "solution_B1_1.tex",
    "problem_CV03_1.tex",
    "solution_CV03_1.tex",
]


def test_createCustomTestList_correct(file_names_tex):

    test_types_dic = {
        "test1": ["Test1", "A1", "B1", "CV03"],
        "test2": ["Test2", "A1", "B1"],
    }

    poolA1 = classes.Pool("A1", file_names_tex)
    poolB1 = classes.Pool("B1", file_names_tex)
    poolCV03 = classes.Pool("CV03", file_names_tex)

    pool_list1 = [poolA1, poolB1, poolCV03]
    pool_list2 = [poolA1, poolB1]

    custom_test_list = funcs.createCustomTestList(test_types_dic, file_names_tex)

    error = False

    if len(custom_test_list) != 2:
        error = True

    # checking first testtype
    testtype1 = custom_test_list[0]
    if testtype1.name != "Test1":
        error = True

    if len(testtype1.pools) != len(pool_list1):
        error = True

    for pool in testtype1.pools:
        if pool.name != pool_list1[pool.index()].name:
            error = True

    # checking second testtype
    testtype2 = custom_test_list[1]
    if testtype2.name != "Test2":
        error = True
    if len(testtype1.pools) != len(pool_list2):
        error = True

    for pool in testtype2.pools:
        if pool.name != pool_list2[pool.index()].name:
            error = True

    assert error == False


def test_createCustomTestList_noEntries(file_names_tex):
    test_types_dic = {}
    with pytest.raises(customExceptions.SettingsError):
        funcs.createCustomTestList(test_types_dic, file_names_tex)


def test_createCustomTestList_noProblemsForPool(file_names_tex):
    test_types_dic = {
        "test1": ["Test1", "APPA"],
    }
    with pytest.raises(customExceptions.SettingsError):
        funcs.createCustomTestList(test_types_dic, file_names_tex)
