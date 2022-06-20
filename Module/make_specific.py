# Dieses Skript packt alle ausgewählten Aufgaben und Loesungen der ausgewählten Pools, bzw. Einzeldateien  in eine
# Datei und kompiliert diese in eine pdf-Datei mit dem Namen, welcher über die json Datei festgelegt wird.
# 
#
# -*- coding: utf-8 -*-

# Die Einstellungen, welche Aufgaben/ Pools erstellt werden sollen erfolgen in einstellungen_make_specific.json
# Der Aufgabenname wird ohne den Suffix .tex angegeben.
#
# Nuetzlich zur Korrekturlesung etc.

import glob
import subprocess
import os
import shutil
from pathlib import Path

#-----------------Einstellungen--------------------#
def make_specific(make_all, pool, aufgabe):
    
    make_PoolA = False
    make_PoolB = False
    make_PoolC = False
    make_PoolD = False
    
    if pool is not None:
        if pool == "A":
           make_PoolA = True
        elif pool == "B":
            make_PoolB = True
        elif pool == "C":
            make_PoolC = True
        elif pool == "D":
            make_PoolD = True
        DATEINAME = "Preview_Pool_" + pool
    
    # Zusammensetzen der Liste mit den ausgewählten Aufgaben/ Pools
    filenames_aufgaben = []
    
    if make_PoolA:
        filenames_aufgaben.extend(glob.glob("Aufgaben/PoolA/aufgabe*.tex"))
    
    if make_PoolB:
        filenames_aufgaben.extend(glob.glob("Aufgaben/PoolB/aufgabe*.tex"))
    
    if make_PoolC:
        filenames_aufgaben.extend(glob.glob("Aufgaben/PoolC/aufgabe*.tex"))
        
    if make_PoolD:
        filenames_aufgaben.extend(glob.glob("Aufgaben/PoolD/aufgabe*.tex"))
        
    if aufgabe is not None:
        filenames_aufgaben.extend(glob.glob("Aufgaben/Pool*/" + aufgabe + ".tex"))
        DATEINAME = "Preview_" + aufgabe
    
    if make_all:
        filenames_aufgaben = glob.glob("Aufgaben/Pool*/*.tex")
        DATEINAME = "Preview_all"
    
    specific_verzeichnis = os.path.join(os.getcwd(), "Previews")
    
    # veraendert den Namen der Datei, falls bereits eine gleichbenannte vorhanden ist
    i = 1
    while Path(os.path.join(specific_verzeichnis, DATEINAME + ".pdf")).is_file():
        DATEINAME = DATEINAME + "_" + str(i)
        i += 1
        
        
        
    #---------------Einstellungen Ende-----------------#
    
    #-------------Erstellen der PDF Datei-------------#
    
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
        f.write("\\newcommand{\\diff}[3][]{\\frac{\\mathrm{d}^{#1}#2}{\\mathrm{d}{#3}^{#1}}}")
        f.write("\\newcommand{\\Pkte}[2][-999]{\\fbox{\\textcolor{red}{\\textbf{#2\\,P.}}}}\n")
        f.write("\\newenvironment{Loesung}{\\begin{enumerate}}{\\end{enumerate}}\n")
        f.write("\\newcommand{\\lsgitem}{\\item}\n")
        f.write("\\newcommand{\\abb}{\\\\[0,5cm]}\n")
        f.write("\\newcommand{\\ds}{\\displaystyle}\n")
        f.write("\\graphicspath{{Latex}}\n")
        f.write("\\begin{document}\n")
    
        # Aufgaben und Loesungen
        for name in filenames_aufgaben:
            name = name.replace("\\", "/")
            f.write("\\textbf{{{0}}}\n\n".format(name.replace("_", "\\_")))
            f.write("\\input{{{0}}}\n\n".format(name))
            f.write("\\textbf{Loesung:}\\\\\n\n")
            f.write("\\input{{{0}}}\n\n".format(name.replace("aufgabe", "loesung")))
            f.write("\\hrulefill\n\n\n")
    
        # Dokumentende
        f.write("\\end{document}\n")
    
    # Kompilieren und im Erfolgsfall temporaere Dateien loeschen
    process = subprocess.Popen("pdflatex -interaction=nonstopmode {0}.tex".format(DATEINAME),
                               shell=True)
    process.wait()
    
    if process.returncode == 0:
        process = subprocess.Popen("del {0}.aux {0}.log {0}.tex".format(DATEINAME), shell=True)
    else:
        print("Fehler")
    
    # Neuen Ordner erstellen, falls dieser noch nicht existiert
    if not os.path.isdir(specific_verzeichnis):
        os.mkdir(specific_verzeichnis)
    
    # PDF Datei in Ordner verschieben
    shutil.move(DATEINAME + ".pdf", specific_verzeichnis)
