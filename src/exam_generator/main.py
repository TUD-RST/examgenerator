# -*- coding: utf-8 -*-

import os
import glob
import random
from warnings import warn
import json
import argparse as ap
import textwrap as tw


from .classes import *
from .funcs import *


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

    settings = args.create_test

    path_settings = os.path.join(root_directory, "settings", str(settings))

    # Loading the json settings into a Python dictionary
    with open(path_settings, "r") as json_datei:
        settings_dictionary = json.load(json_datei)

    # Determines the amount of group pairs
    # for example:  6 => group pairs 01-12
    # 01+02, 03+04, ..., have the same problems
    number_group_pairs = settings_dictionary["group_pairs"]

    # Degree for which the test is created
    # Prefactored options: ET1, ET2, MT, RES
    variant_name = settings_dictionary["variant_name"]

    # Semester
    semester = settings_dictionary["semester"]

    # SUMO-pdf:
    # File contains all tests for the entire semester
    # Creates the test for the whole smester in one go
    sumo_pages_per_sheet_test = settings_dictionary["sumo"]["pages_per_page_test"]
    # 4 = printing double paged A5

    sumo_copies_per_test = settings_dictionary["sumo"]["sumo_number_copies"]
    # Has to match the number of participants per groups

    sumo_pages_per_sheet_solution = settings_dictionary["sumo"][
        "pages_per_page_solution"
    ]
    sumo_copies_per_solution = settings_dictionary["sumo"]["sumo_solution_copies"]

    # Settings of what should be created and deleted
    generate_single_pdfs = settings_dictionary["data"]["generate_single_pdfs"]
    generate_sumo_pdf = settings_dictionary["data"]["generate_sumo_pdf"]
    delete_temp_data = settings_dictionary["data"]["delete_temp_data"]

    # ==================================
    # --- Configuration ---
    # ==================================

    # Working directory for the LaTeX compiler
    latex_directory = os.path.join(root_directory, "problem_data")

    # Template directory
    template_directory = os.path.join(root_directory, "templates")

    # Directory where the tests will be saved in (for example: Exams-ET1-WS201920)
    test_directory = os.path.join(
        root_directory,
        "Exams-{}-{}".format(variant_name, semester).replace(" ", "").replace("/", ""),
    )

    pool_files = poolDirectoryConfig(latex_directory)

    file_names_tex = combineFileNames(pool_files)

    # ------------Custom Tests----------------#
    use_custom_test = settings_dictionary["use_custom_test"]

    if use_custom_test:
        test_types_dictionary = settings_dictionary["test_types"]
        custom_test_list = createCustomTestList(test_types_dictionary, file_names_tex)

    # ------------Premade Tests----------------#

    # General problems for each test
    # A1, B1 -> for 5th Semester RT and 6th semester MT and RES
    # A2, B2 -> for 6th Semester RT (knowledge from RT 2 required)
    poolA1 = Pool("A1", file_names_tex)
    poolB1 = Pool("B1", file_names_tex)
    poolA2 = Pool("A2", file_names_tex)
    poolB2 = Pool("B2", file_names_tex)

    # Experiment specific problems for V1, V3, V7, V8, V15 und V21
    poolCV01 = Pool("CV01", file_names_tex)
    poolCV03 = Pool("CV03", file_names_tex)
    poolCV07 = Pool("CV07", file_names_tex)
    poolCV08 = Pool("CV08", file_names_tex)
    poolCV15 = Pool("CV15", file_names_tex)
    poolCV21 = Pool("CV21", file_names_tex)

    # More experiment specific problems, if there is not enough from C
    poolDV07 = Pool("DV07", file_names_tex)
    poolDV08 = Pool("DV08", file_names_tex)
    poolDV15 = Pool("DV15", file_names_tex)
    poolDV21 = Pool("DV21", file_names_tex)

    # Tests for RT1, MT and RES courses
    testV1 = TestType("V01", poolA1, poolB1, poolCV01)
    testV7 = TestType("V07", poolA1, poolB1, poolCV07, poolDV07)
    testV8_MT_RES = TestType("V08", poolA1, poolB1, poolCV08)
    testV15_MT_RES = TestType("V15", poolA1, poolB1, poolCV15, poolDV15)
    testV21 = TestType("V21", poolA1, poolB1, poolCV21, poolDV21)
    test_list_ET1 = [testV1, testV7, testV21]
    test_list_MT = [testV21, testV8_MT_RES]
    test_list_RES = [testV21, testV8_MT_RES, testV15_MT_RES]

    # Tests for RT2 (6th Semester)
    testV3 = TestType("V03", poolA2, poolB2, poolCV03)
    testV8_ET = TestType("V08", poolA2, poolB2, poolCV08)
    testV15_ET = TestType("V15", poolA2, poolB2, poolCV15, poolDV15)
    test_list_ET2 = [testV3, testV8_ET, testV15_ET]

    # for debugging
    pool_all = Pool(".*", file_names_tex)
    test_all = TestType("VX", *[pool_all for i in range(len(pool_all.stack_available))])
    test_list_all = [test_all]

    # ------------Titles and Test Lists Config----------------#

    if variant_name == "ET1":
        title = "Praktikum Regelungstechnik 1 (ET)"
        test_list_variant = test_list_ET1
    elif variant_name == "ET2":
        title = "Praktikum Regelungstechnik 2 (ET)"
        test_list_variant = test_list_ET2
    elif variant_name == "MT":
        title = "Praktikum Regelung \\& Steuerung (MT)"
        test_list_variant = test_list_MT
    elif variant_name == "RES":
        title = "Praktikum Regelungstechnik (RES)"
        test_list_variant = test_list_RES
    elif use_custom_test:
        title = variant_name
        test_list_variant = custom_test_list
    elif not use_custom_test:
        warn("Unbekannter Bezeichner. Gewuenscht: ET1, ET2, MT oder RES!")
        test_list_variant = []
        title = ""
        quit()

    # ================================
    # --- Combining problems ---
    # ================================

    tests_per_group = combiningProblems(number_group_pairs, test_list_variant)

    # ==================================
    # --- Generating the TeX-Files ---
    # ==================================

    names_prob_sol_pdf = generateTexFiles(
        latex_directory,
        template_directory,
        number_group_pairs,
        test_list_variant,
        variant_name,
        title,
        semester,
        tests_per_group,
        pool_files,
    )

    # ===================
    # --- Compiling ---
    # ===================

    compile(
        test_directory,
        latex_directory,
        generate_single_pdfs,
        delete_temp_data,
    )

    # ==================================
    # --- Sumo-Files ---
    # ==================================

    if generate_sumo_pdf:
        names_prob_sol_pdf[0].sort()
        sumo_name_problems = f"Sumo-{variant_name}-Problems.pdf"
        buildSumo(
            test_directory,
            sumo_name_problems,
            names_prob_sol_pdf[0],
            sumo_pages_per_sheet_test,
            sumo_copies_per_test,
        )

        names_prob_sol_pdf[1].sort()

        sumo_name_solutions = f"Sumo-{variant_name}-Solutions.pdf"
        buildSumo(
            test_directory,
            sumo_name_solutions,
            names_prob_sol_pdf[1],
            sumo_pages_per_sheet_solution,
            sumo_copies_per_solution,
        )


def main():
    """
    Calls parser and delivers arguments to exam_generator.
    """
    if check_directory() == False:
        return

    Descr = tw.dedent(
        """\
                        This script creates tests based on given problems and settings

                        From a pool of problems, test will be created in  a way, that there will be no
                        repetition for all experiments and groups.

                        There is two LaTeX templates in the Templates Directory:
                        One for the problems and one for the sample solution and evaluation.
                        In these templates there is placeholders, which will be replaced by
                        this script.

                        The problems are located in the Aufgaben directory which is furthermore separated into
                        the main pools (PoolA, PoolB, PoolC, PoolD). They usually differ between general problems,
                        that are used in every test, and problems, that are specific for the given experiment.

                        Tests are combined via instances of the class TestType and managed via instances of the class Pool.
                        Solutions are saved in separate files.
                        Files for problems have the prefix "aufgabe_", solutions the prefix "loesung_".
                        The scheme is the following: 
                            aufgabe_A1_2.tex -> 2. problem of type A1
                        or for an experiment:
                            aufgabe_CV03_1.tex -> 2. problem from experiment (V) number 03 of type C
                        for a more detailed breakdown of the nomenclature view the read.me file in the Aufgaben folder
                        Please avoid using combinations of more than one capital letter describing your pools
                        except for combinations with V (which stands for experiment) since this could lead to 
                        problems during the compiling process.

                        Subtasks of a problem should be structured in an enumerate-surrounding.

                        Within the solution files the solution text has to be written in between
                        \begin{Loesung} \end{Loesung}. The solution of every subtask starts with the 
                        key \lsgitem.

                        It is possible to assign points to problems and solutions with the macro \Pkte{n}.
                        During the compiling process the given points will be added automatically for the entire test

                        Optionally, all tests and sample solutions can be combined into one "sumo-file". 
                        This allows creating the tests for the entire semester in one go. However, this
                        is only useful if the problems and solutions are final and will not have to be corrected
                        afterwards."""
    )

    parser = ap.ArgumentParser(description=Descr)

    parser.add_argument(
        "-ct",
        "--create_test",
        help="Creates a test based on the provided json settings file",
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
        choices=["A", "B", "C", "D", "E", "F", "G", "H"],
        help="Creates a Preview for all problems of the given pool",
    )
    parser.add_argument(
        "-ms",
        "--make_specific",
        help="Creates a Preview for only the given problem\
                            you will need to provide them problem´s name (without .tex)",
    )

    args = parser.parse_args()

    if (
        (args.create_test is None)
        and (args.make_all == False)
        and (args.make_pool is None)
        and (args.make_specific is None)
    ):
        parser.error("Please choose at least one of the options. For help type: -h")

    else:
        exam_generator(args)


if __name__ == "__main__":
    main()
