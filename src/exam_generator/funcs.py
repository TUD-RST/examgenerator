"""
This module contains all functions relevant for the exam-generator.
"""

import os
from platform import platform
from PyPDF2 import PdfFileReader, PdfFileWriter
import glob
import subprocess
import shutil
from pathlib import Path
from addict import Dict
import platform
import math
from jinja2 import Environment, FileSystemLoader
import random
import re

from .classes import TestType, Pool
from .customExceptions import *


def check_directory(root_directory) -> bool:
    """
    Checks if required directories exists.

    :return: False=not all exist, True= all exist
    :rtype: bool
    """
    if not os.path.isdir(os.path.join(root_directory, "settings")):
        raise MissingDirectoryError(
            f"{errorInfo()} settings directory does not exist in \
            current working directory. Please make sure you are starting this program in \
                a directory following the instructions."
        )

    if not os.path.isdir(os.path.join(root_directory, "templates")):
        raise MissingDirectoryError(
            f"{errorInfo()} templates directory does not exist in \
            current working directory. Please make sure you are starting this program in \
                a directory following the instructions."
        )

    if not os.path.isdir(os.path.join(root_directory, "pool_data")):
        raise MissingDirectoryError(
            f"{errorInfo()} pool_data directory does not exist in \
            current working directory. Please make sure you are starting this program in \
                a directory following the instructions."
        )

    return True


def initialize_random_number_generator(seed=1024):
    """
    Initializes random seed.

    :param seed: seed. Defaults to 1024 for debugging purposes.
    :type seed: int
    """
    random.seed(seed)


def check_settings(settings, settings_file):
    """
    Checks the json settings file for user input errors.

    :param settings: settings input from user.
    :type settings: Dict from  addict

    :param settings_file: name of the used settings file.
    :type settings_file: str
    """
    if not isinstance(settings.number_of_groups, int):
        raise SettingsError(
            f"{errorInfo()} group_pairs in {settings_file} is not of the required type int. \
            Please make sure all types match the ones given in the instructions."
        )

    if not isinstance(settings.title, str):
        raise SettingsError(
            f"{errorInfo()} title in {settings_file} is not of the required type string. \
            Please make sure all types match the ones given in the instructions."
        )

    if not isinstance(settings.variant_name, str):
        raise SettingsError(
            f"{errorInfo()} variant_name in {settings_file} is not of the required type string. Please make sure all types match the ones given in the instructions."
        )

    if not isinstance(settings.semester, str):
        raise SettingsError(
            f"{errorInfo()} semester in {settings_file} is not of the required type string. Please make sure all types match the ones given in the instructions."
        )

    if not isinstance(settings.page_format_exam, str):
        raise SettingsError(
            f"{errorInfo()} pages_per_sheet_test in {settings_file} is not of the required type string. Please make sure all types match the ones given in the instructions."
        )

    if not isinstance(settings.sumo_options.exam_copies, int):
        raise SettingsError(
            f"{errorInfo()} sumo_number_copies in {settings_file} is not of the required type int. Please make sure all types match the ones given in the instructions."
        )

    if not isinstance(settings.page_format_solution, str):
        raise SettingsError(
            f"{errorInfo()} pages_per_sheet_solution in {settings_file} is not of the required type string. Please make sure all types match the ones given in the instructions."
        )

    if not isinstance(settings.sumo_options.solution_copies, int):
        raise SettingsError(
            f"{errorInfo()} sumo_copies_per_solution in {settings_file} is not of the required type int. Please make sure all types match the ones given in the instructions."
        )

    if not isinstance(settings.options.generate_single_pdfs, bool):
        raise SettingsError(
            f"{errorInfo()} generate_single_pdfs in {settings_file} is not of the required type bool. \
             Please make sure all types match the ones given in the instructions."
        )

    if not isinstance(settings.options.generate_sumo_pdf, bool):
        raise SettingsError(
            f"{errorInfo()} generate_sumo_pdf in {settings_file} is not of the required type bool. \
             Please make sure all types match the ones given in the instructions."
        )

    if not isinstance(settings.options.delete_temp_data, bool):
        raise SettingsError(
            f"{errorInfo()} delete_temp_data in {settings_file} is not of the required type bool. \
             Please make sure all types match the ones given in the instructions."
        )

    if (
        settings.sumo_options.solution_copies < 1
        or settings.sumo_options.exam_copies < 1
    ):
        raise SettingsError(
            f"{errorInfo()} You have to have at least one copy for each test/ solution in {settings_file}."
        )

    if (settings.page_format_exam != "A4") and (settings.pages_format_exam != "A5"):
        raise SettingsError(
            f"{errorInfo()} Please choose between 2 (print problems in A4) or 4 (print problems in A5) pages \
            per sheet for your sumo problem/ solution files in {settings_file}."
        )

    if (settings.page_format_solution != "A4") and (
        settings.page_format_solution != "A5"
    ):
        raise SettingsError(
            f"{errorInfo()} Please choose between 2 (print problems in A4) or 4 (print problems in A5) pages \
            per sheet for your sumo problem/ solution files in {settings_file}."
        )

    if settings.number_of_groups < 1:
        raise SettingsError(
            f"{errorInfo()} You have to have at least one group_pair in {settings_file}."
        )

    if not isinstance(settings.copies, int):
        raise SettingsError(
            f"{errorInfo()} copies in {settings_file} is not of the required type int. Please make sure all types match the ones given in the instructions."
        )

    if settings.copies < 1:
        raise SettingsError(
            f"{errorInfo()} Number of copies has to be at least one in {settings_file}."
        )


def pull_pool_data(latex_directory):
    """
    Sets pool directories and its problem data.


    Args:
        latex_directory (str): working directory of latex compiler

    Returns:
        list[tuple(list[str], str)]: problem/ solution names, name of corresponding pool
    """
    pool_info = []

    for pool_name in sorted(os.listdir(latex_directory)):
        pool_dir = os.path.join(latex_directory, pool_name)

        if not os.path.isdir(pool_dir):
            continue

        pool_data_list = [
            os.path.basename(fn)
            for fn in sorted(glob.iglob(os.path.join(pool_dir, "*.tex")))
        ]

        for file in pool_data_list:
            if "problem" not in file and "solution" not in file:
                raise CompilingError(
                    f"{errorInfo()} File name {file} does not follow the \
                    naming pattern given in the instructions."
                )

        pool_info.append((pool_data_list, pool_name))

    if len(pool_info) == 0:
        raise MissingDirectoryError(
            f"{errorInfo()} No pools provided in the pool_data directory. \
            Please make sure your directory setup follows the instructions."
        )

    return pool_info


def combine_file_names(pool_files):
    """
    Combines the problems of all individual pools into one.

    Args:
        pool_files (list[tuple(list[str], str)]): problem/ solution names, name of corresponding pool

    Returns:
        list[str]: names of all problems/ solutions
    """
    file_names_tex = []
    for pool in pool_files:
        file_names_tex += pool[0]
    return file_names_tex


def create_custom_test_list(test_types_dictionary, pool_info):
    """
    Creates custom test list out of json dictionary.


    Args:
        test_types_dictionary (dict): json dict loaded into Python format
        pool_info (list[tuple(list[str], str)]): pool files, pool name

    Returns:
        list[TestType]: list of custom tests
    """

    if len(test_types_dictionary) == 0:
        raise SettingsError(
            f"{errorInfo()} No custom exams provided in your settings. \
            Please make sure you follow the instructions on creating custom exams."
        )
    custom_test_list = []

    # converts all test types (strings) to actual test types
    # and adds them to custom test list
    for test_name, pool_list in test_types_dictionary.items():
        custom_test_pools = []

        for pool_name in pool_list:

            # selects the correct file list for the pool
            pool_file_list = []
            for pool in pool_info:
                if pool[1] == pool_name:
                    pool_file_list = pool[0]
                    break

            new_pool = Pool(pool_name, pool_file_list)

            # checking if new pool already exists so not two instances are created
            for existing_pool in custom_test_pools:
                if existing_pool.name == new_pool.name:
                    new_pool = existing_pool
                    break

            custom_test_pools.append(new_pool)

        custom_test = TestType(test_name, *custom_test_pools)

        custom_test_list.append(custom_test)

    return custom_test_list


def combining_problems(number_group_pairs, test_list_variant):

    """
    For each group this function adds to a list which contains
    problems and their according solutions from given pools
    depending on the test variant.

    :param number_group_pairs: Number of group pairs
    :type number_group_pairs: int

    :param test_list_variant: List of test variants belonging to chosen variant
    :type test_list_variant: list[TestType]

    :return: tests_per_group - problems/ solutions for each group
    :rtype: list[list[list[tuple(str, str, str)]]]

    """

    tests_per_group = []

    for i in range(number_group_pairs):
        test_satz = []

        # For each test from every pool a problem is pulled
        for test_typ in test_list_variant:
            prob_sol = []

            for pool in test_typ.pools:
                prob_sol.append(pool.pull())

            test_satz.append(prob_sol)

        # Sets aside the used problems of each pool
        for test_typ in test_list_variant:
            for pool in test_typ.pools:
                pool.discard()

        tests_per_group.append(test_satz)

    return tests_per_group


def determine_copies_per_group(number_groups, copies):
    """
    Calculates copies per group

    Args:
        number_groups (int): group count
        copies (int): number of total copies

    Returns:
        int: number of copies for each group
    """
    copies_per_group = math.ceil(copies / number_groups)

    return copies_per_group


def generate_tex_files(
    latex_directory,
    template_directory,
    number_group_pairs,
    test_list_variant,
    variant_name,
    title,
    semester,
    tests_per_group,
    copies_per_group,
):

    """

    This function replaces the variables within the tex problem/ solution files with the information given
    by the settings.

    :param latex_directory: Directory for the latex compiler
    :type latex_directory: str

    :param template_directory: Directory of the problem/ solution templates
    :type template_directory: int

    :param number_group_pairs: Number of group pairs
    :type number_group_pairs: int

    :param test_list_variant: List of test variants belonging to chosen variant
    :type test_list_variant: list[TestType]

    :param variant_name: Name of the test variant
    :type variant_name: str

    :param title: Title of the event. Dependent on name_variant
    :type title: str

    :param semester: Given semester in json settings file
    :type semester: str

    :param tests_per_group: List of problems/ solutions for each group
    :type tests_per_group: list[str]

    """

    # Deletes all temporary files in the pool_data directory
    for file in glob.glob(os.path.join(latex_directory, "*.*")):
        os.remove(file)

    problem_template = "template_problem.tex"
    template_problem_path = os.path.join(template_directory, problem_template)

    if not os.path.isfile(template_problem_path):
        raise MissingFileError(
            f"{errorInfo} File {problem_template} does not exist in \
            the settings directory. Please make sure your file structure follows the directions."
        )

    solution_template = "template_solution.tex"
    template_solution_path = os.path.join(template_directory, solution_template)

    if not os.path.isfile(template_problem_path):
        raise MissingFileError(
            f"{errorInfo} File {problem_template} does not exist in \
             the settings directory. Please make sure your file structure follows the directions."
        )

    with open(template_problem_path, "r") as d:
        template_problem = d.read()
    with open(template_solution_path, "r") as d:
        template_solution = d.read()

    for group in range(number_group_pairs):
        group_name = f"{group + 1}"

        for test_index, test_typ in enumerate(test_list_variant):
            # Problem
            # Setting file name and path
            name = test_typ.name.replace(" ", "")
            # file_name_prob = f"Exam-{variant_name}-{name}-{group_name}-{i}.tex"
            # file_path_problem = os.path.join(latex_directory, file_name_prob)

            for i in range(copies_per_group):
                file_name_prob = f"Exam-{variant_name}-{name}-{group_name}-{i}.tex"
                file_path_problem = os.path.join(latex_directory, file_name_prob)
                file_content_prob = create_file_content(
                    template_problem,
                    title,
                    semester,
                    test_typ,
                    group_name,
                    tests_per_group,
                    group,
                    test_index,
                    0,
                    i,
                    name,
                )

                # keys = generate_keys(file_content_prob, name, group_name, i)

                # file_content_prob = replace_keys(file_content_prob, keys)

                with open(file_path_problem, "w+") as d:
                    d.write(file_content_prob)

                # Solution
                # Setting file name and path
                file_name_sol = (
                    f"Exam-{variant_name}-{name}-{group_name}-Solution-{i}.tex"
                )
                file_path_sol = os.path.join(latex_directory, file_name_sol)

                file_content_sol = create_file_content(
                    template_solution,
                    title,
                    semester,
                    test_typ,
                    group_name,
                    tests_per_group,
                    group,
                    test_index,
                    1,
                    i,
                    name,
                )

                # file_content_sol = replace_keys(file_content_sol, keys)

                with open(file_path_sol, "w+") as d:
                    d.write(file_content_sol)


def create_file_content(
    template,
    title,
    semester,
    test_typ,
    group_name,
    tests_per_group,
    group,
    test_index,
    prob_sol_index,
    student,
    test,
):
    """
    Replaces template variables and adds problem string.

    :param template: file content of template
    :type template: str

    :param title: title of exam
    :type title: str

    :param semester: semester
    :type semester: str

    :param test_typ: test type out of test list
    :type test_typ: TestType

    :param group_name: name of group
    :type group_name: str

    :param test_index: index of test in test_list_variant
    :type test_index: int

    :param prob_sol_index: determines compilation for prob[0]/ sol[1]
    :type prob_sol_index: int

    :param student: number of student
    :type student: int

    :param test: name of test
    :type test: str

    :returns: file content
    :rtype: str
    """
    # Replacing the parameters in the LaTeX file
    file_content = template
    file_content = file_content.replace("__TITLE__", title)
    file_content = file_content.replace("__SEMESTER__", semester)
    file_content = file_content.replace("__EXAM__", test_typ.name)
    file_content = file_content.replace("__GROUP__", group_name)

    # Creation of the problem strings + implementation in the LaTeX file
    problem_string = create_problem_content(
        tests_per_group, group, test_index, prob_sol_index, student, test
    )

    file_content = file_content.replace("__PROBLEMS__", problem_string)

    return file_content


def create_problem_content(
    tests_per_group, group, test_index, prob_sol_index, student, test
):
    """
    Combines problem files, replaces KEYs and applies jinja templates.

    :param tests_per_group: number of tests per group
    :type tests_per_group: int

    :param group: name of group
    :type group: str

    :param test_index: index of test in test_list_variant
    :type test_index: int

    :param prob_sol_index: determines compilation for prob[0]/ sol[1]
    :type prob_sol_index: int

    :param student: number of student
    :type student: int

    :param test: name of test
    :type test: str

    :returns: string concisting of all problems for a student
    :rtype: str
    """
    problem_string = ""
    for prob_sol in tests_per_group[group][test_index]:
        problem_string += f"\\item\n"
        pool_name = prob_sol[2]
        with open(
            os.path.join(
                os.getcwd(), "pool_data", pool_name, prob_sol[prob_sol_index]
            ).replace("\\", "/"),
            "r",
        ) as d:
            problem_str = d.read()
        problem_string += f"{problem_str}\n\n"

    problem_string = replace_keys(problem_string, test, group, student)

    temp_file = "temp_file.tex"
    with open(temp_file, "w") as temp:
        temp.write(problem_string)

    applyJinjaTemplate(os.getcwd(), temp_file)

    with open(temp_file, "r") as d:
        problem_string = d.read()

    delete_command("temp_file")

    return problem_string


##############################################
###------------Parameterization------------###
##############################################


def generate_keys(file_content: str, test, group, student):
    """
    Searches for all variants of __KEY{int}__ and adds them
    with a uniquely generated key to dict.

    :param file_content: content of working file
    :type file_content: str

    :param test: name of test
    :type test: str

    :param group: group name
    :type group: str

    :param student: number of student
    :type student: str

    :returns: old key -> unique key
    :rtype: dict{str: str}
    """

    # creates list with different keys in file
    keys = re.findall(r"__KEY+\d__", file_content)
    keys = list(dict.fromkeys(keys))

    # adds unique keys
    unique_keys = {}
    for index, key in enumerate(keys):
        unique_keys[key] = f'"{test}-{group}-{student}-{index+1}"'

    return unique_keys


def replace_keys(file_content: str, test, group, student):
    """
    Replaces __KEY{int}__ in latex files with custom keys for later usage.

    :param file_content: content of file to be edited
    :type file_conten: str

    :param test: name of test
    :type test: str

    :param group: group name
    :type group: str

    :param student: number of student
    :type student: int

    :returns: file content with replaced keys
    :rtype: str
    """
    keys = generate_keys(file_content, test, group, student)
    for key, unique_key in keys.items():
        file_content = file_content.replace(key, unique_key)

    return file_content


def curly_braces_wrapper(arg: str):
    r"""
    Return a string like "{" + arg + "}".

    Motivation: the templating engine uses curly braces as variable-section delimiter. Also, TeX
    syntax uses curly braces on many occassion. This makes it hard to denote e.g.

    ```
    \emph{XYZ}
    ```

    where XYZ should be an expression like {{contex.myvariable}}. The following results in an
    error of the templating engine:


    ```
    \emph{{{contex.myvariable}}}
    ```

    With this function one can use:

    \emph{{cbw(context["myvariable"])}}


    """
    return "{%s}" % arg


# CACHE used for keys -> random numbers
CACHE = {}


def get_random_number(key: str, lower_bound=1, upper_bound=10):
    """
    Return a number from the CACHE or key is yet unknown, randomly create a new one.

    :param key: key to uniquely identify this number for later usages, e.g. in the solution
    :type key: str

    :param lower_bound: lower bound
    :type lower_bound: int

    :param upper_bound: upper bound
    :type upper_bound: int

    :returns: random number
    :rtype: int
    """

    if key in CACHE:
        return CACHE[key]

    # key is yet unknown → create new entry
    res = random.randint(lower_bound, upper_bound)
    CACHE[key] = res
    return res


def applyJinjaTemplate(latex_directory, file):
    """
    Applies jinja template to a file.

    :param latex_directory: directory where template lives
    :type latex_directory: str

    :param file: name of file
    :type file: str
    """

    jin_env = Environment(
        loader=FileSystemLoader(latex_directory),
        # autoescape=select_autoescape(['html', 'xml']),
    )

    context = {
        # pass this function to the template to allow the template-engine to access CACHE
        "rnum": get_random_number,
    }

    template = jin_env.get_template(file)

    file_content = template.render(context=context, cbw=curly_braces_wrapper)

    with open(file, "w") as resfile:
        resfile.write(file_content)


###############################################
###----------End Parameterization-----------###
###############################################


def compile(test_directory, latex_directory, delete_temp_data):

    """
    This function compiles the tex files and turns them into pdf format and moves them to
    the test directory. Lastly, it deletes temporary data.

    :param test_directory: Directory where the generated tests are saved
    :type test_directory: str

    :param latex_directory: Working directory of latex compiler
    :type latex_directory: str

    :param delete_temp_data: Should temporary data be deleted
    :type delete_temp_data: bool
    """

    shutil.rmtree(test_directory, ignore_errors=True)
    os.mkdir(test_directory)
    os.chdir(latex_directory)

    tex_files = [file for file in os.listdir(latex_directory) if file.endswith(".tex")]

    for file in tex_files:
        # execute pdflatex twice to resolve references
        command = (
            # f"pdflatex -interaction=batchmode {file} && "
            f"pdflatex -interaction=batchmode {file}"
        )
        print(command)
        process = subprocess.Popen(
            command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
        )
        process.wait()
        if process.returncode != 0:
            delete_temp_data = False
            raise CompilingError(
                f"{errorInfo()} Problem while compiling {file}. Temporary data will not be deleted."
            )

    # Delete temporary data
    if delete_temp_data:
        delete_command()


def combine_group_files(
    test_directory,
    latex_directory,
    groups,
    test_list_variant,
    variant_name,
    exam_format,
    solution_format,
):
    """
    Combines the separate group pdf files into one file and moves it to the test directory.

    :param test_directory: directory where generated exam is stored
    :type test_directory: str

    :param latex_directory: directory of latex compiler
    :type latex_directory: str

    :param groups: number of different groups
    :type groups: int

    :param test_list_variant: List of test variants belonging to chosen variant
    :type test_list_variant: list[TestType]

    :param variant_name: name of the variant
    :type variant_name: str
    """
    pdf_files = [file for file in os.listdir(latex_directory) if file.endswith(".pdf")]

    for test in test_list_variant:
        name = test.name.replace(" ", "")
        for group in range(groups):
            group_name = f"{group + 1}"
            group_prob_files = [
                file
                for file in pdf_files
                if f"Exam-{variant_name}-{name}-{group_name}" in file
                and not "Solution" in file
            ]

            group_file_prob_name = f"Exam-{variant_name}-{name}-{group_name}.pdf"

            build_sumo(
                latex_directory,
                group_file_prob_name,
                group_prob_files,
                exam_format,
                1,
            )

            shutil.move(group_file_prob_name, test_directory)

            group_sol_files = [
                file
                for file in pdf_files
                if (
                    f"Exam-{variant_name}-{name}-{group_name}" in file
                    and "Solution" in file
                )
            ]

            group_file_sol_name = (
                f"Exam-{variant_name}-{name}-{group_name}-Solution.pdf"
            )
            build_sumo(
                latex_directory,
                group_file_sol_name,
                group_sol_files,
                solution_format,
                1,
            )

            shutil.move(group_file_sol_name, test_directory)
    for file in [
        file for file in os.listdir() if os.path.isfile(file) and file.endswith(".pdf")
    ]:
        delete_pdf(file)


def build_sumo(directory, sumo_name, pdf_list, pages_per_sheet, copies_per_file):

    """
    This function creates the sumo file which contains all problems/ solutions for all groups.

    :param directory: Directory where to be combined problems lie
    :type test_directory: str

    :param sumo_name: Name of the Sumo file either for the problems or solutions
    :type sumo_name: str

    :param pdf_list: List of the names of the created PDF problem/ solution files
    :type pdf_list: list[str]

    :param pages_per_sheet: How many different pages there should be displayed on one page/ sheet
    :type pages_per_sheet: int

    :param kopien_pro_blatt: How many copies you would like for each problem/ solution
    :type kopien_pro_blatt: int

    Creates:

        * pdf file sumo_name.pdf

    """

    os.chdir(directory)
    writer = PdfFileWriter()

    open_files = []
    for pdf in pdf_list:
        d = open(pdf, "rb")
        open_files.append(d)
        # TODO create extra func with: with open
        reader = PdfFileReader(d)
        num_pages = reader.getNumPages()
        more_than_multiple = num_pages % pages_per_sheet
        if more_than_multiple == 0:
            blank_pages = 0
        else:
            blank_pages = pages_per_sheet - more_than_multiple

        for copy in range(copies_per_file):
            for page in range(num_pages):
                writer.addPage(reader.getPage(page))
            for blank_page in range(blank_pages):
                writer.addBlankPage()

    with open(sumo_name, "wb+") as d:
        writer.write(d)

    for d in open_files:
        d.close()


######################################
###------------Previews------------###
######################################


def make_specific(make_all, pool_path, problem_path, root_directory):
    """
    This Function creates previews for given pools/ problems or all.

    :param make_all: Make a preview for all problems
    :type make_all: bool

    :param pool: Name of the pool to be created
    :type pool: str

    :problem: File name of the problem to be created
    :type problem: str
    """

    # list of problems to be created
    filenames_problems = []

    # if a pool is selected, all its problems will be added to the creation list
    if pool_path is not None:

        abs_path = os.path.join(root_directory, f"{pool_path}/problem*.tex")

        if not os.path.isfile(abs_path):
            abs_path = os.path.join(pool_path, "problem*.tex")

        filenames_problems.extend(glob.glob(abs_path))

        pool = os.path.normpath(pool_path).split(os.sep)[-1]

        FILENAME = "Preview_Pool_" + pool
    # if problem is provided, it is added to the preview creation list
    if problem_path is not None:
        abs_path = os.path.join(root_directory, problem_path)

        if not os.path.isfile(abs_path):
            abs_path = problem_path

        filenames_problems.extend(glob.glob(abs_path))

        problem = os.path.normpath(abs_path).split(os.sep)[-1].removesuffix(".tex")

        FILENAME = "Preview_" + problem

    # if make_all is selected the preview creation list contains all problems
    if make_all:
        filenames_problems = glob.glob(
            os.path.join(root_directory, "pool_data/*/problem*.tex")
        )
        FILENAME = "Preview_all"

    specific_directory = os.path.join(root_directory, "previews")

    # changes file name if file already exists
    i = 1
    while Path(os.path.join(specific_directory, FILENAME + ".pdf")).is_file():
        if i == 1:
            FILENAME = FILENAME + "_" + str(i)
        if i > 10:
            FILENAME = FILENAME[:-2] + str(i)
        if i > 100:
            raise CompilingError(
                f"{errorInfo()} Maximum amount of previews for a single file is reached. Please delete unnecessary files."
            )
        if i < 11:
            FILENAME = FILENAME[:-1] + str(i)
        i += 1

    # ---------------Settings End-----------------#

    # -------------Creation of the PDF File-------------#

    with open("{0}.tex".format(FILENAME), "w", encoding="utf-8") as f:
        # Latex-Preamble
        f.write("\\documentclass[a4paper,10pt]{article}\n")
        f.write("\\usepackage[utf8]{inputenc}\n")
        f.write("\\usepackage[T1]{fontenc}\n")
        f.write("\\usepackage{german}\n")
        f.write("\\usepackage{amsmath}\n")
        f.write("\\usepackage{amssymb}\n")
        f.write("\\usepackage{epsfig}\n")
        f.write("\\usepackage{graphicx}\n")
        f.write("\\usepackage{color}\n")
        f.write("\\usepackage{subfigure}\n")
        f.write("\\usepackage{tabularx}\n")
        f.write("\\usepackage{cancel}\n")
        f.write("\\usepackage{enumitem}\n")
        f.write("\\usepackage{units}\n")
        f.write("\\usepackage[left=1.5cm,right=1.5cm,top=2cm,bottom=2cm]{geometry}\n")
        f.write("\\setlength{\\parskip}{2ex}\n")
        f.write("\\setlength{\\parindent}{0ex}\n")
        f.write("\\newcolumntype{C}[1]{>{\\centering\\arraybackslash}m{#1}}\n")
        f.write(
            "\\newcommand{\\diff}[3][]{\\frac{\\mathrm{d}^{#1}#2}{\\mathrm{d}{#3}^{#1}}}"
        )
        f.write(
            "\\newcommand{\\Pkte}[2][-999]{\\fbox{\\textcolor{black}{\\textbf{#2\\,P.}}}}\n"
        )
        f.write("\\newenvironment{Loesung}{\\begin{enumerate}}{\\end{enumerate}}\n")
        f.write("\\newcommand{\\lsgitem}{\\item}\n")
        f.write("\\newcommand{\\abb}{\\\\[0,5cm]}\n")
        f.write("\\newcommand{\\ds}{\\displaystyle}\n")
        f.write("\\graphicspath{{Latex}}\n")
        f.write("\\begin{document}\n")

        # problems and solutions
        for name in filenames_problems:
            name = name.replace("\\", "/")
            f.write("\\textbf{{{0}}}\n\n".format(name.replace("_", "\\_")))
            f.write("\\input{{{0}}}\n\n".format(name))
            f.write("\\textbf{Loesung:}\\\\\n\n")
            f.write("\\input{{{0}}}\n\n".format(name.replace("problem", "solution")))
            f.write("\\hrulefill\n\n\n")

        # Document end
        f.write("\\end{document}\n")

    # compiling and if successful deleting temporary data
    process = subprocess.Popen(
        "pdflatex -interaction=nonstopmode {0}.tex".format(FILENAME), shell=True
    )
    process.wait()

    if process.returncode == 0:
        delete_command(FILENAME)
    else:
        raise CompilingError(
            f"{errorInfo()}, Problem while compiling the template pdf file."
        )

    # creating new folder if not already existend
    if not os.path.isdir(specific_directory):
        os.mkdir(specific_directory)

    # moving pdf file to Previews directory
    shutil.move(FILENAME + ".pdf", specific_directory)


#####################################
###------------Helpers------------###
#####################################


def delete_command(filename=None):
    """
    Deletes temporary data with commands based on OS.

    :param filename: Specific name to be deleted. Defaulted to None
    :type filename: str
    """
    if platform.system() == "Windows":
        command = "del /Q *.dvi *.ps *.aux *.log *.tex"
        if filename is not None:
            command = "del {0}.aux {0}.log {0}.tex {0}.pdf".format(filename)

    elif platform.system() == "Linux":
        command = "rm -f *.dvi *.ps *.aux *.log *.tex"
        if filename is not None:
            command = "rm -f {0}.aux {0}.log {0}.tex {0}.pdf".format(filename)
    else:
        raise CompilingError(
            f"{errorInfo()} Your operating system is not supported. Please try again on Windows or Linux."
        )

    # print(command)
    process = subprocess.Popen(command, shell=True)
    process.wait()
    if process.returncode != 0:
        raise CompilingError(f"{errorInfo()} Temporary data could not be deleted.")


def delete_pdf(filename):
    """
    Deletes a pdf file based on os.

    :param filename: name of the file to be deleted.
    :type filename: str
    """
    if platform.system() == "Windows":
        command = f"del /Q {filename}"
    elif platform.system() == "Linux":
        command = f"rm -f {filename}"

    process = subprocess.Popen(command, shell=True)
    process.wait()
    if process.returncode != 0:
        raise CompilingError(f"{errorInfo()} Single PDFs could not be deleted.")
