"""
This module contains all functions relevant for the exam-generator.
"""

from genericpath import isfile
import os
from PyPDF2 import PdfFileReader, PdfFileWriter
import glob
import subprocess
import shutil
from pathlib import Path
from addict import Dict

from .classes import *
from .customExceptions import *


def buildSumo(test_directory, sumo_name, pdf_list, pages_per_sheet, copies_per_file):

    """
    This function creates the sumo file which contains all problems/ solutions for all groups.

    :param test_directory: Directory in which the created tests are saved
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

    os.chdir(test_directory)
    writer = PdfFileWriter()

    open_files = []
    for pdf in pdf_list:
        d = open(pdf, "rb")
        open_files.append(d)

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


def generateTexFiles(
    latex_directory,
    template_directory,
    number_group_pairs,
    test_list_variant,
    variant_name,
    title,
    semester,
    tests_per_group,
    pool_files,
):

    """

    This function replaces the variables within the tex problem/ solution files with the information given
    by the setting and returns the names of the according pdf files.

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

    :param pool_files: [0] list of names of problems for each pool, [1] name of pool
    :type pool_files: list[tuple]

    :return: [0] problem pdf names, [1] solution pdf names
    :rtype: list[tuple]

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

    file_names_problems_pdf = []
    file_names_solutions_pdf = []

    for group in range(number_group_pairs):
        group_name = f"{group*2 + 1:02d}{group*2+2:02d}"

        for test_index, test_typ in enumerate(test_list_variant):
            # Problem
            # Setting file name and path
            file_name = f"Exam-{variant_name}-{test_typ.name}-{group_name}.tex"
            file_path = os.path.join(latex_directory, file_name)

            # Replacing the parameters in the LaTeX file
            file_content = template_problem
            file_content = file_content.replace("__PRAKTIKUM__", title)
            file_content = file_content.replace("__SEMESTER__", semester)
            file_content = file_content.replace("__VERSUCH__", test_typ.name)
            file_content = file_content.replace("__GRUPPE__", group_name)

            # Creation of the problem strings + implementation in the LaTeX file
            # String has to  be adjusted for every pool, so that the correct
            # directory for each file is given
            # This could probably be solved more elegantly, but it works for now

            problem_string = ""
            for prob_sol in tests_per_group[group][test_index]:
                problem_string += f"\\item\n"
                pool_name = prob_sol[2]
                problem_string += f"\\input{{{pool_name}/{prob_sol[0]}}}\n\n"

            file_content = file_content.replace("__AUFGABEN__", problem_string)

            with open(file_path, "w+") as d:
                d.write(file_content)

            # LaTeX file of the problem is converted to PDF
            file_names_problems_pdf.append(file_name.replace(".tex", ".pdf"))

            # Solution
            # Setting file name and path
            file_name = f"Exam-{variant_name}-{test_typ.name}-{group_name}-Solution.tex"
            file_path = os.path.join(latex_directory, file_name)

            # Replacing parameters in LaTeX file
            file_content = template_solution
            file_content = file_content.replace("__PRAKTIKUM__", title)
            file_content = file_content.replace("__SEMESTER__", semester)
            file_content = file_content.replace("__VERSUCH__", test_typ.name)
            file_content = file_content.replace("__GRUPPE__", group_name)

            # Creation of the solution strings + implementation in the LaTeX file
            # String has to  be adjusted for every pool, so that the correct
            # directory for each file is given
            # This could probably be solved more elegantly, but it works for now
            solution_string = ""

            for prob_sol in tests_per_group[group][test_index]:
                solution_string += f"\\item\n"


                pool_name = prob_sol[2]
                solution_string += f"\\input{{{pool_name}/{prob_sol[1]}}}\n\n"

            file_content = file_content.replace("__AUFGABEN__", solution_string)

            with open(file_path, "w+") as d:
                d.write(file_content)

            # LaTeX file of the solution converted to pdf
            file_names_solutions_pdf.append(file_name.replace(".tex", ".pdf"))

    return file_names_problems_pdf, file_names_solutions_pdf


def combiningProblems(number_group_pairs, test_list_variant):

    """
    For each group this function adds to a list which contains
    problems and their according solutions from given pools
    depending on the test variant.

    :param number_group_pairs: Number of group pairs
    :type number_group_pairs: int

    :param test_list_variant: List of test variants belonging to chosen variant
    :type test_list_variant: list[TestType]

    :return: tests_per_group - problems/ solutions for each group
    :rtype: list[str]

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


def compile(test_directory, latex_directory, generate_single_pdfs, delete_temp_data):

    """
    This function compiles the tex files and turns them into pdf format and moves them to
    the test directory. Lastly, it deletes temporary data.

    :param test_directory: Directory where the generated tests are saved
    :type test_directory: str

    :param latex_directory: Working directory of latex compiler
    :type latex_directory: str

    :param generate_single_pdfs: Should individual PDFs be created
    :type generate_single_pdfs: bool

    :param delete_temp_data: Should temporary data be deleted
    :type delete_temp_data: bool
    """

    shutil.rmtree(test_directory, ignore_errors=True)
    os.mkdir(test_directory)
    os.chdir(latex_directory)

    if generate_single_pdfs:
        tex_files = [
            file for file in os.listdir(latex_directory) if file.endswith(".tex")
        ]

        for file in tex_files:
            # execute pdflatex twice to resolve references
            command = (
                f"pdflatex -interaction=batchmode {file} && "
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
                    f"{errorInfo()} Problem while compiling {file}. \
                    temporary data will not be deleted."
                )
            else:
                shutil.move(file.replace(".tex", ".pdf"), test_directory)

    # Delete temporary data
    # ToDo: mit python machen!
    if delete_temp_data:
        command = "del /Q *.dvi *.ps *.aux *.log *.tex"
        print(command)
        process = subprocess.Popen(command, shell=True)
        process.wait()
        if process.returncode != 0:
            raise CompilingError(f"{errorInfo()} Temporary data could not be deleted.")


def make_specific(make_all, pool, problem_path, root_directory):
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
    if pool is not None:
        FILENAME = "Preview_Pool_" + pool
        filenames_problems.extend(
            glob.glob(os.path.join(root_directory, f"pool_data/{pool}/problem*.tex"))
        )

    # if problem is provided, it is added to the preview creation list
    if problem_path is not None:
        abs_path = os.path.join(root_directory, problem_path)

        if not os.path.isfile(abs_path):
            abs_path = problem_path
            
        filenames_problems.extend(
            glob.glob(abs_path)
        )

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
        process = subprocess.Popen(
            "del {0}.aux {0}.log {0}.tex".format(FILENAME), shell=True
        )
    else:
        raise CompilingError(
            f"{errorInfo()}, Problem while compiling the template pdf file."
        )

    # creating new folder if not already existend
    if not os.path.isdir(specific_directory):
        os.mkdir(specific_directory)

    # moving pdf file to Previews directory
    shutil.move(FILENAME + ".pdf", specific_directory)


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


def pullPoolData(latex_directory):
    """
    Sets pool directories and its problem data.


    Args:
        latex_directory (str): working directory of latex compiler

    Returns:
        list[tuple(list[str], str)]: problem/ solution names, name of corresponding pool
    """
    pool_info = []

    for pool_name in os.listdir(latex_directory):
        pool_dir = os.path.join(latex_directory, pool_name)

        if not os.path.isdir(pool_dir):
            continue

        pool_data_list = [
            os.path.basename(fn) for fn in glob.iglob(os.path.join(pool_dir, "*.tex"))
        ]

        for file in pool_data_list:
            if "problem" not in file and  "solution" not in file:
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

def combineFileNames(pool_files):
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

def createCustomTestList(test_types_dictionary, pool_info):
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

            # checking if there is any problems/ solutions for the given pools
            # unnecessary because now done when initialising a pool instance
            """pool_files_exist = False
            for file in file_names_tex:
                if pool_name in file:
                    pool_files_exist = True

            if not pool_files_exist:
                raise SettingsError(
                    f"{errorInfo()} The pool {pool_name} does not have any \
                    problem/ solution files."
                )"""

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

def checkSettings(settings, settings_file):
    if not isinstance(settings.group_pairs, int):
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
            f"{errorInfo()} variant_name in {settings_file} is not of the required type string. \
            Please make sure all types match the ones given in the instructions."
        )

    if not isinstance(settings.semester, str):
        raise SettingsError(
            f"{errorInfo()} semester in {settings_file} is not of the required type string. \
            Please make sure all types match the ones given in the instructions."
        )

    if not isinstance(settings.sumo.pages_per_sheet_test, int):
        raise SettingsError(
            f"{errorInfo()} pages_per_sheet_test in {settings_file} is not of the required type int. \
            Please make sure all types match the ones given in the instructions."
        )

    if not isinstance(settings.sumo.sumo_problem_copies, int):
        raise SettingsError(
            f"{errorInfo()} sumo_number_copies in {settings_file} is not of the required type int. \
             Please make sure all types match the ones given in the instructions."
        )


    if not isinstance(settings.sumo.pages_per_sheet_solution, int):
        raise SettingsError(
            f"{errorInfo()} pages_per_sheet_solution in {settings_file} is not of the required type int. \
             Please make sure all types match the ones given in the instructions."
        )

    if not isinstance(settings.sumo.sumo_solution_copies, int):
        raise SettingsError(
            f"{errorInfo()} sumo_copies_per_solution in {settings_file} is not of the required type int. \
             Please make sure all types match the ones given in the instructions."
        )


    if not isinstance(settings.data.generate_single_pdfs, bool):
        raise SettingsError(
            f"{errorInfo()} generate_single_pdfs in {settings_file} is not of the required type bool. \
             Please make sure all types match the ones given in the instructions."
        )


    if not isinstance(settings.data.generate_sumo_pdf, bool):
        raise SettingsError(
            f"{errorInfo()} generate_sumo_pdf in {settings_file} is not of the required type bool. \
             Please make sure all types match the ones given in the instructions."
        )

    if not isinstance(settings.data.delete_temp_data, bool):
        raise SettingsError(
            f"{errorInfo()} delete_temp_data in {settings_file} is not of the required type bool. \
             Please make sure all types match the ones given in the instructions."
        )

    if settings.sumo.sumo_solution_copies < 1 or settings.sumo.sumo_problem_copies < 1:
        raise SettingsError(
            f"{errorInfo()} You have to have at least one copy for each test/ solution in {settings_file}."
        )

    if (settings.sumo.pages_per_sheet_test != 2) and (settings.sumo.pages_per_sheet_test != 4):
        raise SettingsError(
            f"{errorInfo()} Please choose between 2 (print problems in A4) or 4 (print problems in A5) pages \
            per sheet for your sumo problem/ solution files in {settings_file}."
        )
    
    if (settings.sumo.pages_per_sheet_solution != 2) and (settings.sumo.pages_per_sheet_solution != 4):
        raise SettingsError(
            f"{errorInfo()} Please choose between 2 (print problems in A4) or 4 (print problems in A5) pages \
            per sheet for your sumo problem/ solution files in {settings_file}."
        )

    if settings.group_pairs < 1:
        raise SettingsError(
            f"{errorInfo()} You have to have at least one group_pair in {settings_file}."
        )
