import pytest

from exam_generator import funcs
from exam_generator import classes
from exam_generator import customExceptions


def test_createCustomTestList_correct():

    poolA_files = ["problem_1.tex", "solution_1.tex"]

    poolB_files = ["problem_1.tex", "solution_1.tex"]

    poolC_files = ["problem_1.tex", "solution_1.tex"]

    pool_info = [(poolA_files, "A1"), (poolB_files, "B1"), (poolC_files, "CV03")]

    test_types_dic = {
        "test1": ["A1", "B1", "CV03"],
        "test2": ["A1", "B1"],
    }

    poolA1 = classes.Pool("A1", poolA_files)
    poolB1 = classes.Pool("B1", poolB_files)
    poolCV03 = classes.Pool("CV03", poolC_files)

    pool_list1 = (poolA1, poolB1, poolCV03)
    pool_list2 = (poolA1, poolB1)

    custom_test_list = funcs.createCustomTestList(test_types_dic, pool_info)

    error = False

    if len(custom_test_list) != 2:
        error = True

    # checking first testtype
    testtype1 = custom_test_list[0]
    if testtype1.name != "Test1":
        error = True

    if len(testtype1.pools) != len(pool_list1):
        error = True

    pool_list_test1 = testtype1.pools
    for pool in pool_list_test1:
        if pool.name != pool_list1[pool_list_test1.index(pool)].name:
            error = True

    # checking second testtype
    testtype2 = custom_test_list[1]
    if testtype2.name != "Test2":
        error = True
    if len(testtype1.pools) != len(pool_list2):
        error = True

    pool_list_test2 = testtype2.pools

    for pool in pool_list2:
        if pool.name != pool_list2[pool_list_test2.index(pool)].name:
            error = True

    assert error == False


def test_createCustomTestList_noEntries():
    poolA_files = ["problem_1.tex", "solution_1.tex"]

    poolB_files = ["problem_1.tex", "solution_1.tex"]

    poolC_files = ["problem_1.tex", "solution_1.tex"]

    pool_info = [(poolA_files, "A1"), (poolB_files, "B1"), (poolC_files, "CV03")]

    test_types_dic = {}
    with pytest.raises(customExceptions.SettingsError):
        funcs.createCustomTestList(test_types_dic, pool_info)
