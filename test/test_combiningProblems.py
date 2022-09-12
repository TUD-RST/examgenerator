import pytest
import os
import json
from addict import Dict

from exam_generator import funcs


def test_combiningProblems():
    root_path = os.path.join(os.getcwd(), "test_directories", "combiningProblems")
    pool_path = os.path.join(root_path, "pool_data")
    settings_path = os.path.join(root_path, "settings", "test.json")

    with open(settings_path, "r") as json_file:
        settings_dictionary = json.load(json_file)

    settings = Dict(settings_dictionary)

    pool_info = funcs.pullPoolData(pool_path)

    test_list = funcs.createCustomTestList(settings.test_types, pool_info)

    tests_per_group = funcs.combiningProblems(settings.group_pairs, test_list)

    # all possible results

    res_1 = [
        [
            [
                ("problem_1.tex", "solution_1.tex", "A1"),
                ("problem_7.tex", "solution_7.tex", "B1"),
            ]
        ],
        [
            [
                ("problem_2.tex", "solution_2.tex", "A1"),
                ("problem_8.tex", "solution_8.tex", "B1"),
            ]
        ],
    ]
    res_2 = [
        [
            [
                ("problem_2.tex", "solution_2.tex", "A1"),
                ("problem_7.tex", "solution_7.tex", "B1"),
            ]
        ],
        [
            [
                ("problem_1.tex", "solution_1.tex", "A1"),
                ("problem_8.tex", "solution_8.tex", "B1"),
            ]
        ],
    ]
    res_3 = [
        [
            [
                ("problem_1.tex", "solution_1.tex", "A1"),
                ("problem_8.tex", "solution_8.tex", "B1"),
            ]
        ],
        [
            [
                ("problem_2.tex", "solution_2.tex", "A1"),
                ("problem_7.tex", "solution_7.tex", "B1"),
            ]
        ],
    ]
    res_4 = [
        [
            [
                ("problem_2.tex", "solution_2.tex", "A1"),
                ("problem_8.tex", "solution_8.tex", "B1"),
            ]
        ],
        [
            [
                ("problem_1.tex", "solution_1.tex", "A1"),
                ("problem_7.tex", "solution_7.tex", "B1"),
            ]
        ],
    ]

    assert (
        (tests_per_group == res_1)
        or (tests_per_group == res_2)
        or (tests_per_group == res_3)
        or (tests_per_group == res_4)
    )
