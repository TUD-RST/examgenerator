import os
import glob


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
