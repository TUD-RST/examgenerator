"""
This module contains all functions relevant for the exam-generator.
"""

import os
from PyPDF2 import PdfFileReader, PdfFileWriter
import glob
import subprocess
import shutil
from pathlib import Path
from warnings import warn

def baue_sumo(
    test_verzeichnis, sumo_name, pdf_liste, seiten_pro_blatt, kopien_pro_datei
):

    """
    This function creates the sumo file which contains all problems/ solutions for all groups.

    :param test_verzeichnis: Directory in which the created tests are saved
    :type test_verzeichnis: str

    :param sumo_name: Name of the Sumo file either for the problems or solutions
    :type sumo_name: str

    :param pdf_liste: List of the names of the created PDF problem/ solution files
    :type pdf_liste: list[str]

    :param seiten_pro_blatt: How many different pages there should be displayed on one page/ sheet
    :type seiten_pro_blatt: int

    :param kopien_pro_blatt: How many copies you would like for each problem/ solution
    :type kopien_pro_blatt: int

    Creates:

        * pdf file sumo_name.pdf
    
    """

    os.chdir(test_verzeichnis)
    writer = PdfFileWriter()

    open_files = []
    for pdf in pdf_liste:
        d = open(pdf, "rb")
        open_files.append(d)

        reader = PdfFileReader(d)
        num_pages = reader.getNumPages()
        mehr_als_vielfaches = num_pages % seiten_pro_blatt
        if mehr_als_vielfaches == 0:
            blank_pages = 0
        else:
            blank_pages = seiten_pro_blatt - mehr_als_vielfaches

        for kopie in range(kopien_pro_datei):
            for page in range(num_pages):
                writer.addPage(reader.getPage(page))
            for blank_page in range(blank_pages):
                writer.addBlankPage()

    with open(sumo_name, "wb+") as d:
        writer.write(d)

    for d in open_files:
        d.close()


def generieren_tex_dateien(
    latex_verzeichnis,
    template_verzeichnis,
    anzahl_gruppen,
    test_liste_variante,
    name_variante,
    titel_praktikum,
    semester,
    test_saetze_pro_gruppe,
    pool_dateien,
):

    """
    
    This function replaces the variables within the tex problem/ solution files with the information given
    by the setting and returns the names of the according pdf files.

    :param latex_verzeichnis: Directory for the latex compiler
    :type latex_verzeichnis: str

    :param template_verzeichnis: Directory of the problem/ solution templates
    :type template_verzeichnis: int

    :param anzahl_gruppe: Number of group pairs
    :type anzahl_gruppe: int

    :param test_liste_variante: List of test variants belonging to chosen variant
    :type test_liste_variante: list[testtyp]

    :param name_variante: Name of the test variant
    :type name_variante: str

    :param titel_praktikum: Title of the event. Dependent on name_variant
    :type titel_praktikum: str

    :param semester: Given semester in json settings file
    :type semester: str

    :param test_saetze_pro_gruppe: List of problems/ solutions for each group
    :type test_saetze_pro_gruppe: list[str]

    :param pool_dateien: [0] list of names of problems for each pool, [1] name of pool
    :type pool_dateien: list[tuple]

    :return: [0] problem pdf names, [1] solution pdf names       
    :rtype: list[tuple]  

    """

    # Deletes all temporary files in the Aufgaben directory
    for file in glob.glob(os.path.join(latex_verzeichnis, "*.*")):
        os.remove(file)

    template_aufgabe_pfad = os.path.join(template_verzeichnis, "template_aufgabe.tex")
    template_loesung_pfad = os.path.join(template_verzeichnis, "template_loesung.tex")

    with open(template_aufgabe_pfad, "r") as d:
        template_aufgabe = d.read()
    with open(template_loesung_pfad, "r") as d:
        template_loesung = d.read()

    dateinamen_aufgaben_pdf = []
    dateinamen_loesungen_pdf = []

    for gruppe in range(anzahl_gruppen):
        gruppe_name = f"{gruppe*2 + 1:02d}{gruppe*2+2:02d}"

        for test_index, test_typ in enumerate(test_liste_variante):
            # Problem
            # Setting file name and path
            datei_name = f"ETest-{name_variante}-{test_typ.name}-{gruppe_name}.tex"
            datei_pfad = os.path.join(latex_verzeichnis, datei_name)

            # Replacing the parameters in the LaTeX file
            datei_inhalt = template_aufgabe
            datei_inhalt = datei_inhalt.replace("__PRAKTIKUM__", titel_praktikum)
            datei_inhalt = datei_inhalt.replace("__SEMESTER__", semester)
            datei_inhalt = datei_inhalt.replace("__VERSUCH__", test_typ.name)
            datei_inhalt = datei_inhalt.replace("__GRUPPE__", gruppe_name)

            # Creation of the problem strings + implementation in the LaTeX file
            # String has to  be adjusted for every pool, so that the correct
            # directory for each file is given
            # This could probably be solved more elegantly, but it works for now

            aufgaben_string = ""

            for aufg_loes in test_saetze_pro_gruppe[gruppe][test_index]:
                aufgaben_string += f"\\item\n"

                for pool_tuple in pool_dateien:
                    if aufg_loes[0] in pool_tuple[0]:
                        pool_name = str(pool_tuple[1])
                        aufgaben_string += (
                            f"\\input{{pool{pool_name}/{aufg_loes[0]}}}\n\n"
                        )

            datei_inhalt = datei_inhalt.replace("__AUFGABEN__", aufgaben_string)

            with open(datei_pfad, "w+") as d:
                d.write(datei_inhalt)

            # LaTeX file of the problem is converted to PDF
            dateinamen_aufgaben_pdf.append(datei_name.replace(".tex", ".pdf"))

            # Solution
            # Setting file name and path
            datei_name = (
                f"ETest-{name_variante}-{test_typ.name}-{gruppe_name}-Loesung.tex"
            )
            datei_pfad = os.path.join(latex_verzeichnis, datei_name)

            # Replacing parameters in LaTeX file
            datei_inhalt = template_loesung
            datei_inhalt = datei_inhalt.replace("__PRAKTIKUM__", titel_praktikum)
            datei_inhalt = datei_inhalt.replace("__SEMESTER__", semester)
            datei_inhalt = datei_inhalt.replace("__VERSUCH__", test_typ.name)
            datei_inhalt = datei_inhalt.replace("__GRUPPE__", gruppe_name)

            # Creation of the solution strings + implementation in the LaTeX file
            # String has to  be adjusted for every pool, so that the correct
            # directory for each file is given
            # This could probably be solved more elegantly, but it works for now
            loesung_string = ""

            for aufg_loes in test_saetze_pro_gruppe[gruppe][test_index]:
                loesung_string += f"\\item\n"

                for pool_tuple in pool_dateien:
                    if aufg_loes[0] in pool_tuple[0]:
                        pool_name = pool_tuple[1]
                        loesung_string += (
                            f"\\input{{pool{pool_name}/{aufg_loes[1]}}}\n\n"
                        )

            datei_inhalt = datei_inhalt.replace("__AUFGABEN__", loesung_string)

            with open(datei_pfad, "w+") as d:
                d.write(datei_inhalt)

            # LaTeX file of the solution converted to pdf
            dateinamen_loesungen_pdf.append(datei_name.replace(".tex", ".pdf"))

    return dateinamen_aufgaben_pdf, dateinamen_loesungen_pdf


def kombination_aufgaben(anzahl_gruppen, test_liste_variante):

    """
    For each group this function adds to a list which contains
    problems and their according solutions from given pools
    depending on the test variant.

    :param anzahl_gruppe: Number of group pairs
    :type anzahl_gruppe: int

    :param test_liste_variante: List of test variants belonging to chosen variant
    :type test_liste_variante: list[testtyp]

    :return: test_saetze_pro_gruppe - problems/ solutions for each group
    :rtype: list[str]
    
    """

    test_saetze_pro_gruppe = []

    for i in range(anzahl_gruppen):
        test_satz = []

        # For each test from every pool a problem is pulled
        for test_typ in test_liste_variante:
            aufg_loes = []

            for pool in test_typ.pools:
                aufg_loes.append(pool.ziehen())

            test_satz.append(aufg_loes)

        # Sets aside the used problems of each pool
        for test_typ in test_liste_variante:
            for pool in test_typ.pools:
                pool.ablegen()

        test_saetze_pro_gruppe.append(test_satz)

    return test_saetze_pro_gruppe


def kompilieren(
    test_verzeichnis, latex_verzeichnis, generiere_einzel_pdfs, temp_dateien_loeschen
):

    """
    This function compiles the tex files and turns them into pdf format and moves them to
    the test directory. Lastly, it deletes temporary data.

    :param test_verzeichnis: Directory where the generated tests are saved
    :type test_verzeichnis: str

    :param latex_verzeichnis: Working directory of latex compiler
    :type latex_verzeichnis: str

    :param generiere_einzel_pdf: Should individual PDFs be created
    :type generiere_einzel_pdf: bool

    :param temp_dateien_loeschen: Should temporary data be deleted
    :type temp_dateien_loeschen: bool
    """

    shutil.rmtree(test_verzeichnis, ignore_errors=True)
    os.mkdir(test_verzeichnis)
    os.chdir(latex_verzeichnis)

    if generiere_einzel_pdfs:
        tex_dateien = [
            datei for datei in os.listdir(latex_verzeichnis) if datei.endswith(".tex")
        ]

        for datei in tex_dateien:
            # execute pdflatex twice to resolve references
            command = (
                f"pdflatex -interaction=batchmode {datei} && "
                f"pdflatex -interaction=batchmode {datei}"
            )
            print(command)
            process = subprocess.Popen(
                command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
            )
            process.wait()
            if process.returncode != 0:
                warn(
                    f"Problem while compiling {datei}. "
                    f"Temporary data will not be deleted."
                )
                temp_dateien_loeschen = False
            else:
                shutil.move(datei.replace(".tex", ".pdf"), test_verzeichnis)

    # Delete temporary data
    # ToDo: mit python machen!
    if temp_dateien_loeschen:
        command = "del /Q *.dvi *.ps *.aux *.log *.tex"
        print(command)
        process = subprocess.Popen(command, shell=True)
        process.wait()
        if process.returncode != 0:
            warn("Temporary data could not be deleted")


def make_specific(make_all, pool, aufgabe, root_directory):
    """
    This Function creates previews for given pools/ problems or all.

    :param make_all: Make a preview for all problems
    :type make_all: bool

    :param pool: Name of the pool to be created
    :type pool: str

    :aufgabe: File name of the problem to be created
    :type aufgabe: str
    """

    # list of problems to be created
    filenames_aufgaben = []

    # if a pool is selected, all its problems will be added to the creation list
    if pool is not None:
        DATEINAME = "Preview_Pool_" + pool
        filenames_aufgaben.extend(glob.glob(os.path.join(root_directory, "Problems/Pool" + pool + "/aufgabe*.tex")))

    # if problem is provided, it is added to the preview creation list
    if aufgabe is not None:
        filenames_aufgaben.extend(glob.glob(os.path.join(root_directory, "Problems/Pool*/" + aufgabe + ".tex")))
        DATEINAME = "Preview_" + aufgabe

    # if make_all is selected the preview creation list contains all problems
    if make_all:
        filenames_aufgaben = glob.glob(os.path.join(root_directory, "Problems/Pool*/*.tex"))
        DATEINAME = "Preview_all"

    specific_verzeichnis = os.path.join(root_directory, "Previews")

    # veraendert den Namen der Datei, falls bereits eine gleichbenannte vorhanden ist
    i = 1
    while Path(os.path.join(specific_verzeichnis, DATEINAME + ".pdf")).is_file():
        if i > 10:
            DATEINAME = DATEINAME[:-2] + str(i)
        if i > 100:
            warn(
                "Maximum amount of previews for a single file is reached. Please delete unnecessary files."
            )
            quit()
        if i < 11:
            DATEINAME = DATEINAME[:-1] + str(i)
        i += 1

    # ---------------Settings End-----------------#

    # -------------Creation of the PDF File-------------#

    with open("{0}.tex".format(DATEINAME), "w", encoding="utf-8") as f:
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
        for name in filenames_aufgaben:
            name = name.replace("\\", "/")
            f.write("\\textbf{{{0}}}\n\n".format(name.replace("_", "\\_")))
            f.write("\\input{{{0}}}\n\n".format(name))
            f.write("\\textbf{Loesung:}\\\\\n\n")
            f.write("\\input{{{0}}}\n\n".format(name.replace("aufgabe", "loesung")))
            f.write("\\hrulefill\n\n\n")

        # Document end
        f.write("\\end{document}\n")

    # compiling and if successful deleting temporary data
    process = subprocess.Popen(
        "pdflatex -interaction=nonstopmode {0}.tex".format(DATEINAME), shell=True
    )
    process.wait()

    if process.returncode == 0:
        process = subprocess.Popen(
            "del {0}.aux {0}.log {0}.tex".format(DATEINAME), shell=True
        )
    else:
        print("Fehler")

    # creating new folder if not already existend
    if not os.path.isdir(specific_verzeichnis):
        os.mkdir(specific_verzeichnis)

    # moving pdf file to Previews directory
    shutil.move(DATEINAME + ".pdf", specific_verzeichnis)