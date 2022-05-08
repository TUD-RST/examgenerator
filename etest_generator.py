# Script zur Erstellung von Eingangstests fuer das Praktikum Regelungstechnik
#
# Aus einem Pool von Aufgaben werden Eingangstests fuer alle Versuche und alle Praktikumsgruppen
# erstellt und zwar so, dass sich die Aufgaben fÃ¼r eine Gruppe nicht wiederholen.
#
# Dazu gibt es im Verzeichnis Templates zwei LaTeX-Vorlagen: Eine fuer den Test, eine fuer
# die Musterloesung und Bewertung. In den Vorlagen gibt es Platzhalter, die von diesem Script
# mit dem entsprechenden Inhalt befuellt werden (Gruppennummer, Praktikumsname, Aufgaben, ...).
#
# Die Aufgaben finden sich im Verzeichnis Latex/Aufgaben. Diese ordnen sich nach allgemeinen
# Aufgaben, die in jedem Test vorkommen, und Aufgaben, die spezifisch fuer den jeweiligen Versuch
# sind. Die Zusammenstellung der Tests aus diesen Aufgaben erfolgt ueber Instanzen der Klasse
# TestTyp, die Verwaltung der Aufgaben ueber Instanzen vom Typ Pool. Die Loesungen sind in separaten
# Dateien abgelegt. Aufgabendateien haben das PrÃ¤fix "aufgabe_", Loesungen das Praefix "loesung_".
# Das Schema lautet dann z.B.: aufgabe_A1_2.tex -> 2. Aufgabe vom Typ A1
#
# Die Teilaufgaben einer Aufgabe sollten mit der enumerate-Umgebung gegliedert werden.
#
# In den Loesungsdateien muss der Loesungstext in der Umgebung \begin{Loesung} \end{Loesung}
# liegen (anstelle von enumerate). Die Loesung einer jeden Teilaufgabe beginnt dann mit
# Schluesselwort \lsgitem.
# ToDo: Wenn man alles in eine LaTeX-Klasse packt koennte man das vereinfachen
#
# In den Loesungen koennen mit dem Makro \Pkte{n} Punkte fuer die Teilaufgaben vergeben werden.
# Bei der Kompilierung werden die Punkte automatisch fuer die Aufgaben und den gesamten Test
# hochaddiert.
#
# Es besteht die Moeglichkeit, alle erstellten Tests und die Musterloesung in einer einzigen Datei
# zusammenzufassen ("Sumo-Datei"). Dabei kann eingestellt werden, wie viele Kopien der Tests
# pro Doppelgruppe eingebunden werden. Dann kann man zu Beginn des Semesters
# gleich alles in einem Schwung ausdrucken. Dieses Vorgehen ist nur sinnvoll, wenn die Testaufgaben
# stabil sind und nicht mehr korrigiert werden muessen.
#
# Das Script nutzt einige Betriebssystembefehle, die derzeit nur fuer Windows implementiert sind.
import os
import shutil
import glob
import random
from warnings import warn
import subprocess
from PyPDF2 import PdfFileReader, PdfFileWriter
import json


# ================ Einstellungen Beginn =============================

# Die Einstellungen werden ueber die einstellungen.json Datei festgelegt und dann in Python verarbeitet
# Hier keine Veraenderung der Einstellungen!

# Laden der Einstellungen aus json Datei in ein Python Dictionary
with open('einstellungen.json', 'r') as json_datei:
    einstellungen_dictionary = json.load(json_datei)

# Festlegung, wie viele Gruppenpaare erzeugt werden sollen
# z.B. 6: Gruppen 01 bis 12
# 01+02, 03+04, etc. haben dann jeweils die gleichen Aufgaben
anzahl_gruppen = einstellungen_dictionary['anzahl_gruppen']

# Studiengang, fuer den erzeugt werden soll.
# Moegliche Optionen: ET1, ET2, MT, RES
name_variante = einstellungen_dictionary['name_variante']

# Semester
semester = einstellungen_dictionary['semester']

# SUMO-pdf:
# Datei, die saemtliche Tests des Semesters zum Ausdruck enthÃ¤lt
# Dann kann man zu Beginn des Semesters gleich alles auf einen
# Schwung erzeugen und an die Betreuer verteilen
sumo_seiten_pro_blatt_test = einstellungen_dictionary['sumo']['sumo_seiten_pro_blatt_test']  # 4 = Ausdruck doppelseitig A5
sumo_kopien_pro_test = einstellungen_dictionary['sumo']['sumo_kopien_pro_test']  # Muss der Anzahl der Mitglieder pro Doppelgruppe entsprechen
sumo_seiten_pro_blatt_loesung = einstellungen_dictionary['sumo']['sumo_seiten_pro_blatt_loesung']
sumo_kopien_pro_loesung = einstellungen_dictionary['sumo']['sumo_kopien_pro_loesung']

# Einstellungen, was erzeugt und geloescht werden soll.
generiere_einzel_pdfs = einstellungen_dictionary['loeschen_daten']['generiere_einzel_pdfs']
generiere_sumo_pdf = einstellungen_dictionary['loeschen_daten']['generiere_sumo_pdf']
temp_dateien_loeschen = einstellungen_dictionary['loeschen_daten']['temp_dateien_loeschen']


# ==================================
# --- Klassen ---
# ==================================

from Module import Pool

from Module import TestTyp

# ==================================
# --- Konfiguration ---
# ==================================

random.seed("WS2122")

# Arbeitsverzeichnis fuer den LaTeX-Compiler
latex_verzeichnis = os.path.join(os.getcwd(), "Aufgaben")

# Verzeichnis mit den Vorlagen
template_verzeichnis = os.path.join(os.getcwd(), "Templates")

# Ausgabeverzeichnis fuer die erstellten Tests (z.B. Tests-ET1-WS201920)
test_verzeichnis = os.path.join(os.getcwd(), "Tests-{}-{}".format(name_variante, semester)).replace(
    " ", "").replace("/", "")

# Verzeichnis mit dem LaTeX-Quellcode der Aufgaben und Loesungen
poolA_verzeichnis = os.path.join(latex_verzeichnis, "poolA")
poolB_verzeichnis = os.path.join(latex_verzeichnis, "poolB")
poolC_verzeichnis = os.path.join(latex_verzeichnis, "poolC")
poolD_verzeichnis = os.path.join(latex_verzeichnis, "poolD")


# Erstellt für jeden Pool Liste mit den Dateinamen der Aufgaben und Lösungen
dateinamen_poolA_tex = [os.path.basename(fn) for fn in
                  glob.iglob(os.path.join(poolA_verzeichnis, "*.tex"))]

dateinamen_poolB_tex = [os.path.basename(fn) for fn in
                  glob.iglob(os.path.join(poolB_verzeichnis, "*.tex"))]

dateinamen_poolC_tex = [os.path.basename(fn) for fn in
                  glob.iglob(os.path.join(poolC_verzeichnis, "*.tex"))]

dateinamen_poolD_tex = [os.path.basename(fn) for fn in
                  glob.iglob(os.path.join(poolD_verzeichnis, "*.tex"))]

# Fügt die Liste der einzelnen Pools zusammen
dateinamen_tex = (dateinamen_poolA_tex + dateinamen_poolB_tex + 
                  dateinamen_poolC_tex + dateinamen_poolD_tex)
                
                             

# Grundaufgaben, die in jedem Test vorkommen.
# A1, B1 -> fuer fuenftes Semester RT sowie sechstes Semester MT sowie RES
# A2, B2 -> fuer sechstes Semester RT (benoetigt Kenntnisse aus RT 2)
poolA1 = Pool("A1", dateinamen_tex)
poolB1 = Pool("B1", dateinamen_tex)
poolA2 = Pool("A2", dateinamen_tex)
poolB2 = Pool("B2", dateinamen_tex)

# Versuchsspezifische Aufgaben fuer V1, V3, V7, V8, V15 und V21
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

# Tests fuer RT1 sowie MT und RES-Praktikum
testV1 = TestTyp("V01", poolA1, poolB1, poolCV01)
testV7 = TestTyp("V07", poolA1, poolB1, poolCV07, poolDV07)
testV8_MT_RES = TestTyp("V08", poolA1, poolB1, poolCV08)
testV15_MT_RES = TestTyp("V15", poolA1, poolB1, poolCV15, poolDV15)
testV21 = TestTyp("V21", poolA1, poolB1, poolCV21, poolDV21)
test_liste_ET1 = [testV1, testV7, testV21]
test_liste_MT = [testV21, testV8_MT_RES]
test_liste_RES = [testV21, testV8_MT_RES, testV15_MT_RES]

# Tests fuer RT2 (6. Semester)
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
    warn("Unbekannter Bezeichner. Gewuenscht: ET1, ET2, MT oder RES!")
    test_liste_variante = []
    titel_praktikum = ""
    quit()

# ================================
# --- Kombination der Aufgaben ---
# ================================
test_saetze_pro_gruppe = []

for i in range(anzahl_gruppen):
    test_satz = []

    # Fuer jeden Test aus jedem Pool Aufgaben ziehen
    for test_typ in test_liste_variante:
        aufg_loes = []

        for pool in test_typ.pools:
            aufg_loes.append(pool.ziehen())

        test_satz.append(aufg_loes)

    # Fuer jeden genutzten Pool die gezogenen Aufgaben ablegen
    for test_typ in test_liste_variante:
        for pool in test_typ.pools:
            pool.ablegen()

    test_saetze_pro_gruppe.append(test_satz)

# ==================================
# --- Generieren der TeX-Dateien ---
# ==================================

# Loescht alle Dateien im Aufgaben Ordner 
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
        # Der String muss für jeden Pool angepasst werden, damit auf das
        # richtige Verzeichnis zugegriffen wird, daher werden die Tuples abgefragt
        aufgaben_string = ""
        for aufg_loes in test_saetze_pro_gruppe[gruppe][test_index]:
            aufgaben_string += f"\\item\n"
                
            if "A" in aufg_loes[0]:
                aufgaben_string += f"\\input{{poolA/{aufg_loes[0]}}}\n\n"
            
            if "B" in aufg_loes[0]:
                aufgaben_string += f"\\input{{poolB/{aufg_loes[0]}}}\n\n"
            
            if "C" in aufg_loes[0]:
                aufgaben_string += f"\\input{{poolC/{aufg_loes[0]}}}\n\n"
            
            if "D" in aufg_loes[0]:
                aufgaben_string += f"\\input{{poolD/{aufg_loes[0]}}}\n\n"

        datei_inhalt = datei_inhalt.replace("__AUFGABEN__", aufgaben_string)

        with open(datei_pfad, "w+") as d:
            d.write(datei_inhalt)

        # LaTeX Datei der Aufgaben in PDF umwandeln
        dateinamen_aufgaben_pdf.append(datei_name.replace(".tex", ".pdf"))

        # Loesung
        # Festlegung des Dateinamens und Pfades
        datei_name = f"ETest-{name_variante}-{test_typ.name}-{gruppe_name}-Loesung.tex"
        datei_pfad = os.path.join(latex_verzeichnis, datei_name) 

        # Ersetzen der Dateiparameter in LaTeX mit Einstellungen
        datei_inhalt = template_loesung
        datei_inhalt = datei_inhalt.replace("__PRAKTIKUM__", titel_praktikum)
        datei_inhalt = datei_inhalt.replace("__SEMESTER__", semester)
        datei_inhalt = datei_inhalt.replace("__VERSUCH__", test_typ.name)
        datei_inhalt = datei_inhalt.replace("__GRUPPE__", gruppe_name)

        # Erstellen des Loesungsstrings + Implementieren in LaTeX Datei
        # Der String muss für jeden Pool angepasst werden, damit auf das
        # richtige Verzeichnis zugegriffen wird, daher werden die Tuples abgefragt
        loesung_string = ""
        for aufg_loes in test_saetze_pro_gruppe[gruppe][test_index]:
            loesung_string += f"\\item\n"
            
            if "A" in aufg_loes[0]:
                 loesung_string += f"\\input{{poolA/{aufg_loes[1]}}}\n\n"
             
            if "B" in aufg_loes[0]:
                 loesung_string += f"\\input{{poolB/{aufg_loes[1]}}}\n\n"
             
            if "C" in aufg_loes[0]:
                 loesung_string += f"\\input{{poolC/{aufg_loes[1]}}}\n\n"
             
            if "D" in aufg_loes[0]:
                loesung_string += f"\\input{{poolD/{aufg_loes[1]}}}\n\n"

        datei_inhalt = datei_inhalt.replace("__AUFGABEN__", loesung_string)

        with open(datei_pfad, "w+") as d:
            d.write(datei_inhalt)

        # LaTeX Datei der Loesungen in PDF umwandeln
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
        # pdflatex 2 mal ausfuehren, um Referenzen aufzuloesen
        command = f"pdflatex -interaction=batchmode {datei} && " \
                  f"pdflatex -interaction=batchmode {datei}"
        print(command)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL,
                                   stderr=subprocess.STDOUT)
        process.wait()
        if process.returncode != 0:
            warn(f"Problem beim Kompilieren von {datei}. "
                 f"Temporaere Dateien werden nicht geloescht zur Fehlersuche.")
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
