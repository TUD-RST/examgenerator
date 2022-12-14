# -*- coding: utf-8 -*-

import os
import random
import json
import argparse as ap
import textwrap as tw
from addict import Dict

from .classes import *
from .funcs import *
from .customExceptions import *


def exam_generator(args):
    """
    Main function which combines all modules of this program.

    Parameters:

        args.create_test:
            Would the user like to create a test

        args.make_all:
            Would the user like to create a preview for all problems

        args.make_pool
            Pool which the user would like to create a preview for

        args.make_specific
            Name of the problem the user would like to create a preview for
    """

    # main directory
    root_directory = os.getcwd()

    if check_directory(root_directory) == False:
        return

    # ==================================
    # --- Make-Specific ---
    # ==================================

    if args.make_all or args.make_pool or args.make_specific:
        make_specific(args.make_all, args.make_pool, args.make_specific, root_directory)
        return

    # ==================================
    # --- Create-Test ---
    # ==================================

    # ================ Settings =============================

    # Settings are adjusted in the settings json files in the settings directory and then loaded into Python
    # No change of settings in this program!

    if args.random_seed is not None:
        seed = args.random_seed
        initialize_random_number_generator(seed)
    else:
        initialize_random_number_generator()

    settings_path = args.create_test

    path_settings = os.path.join(root_directory, settings_path)

    if not os.path.isfile(path_settings):
        path_settings = settings_path

    settings_name = os.path.normpath(settings_path).split(os.sep)[-1]

    if not os.path.isfile(path_settings):
        raise MissingFileError(
            f"{errorInfo()} File {settings_name} does not exist. \
             Please make sure your directory structure follows the instructions."
        )

    # Loading the json settings into a Python dictionary
    with open(path_settings, "r", encoding="utf8") as json_datei:
        settings_dictionary = json.load(json_datei)

    # converts Python dict into addict Dic
    settings = Dict(settings_dictionary)

    check_settings(settings, settings_name)

    # assigning int values to string decleration of pages_per_sheet for usage in sumo func
    if settings.page_format_exam == "A4":
        settings.page_format_exam = 2
    elif settings.page_format_exam == "A5":
        settings.page_format_exam = 4

    if settings.page_format_solution == "A4":
        settings.page_format_solution = 2
    elif settings.page_format_solution == "A5":
        settings.page_format_solution = 4

    # ensuring variant name does not create problems while compiling
    settings.variant_name = settings.variant_name.replace(" ", "")

    # ==================================
    # --- Configuration ---
    # ==================================

    # Working directory for the LaTeX compiler
    latex_directory = os.path.join(root_directory, "pool_data")

    if not os.path.isdir(latex_directory):
        raise MissingDirectoryError(
            f"{errorInfo()} {latex_directory} does not exist. \
            Please make sure all types match the ones given in the instructions."
        )

    # Template directory
    template_directory = os.path.join(root_directory, "templates")

    if not os.path.isdir(template_directory):
        raise MissingDirectoryError(
            f"{errorInfo()} {latex_directory} does not exist. \
            Please make sure all types match the ones given in the instructions."
        )

    # Directory where the tests will be saved in (for example: Exams-ET1-WS201920)
    test_directory = os.path.join(
        root_directory,
        "Exams-{}-{}".format(settings.variant_name, settings.semester)
        .replace(" ", "")
        .replace("/", ""),
    )

    pool_files = pull_pool_data(latex_directory)

    file_names_tex = combine_file_names(pool_files)

    # ------------Custom Tests----------------#
    custom_test_list = create_custom_test_list(settings.exams, pool_files)

    # for debugging
    pool_all = Pool(".*", file_names_tex)
    test_all = TestType("VX", *[pool_all for i in range(len(pool_all.stack_available))])
    test_list_all = [test_all]

    # ================================
    # --- Combining problems ---
    # ================================

    tests_per_group = combining_problems(settings.number_of_groups, custom_test_list)

    # ==================================
    # --- Generating the TeX-Files ---
    # ==================================

    copies_per_group = determine_copies_per_group(
        settings.number_of_groups, settings.copies
    )

    generate_tex_files(
        latex_directory,
        template_directory,
        settings.number_of_groups,
        custom_test_list,
        settings.variant_name,
        settings.title,
        settings.semester,
        tests_per_group,
        copies_per_group,
    )

    # ===================
    # --- Compiling ---
    # ===================

    compile(
        test_directory,
        latex_directory,
        settings.options.delete_temp_data,
    )

    combine_group_files(
        test_directory,
        latex_directory,
        settings.number_of_groups,
        custom_test_list,
        settings.variant_name,
        settings.page_format_exam,
        settings.page_format_solution,
    )

    # ==================================
    # --- Sumo-Files ---
    # ==================================

    if settings.options.generate_sumo_pdf:
        # list of all exams and solution pdf files
        all_exam_files = os.listdir(test_directory)

        # only exam pdf files
        problem_files = [
            file for file in all_exam_files if not file.endswith("Solution.pdf")
        ]
        problem_files.sort()
        sumo_name_problems = f"Sumo-{settings.variant_name}-Problems.pdf"
        build_sumo(
            test_directory,
            sumo_name_problems,
            problem_files,
            settings.page_format_exam,
            settings.sumo_options.exam_copies,
        )

        # only solution pdf files
        solution_files = [
            file for file in all_exam_files if file.endswith("Solution.pdf")
        ]
        solution_files.sort()

        sumo_name_solutions = f"Sumo-{settings.variant_name}-Solutions.pdf"
        build_sumo(
            test_directory,
            sumo_name_solutions,
            solution_files,
            settings.page_format_solution,
            settings.sumo_options.solution_copies,
        )

    if not settings.options.generate_single_pdfs:
        files = os.listdir(test_directory)

        os.chdir(test_directory)

        for file in files:
            if "Sumo" not in file:
                delete_pdf(file)

        os.chdir(root_directory)


def main():
    """
    Calls parser and delivers arguments to exam_generator.
    """

    Descr = tw.dedent(
        """            
                        Exam_generator is a script which is designed to create exams/ tests from pools of problems 
                        while ensuring that there will be no repetition amongst different groups. The exams/ tests  
                        are based off of two major components: the LaTeX basis (problems, solutions, templates) and 
                        user defined settings.
        """
    )

    parser = ap.ArgumentParser(description=Descr)

    parser.add_argument(
        "-ct",
        "--create_test",
        help="Creates a test based on the provided json settings file. Provide the path to the settings file of your liking.",
    )
    parser.add_argument(
        "-ma",
        "--make_all",
        action="store_true",
        help="Creates a preview for all problems",
    )
    parser.add_argument(
        "-mp",
        "--make_pool",
        help="Creates a preview for all problems of the given pool. Provide the Path to the pool.",
    )
    parser.add_argument(
        "-ms",
        "--make_specific",
        help="Creates a Preview for only the given problem you will need to provide the path to the problem",
    )

    parser.add_argument(
        "-rs",
        "--random_seed",
        type=int,
        help="Set a new random seed, allowing the same exam to be created, yet with different problems pulled. Provide a positive integer of your liking.",
    )

    args = parser.parse_args()

    if (
        (args.create_test is None)
        and (args.make_all == False)
        and (args.make_pool is None)
        and (args.make_specific is None)
    ):
        parser.error("Please choose at least one of the options. For help type: -h")

    elif args.random_seed is not None and args.create_test is None:
        parser.error("You can only select a random seed when creating an exam.")

    elif args.random_seed is not None:
        if args.random_seed <= 0:
            parser.error("Please select a positive integer as your random seed.")

    else:
        exam_generator(args)


if __name__ == "__main__":
    main()
