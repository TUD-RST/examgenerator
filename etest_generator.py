# Script zur Erstellung von Eingangstests für das Praktikum Regelungstechnik
#
# Aus einem Pool von Aufgaben werden Eingangstests für alle Versuche und alle Praktikumsgruppen
# erstellt und zwar so, dass sich die Aufgaben für eine Gruppe nicht wiederholen.
#
# Dazu gibt es im Verzeichnis Templates zwei LaTeX-Vorlagen: Eine für den Test, eine für
# die Musterlösung und Bewertung. In den Vorlagen gibt es Platzhalter, die von diesem Script
# mit dem entsprechenden Inhalt befüllt werden (Gruppennummer, Praktikumsname, Aufgaben, ...).
#
# Die Aufgaben finden sich im Verzeichnis Latex/Aufgaben. Diese ordnen sich nach allgemeinen
# Aufgaben, die in jedem Test vorkommen, und Aufgaben, die spezifisch für den jeweiligen Versuch
# sind. Die Zusammenstellung der Tests aus diesen Aufgaben erfolgt über Instanzen der Klasse
# TestTyp, die Verwaltung der Aufgaben über Instanzen vom Typ Pool. Die Lösungen sind in separaten
# Dateien abgelegt. Aufgabendateien haben das Präfix "aufgabe_", Lösungen das Präfix "loesung_".
# Das Schema lautet dann z.B.: aufgabe_A1_2.tex -> 2. Aufgabe vom Typ A1
#
# Die Teilaufgaben einer Aufgabe sollten mit der enumerate-Umgebung gegliedert werden.
#
# In den Lösungsdateien muss der Lösungstext in der Umgebung \begin{Loesung} \end{Loesung}
# liegen (anstelle von enumerate). Die Lösung einer jeden Teilaufgabe beginnt dann mit
# Schlüsselwort \lsgitem.
# ToDo: Wenn man alles in eine LaTeX-Klasse packt könnte man das vereinfachen
#
# In den Lösungen können mit dem Makro \Pkte{n} Punkte für die Teilaufgaben vergeben werden.
# Bei der Kompilierung werden die Punkte automatisch für die Aufgaben und den gesamten Test
# hochaddiert.
#
# Es besteht die Möglichkeit, alle erstellten Tests und die Musterlösung in einer einzigen Datei
# zusammenzufassen ("Sumo-Datei"). Dabei kann eingestellt werden, wie viele Kopien der Tests
# pro Doppelgruppe eingebunden werden. Dann kann man zu Beginn des Semesters
# gleich alles in einem Schwung ausdrucken. Dieses Vorgehen ist nur sinnvoll, wenn die Testaufgaben
# stabil sind und nicht mehr korrigiert werden müssen.
#
# Das Script nutzt einige Betriebssystembefehle, die derzeit nur für Windows implementiert sind.
import os
import shutil
import glob
import random
from warnings import warn
import re
import subprocess
from PyPDF2 import PdfFileReader, PdfFileWriter


# ================ Einstellungen Beginn =============================
# Festlegung, wie viel Gruppenpaare erzeugt werden sollen
# z.B. 6: Gruppen 01 bis 12
# 01+02, 03+04, etc. haben dann jeweils die gleichen Aufgaben
anzahl_gruppen = 5

# Studiengang, für den erzeugt werden soll.
# Mögliche Optionen: ET1, ET2, MT, RES
name_variante = "ET1"

# Semester
semester = "WS 2021/22"

# SUMO-pdf:
# Datei, die sämtliche Tests des Semesters zum Ausdruck enthält
# Dann kann man zu Beginn des Semesters gleich alles auf einen
# Schwung erzeugen und an die Betreuer verteilen
sumo_seiten_pro_blatt_test = 4  # 4 = Ausdruck doppelseitig A5
sumo_kopien_pro_test = 4  # Muss der Anzahl der Mitglieder pro Doppelgruppe entsprechen
sumo_seiten_pro_blatt_loesung = 4
sumo_kopien_pro_loesung = 1

# Einstellungen, was erzeugt und gelöscht werden soll.
generiere_einzel_pdfs = True
generiere_sumo_pdf = True
temp_dateien_loeschen = True
# ================ Einstellungen Ende =============================


class Pool:
    def __init__(self, name, dateinamen_tex):
        self.name = name
        """Name des Pools, z.B. A1, CV21, DV07"""

        self.stapel_verfuegbar = []
        """
        [(dateiname_aufgabe, dateiname_loesung)]; Zur Auswahl verfügbare Aufgaben
        """

        self.stapel_gezogen = []
        """
        [(dateiname_aufgabe, dateiname_loesung)]; Aufgaben, die für die aktuelle Gruppe gezogen 
        wurden
        """

        self.stapel_ablage = []
        """
        [(dateiname_aufgabe, dateiname_loesung)]; Aufgaben, die von den letzten Gruppen gezogen 
        wurden
        """

        aufgaben_regex = re.compile(f"^aufgabe_{name}_\\d+\\.tex$")
        dateinamen_pool_aufgaben = [datei for datei in dateinamen_tex if
                                    re.match(aufgaben_regex, datei) is not None]
        # Überprüfung, ob es im Pool Aufgaben gibt
        if len(dateinamen_pool_aufgaben) == 0:
            warn(f"Keine Aufgaben im Pool {self.name} gefunden")

        # Ordnet jeder Aufgabe die dazugehörige Lösung zu
        for datei in dateinamen_pool_aufgaben:
            datei_loesung = datei.replace("aufgabe", "loesung")

            # Hinzufügen der Aufgabe und Lösung zum Stapel
            if datei_loesung in dateinamen_tex:
                self.stapel_verfuegbar.append((datei, datei_loesung))

            # Warnung, falls keine passende Lösung gefunden
            else:
                warn(f"{datei} besitzt keine passende Loesungsdatei {datei_loesung}")

    def ziehen(self):
        if len(self.stapel_verfuegbar) == 0:
            # Stapel mit verfügbaren Aufgaben ist leer,
            # Ablagestapel wird zum neuen verfügbaren Stapel

            if len(self.stapel_ablage) > 0:
                self.stapel_verfuegbar = self.stapel_ablage
                self.stapel_ablage = []
            else:
                raise RuntimeError(
                    f"Pool {self.name} ist erschoepft, Aufgaben wuerden sich in Gruppe wiederholen")
        # Zufällige Auswahl einer Aufgabe+Lösung aus verfuegbaren Stapel
        aufg_loes = self.stapel_verfuegbar.pop(random.randint(0, len(self.stapel_verfuegbar) - 1))
        self.stapel_gezogen.append(aufg_loes)

        return aufg_loes

    def ablegen(self):
        self.stapel_ablage.extend(self.stapel_gezogen)
        self.stapel_gezogen = []


class TestTyp:
    def __init__(self, name, *pools):
        self.name = name
        """Name des Testtyps, wahrscheinlich der Name des Versuches, z.B. V21"""
        self.pools = pools
        """Liste von Pools, aus denen Aufgaben gezogen werden sollen"""

# ==================================
# --- Konfiguration ---
# ==================================
random.seed("WS2122")

# Arbeitsverzeichnis für den LaTeX-Compiler
latex_verzeichnis = os.path.join(os.getcwd(), "Latex")

# Verzeichnis mit den Vorlagen
template_verzeichnis = os.path.join(os.getcwd(), "Templates")

# Ausgabeverzeichnis für die erstellten Tests (z.B. Tests-ET1-WS201920)
test_verzeichnis = os.path.join(os.getcwd(), "Tests-{}-{}".format(name_variante, semester)).replace(
    " ", "").replace("/", "")

# Verzeichnis mit dem LaTeX-Quellcode der Aufgaben und Lösungen
aufgaben_verzeichnis = os.path.join(latex_verzeichnis, "Aufgaben")

# Dateinamen der Aufgaben
dateinamen_tex = [os.path.basename(fn) for fn in
                  glob.iglob(os.path.join(aufgaben_verzeichnis, "*.tex"))]


# Grundaufgaben, die in jedem Test vorkommen.
# A1, B1 -> für fünftes Semester RT sowie sechstes Semester MT sowie RES
# A2, B2 -> für sechstes Semester RT (benötigt Kenntnisse aus RT 2)
poolA1 = Pool("A1", dateinamen_tex)
poolB1 = Pool("B1", dateinamen_tex)
poolA2 = Pool("A2", dateinamen_tex)
poolB2 = Pool("B2", dateinamen_tex)

# Versuchsspezifische Aufgaben für V1, V3, V7, V8, V15 und V21
poolCV01 = Pool("CV01", dateinamen_tex)
poolCV03 = Pool("CV03", dateinamen_tex)
poolCV07 = Pool("CV07", dateinamen_tex)
poolCV08 = Pool("CV08", dateinamen_tex)
poolCV15 = Pool("CV15", dateinamen_tex)
poolCV21 = Pool("CV21", dateinamen_tex)

# Weitere versuchsspezifische Aufgaben, falls die aus C zu kurz sind
poolDV07 = Pool("DV07", dateinamen_tex)
poolDV08 = Pool("DV08", dateinamen_tex)
poolDV15 = Pool("DV15", dateinamen_tex)
poolDV21 = Pool("DV21", dateinamen_tex)

# Tests für RT1 sowie MT und RES-Praktikum
testV1 = TestTyp("V01", poolA1, poolB1, poolCV01)
testV7 = TestTyp("V07", poolA1, poolB1, poolCV07, poolDV07)
testV8_MT_RES = TestTyp("V08", poolA1, poolB1, poolCV08)
testV15_MT_RES = TestTyp("V15", poolA1, poolB1, poolCV15, poolDV15)
testV21 = TestTyp("V21", poolA1, poolB1, poolCV21, poolDV21)
test_liste_ET1 = [testV1, testV7, testV21]
test_liste_MT = [testV21, testV8_MT_RES]
test_liste_RES = [testV21, testV8_MT_RES, testV15_MT_RES]

# Tests für RT2 (6. Semester)
testV3 = TestTyp("V03", poolA2, poolB2, poolCV03)
testV8_ET = TestTyp("V08", poolA2, poolB2, poolCV08)
testV15_ET = TestTyp("V15", poolA2, poolB2, poolCV15, poolDV15)
test_liste_ET2 = [testV3, testV8_ET, testV15_ET]

# Zum debuggen
pool_all = Pool(".*", dateinamen_tex)
test_all = TestTyp("VX", *[pool_all for i in range(len(pool_all.stapel_verfuegbar))])
test_liste_all = [test_all]
# --------------

# Zuweisung der Testlisten zu den jeweiligen Praktika
if name_variante == "ET1":
    titel_praktikum = "Praktikum Regelungstechnik 1 (ET)"
    test_liste_variante = test_liste_ET1
elif name_variante == "ET2":
    titel_praktikum = "Praktikum Regelungstechnik 2 (ET)"
    test_liste_variante = test_liste_ET2
elif name_variante == "MT":
    titel_praktikum = "Praktikum Regelung \\& Steuerung (MT)"
    test_liste_variante = test_liste_MT
elif name_variante == "RES":
    titel_praktikum = "Praktikum Regelungstechnik (RES)"
    test_liste_variante = test_liste_RES
else:
    warn("Unbekannter Bezeichner. Gewünscht: ET1, ET2, MT oder RES!")
    test_liste_variante = []
    titel_praktikum = ""
    quit()

# ================================
# --- Kombination der Aufgaben ---
# ================================
test_saetze_pro_gruppe = []

for i in range(anzahl_gruppen):
    test_satz = []

    # Für jeden Test aus jedem Pool Aufgaben ziehen
    for test_typ in test_liste_variante:
        aufg_loes = []

        for pool in test_typ.pools:
            aufg_loes.append(pool.ziehen())

        test_satz.append(aufg_loes)

    # Für jeden genutzten Pool die gezogenen Aufgaben ablegen
    for test_typ in test_liste_variante:
        for pool in test_typ.pools:
            pool.ablegen()

    test_saetze_pro_gruppe.append(test_satz)

# ==================================
# --- Generieren der TeX-Dateien ---
# ==================================
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
        # Aufgabe
        # Festlegung des Dateinamens und Pfades
        datei_name = f"ETest-{name_variante}-{test_typ.name}-{gruppe_name}.tex"
        datei_pfad = os.path.join(latex_verzeichnis, datei_name)

        # Ersetzen der Dateiparameter in LaTeX mit Einstellungen
        datei_inhalt = template_aufgabe
        datei_inhalt = datei_inhalt.replace("__PRAKTIKUM__", titel_praktikum)
        datei_inhalt = datei_inhalt.replace("__SEMESTER__", semester)
        datei_inhalt = datei_inhalt.replace("__VERSUCH__", test_typ.name)
        datei_inhalt = datei_inhalt.replace("__GRUPPE__", gruppe_name)

        # Erstellen des Aufgabenstrings + Implementieren in LaTeX Datei
        aufgaben_string = ""
        for aufg_loes in test_saetze_pro_gruppe[gruppe][test_index]:
            aufgaben_string += f"\\item\n"
            aufgaben_string += f"\\input{{Aufgaben/{aufg_loes[0]}}}\n\n"

        datei_inhalt = datei_inhalt.replace("__AUFGABEN__", aufgaben_string)

        with open(datei_pfad, "w+") as d:
            d.write(datei_inhalt)

        # LaTeX Datei der Aufgaben in PDF umwandeln
        dateinamen_aufgaben_pdf.append(datei_name.replace(".tex", ".pdf"))

        # Lösung
        # Festlegung des Dateinamens und Pfades
        datei_name = f"ETest-{name_variante}-{test_typ.name}-{gruppe_name}-Loesung.tex"
        datei_pfad = os.path.join(latex_verzeichnis, datei_name)

        # Ersetzen der Dateiparameter in LaTeX mit Einstellungen
        datei_inhalt = template_loesung
        datei_inhalt = datei_inhalt.replace("__PRAKTIKUM__", titel_praktikum)
        datei_inhalt = datei_inhalt.replace("__SEMESTER__", semester)
        datei_inhalt = datei_inhalt.replace("__VERSUCH__", test_typ.name)
        datei_inhalt = datei_inhalt.replace("__GRUPPE__", gruppe_name)

        # Erstellen des Lösungsstrings + Implementieren in LaTeX Datei
        loesung_string = ""
        for aufg_loes in test_saetze_pro_gruppe[gruppe][test_index]:
            loesung_string += f"\\item\n"
            loesung_string += f"\\input{{Aufgaben/{aufg_loes[1]}}}\n\n"

        datei_inhalt = datei_inhalt.replace("__AUFGABEN__", loesung_string)

        with open(datei_pfad, "w+") as d:
            d.write(datei_inhalt)

        # LaTeX Datei der Lösungen in PDF umwandeln
        dateinamen_loesungen_pdf.append(datei_name.replace(".tex", ".pdf"))

# ===================
# --- Kompilieren ---
# ===================
shutil.rmtree(test_verzeichnis, ignore_errors=True)
os.mkdir(test_verzeichnis)
os.chdir(latex_verzeichnis)

if generiere_einzel_pdfs:
    tex_dateien = [datei for datei in os.listdir(latex_verzeichnis) if datei.endswith(".tex")]

    for datei in tex_dateien:
        # pdflatex 2 mal ausführen, um Referenzen aufzulösen
        command = f"pdflatex -interaction=batchmode {datei} && " \
                  f"pdflatex -interaction=batchmode {datei}"
        print(command)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL,
                                   stderr=subprocess.STDOUT)
        process.wait()
        if process.returncode != 0:
            warn(f"Problem beim Kompilieren von {datei}. "
                 f"Temporäre Dateien werden nicht gelöscht zur Fehlersuche.")
            temp_dateien_loeschen = False
        else:
            shutil.move(datei.replace(".tex", ".pdf"), test_verzeichnis)

# ToDo: mit python machen!
if temp_dateien_loeschen:
    command = 'del /Q *.dvi *.ps *.aux *.log'
    print(command)
    process = subprocess.Popen(command, shell=True)
    process.wait()
    if process.returncode != 0:
        warn("Temporaere Dateien konnten nicht geloescht werden")


# ==================================
# --- Sumo-Files ---
# ==================================
def baue_sumo(sumo_name, pdf_liste, seiten_pro_blatt, kopien_pro_datei):
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


if generiere_sumo_pdf:
    dateinamen_aufgaben_pdf.sort()
    sumo_aufgaben_name = f"Sumo-{name_variante}-Aufgaben.pdf"
    baue_sumo(sumo_aufgaben_name, dateinamen_aufgaben_pdf, sumo_seiten_pro_blatt_test,
              sumo_kopien_pro_test)

    dateinamen_loesungen_pdf.sort()
    sumo_loesungen_name = f"Sumo-{name_variante}-Loesungen.pdf"
    baue_sumo(sumo_loesungen_name, dateinamen_loesungen_pdf, sumo_seiten_pro_blatt_loesung,
              sumo_kopien_pro_loesung)
