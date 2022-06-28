# -*- coding: utf-8 -*-

import glob
import subprocess
import os
import shutil
from pathlib import Path

#-----------------Settings--------------------#
def make_specific(make_all, pool, aufgabe):
    """
    This Function creates previews for given pools/ problems or all.
    
    Parameters:
        
        * make_all: 
            Boolean: make a preview for all problems
        
        * pool:
            Name of the pool to be created
        
        * aufgabe:
            File name of the problem to be made"""
     
    """        
    # Default
    make_PoolA = False
    make_PoolB = False
    make_PoolC = False
    make_PoolD = False
    make_PoolE = False
    make_PoolF = False
    make_PoolG = False
    make_PoolH = False
    
    if pool is not None:
        if pool == "A":
           make_PoolA = True
        elif pool == "B":
            make_PoolB = True
        elif pool == "C":
            make_PoolC = True
        elif pool == "D":
            make_PoolD = True
        elif pool == "E":
            make_PoolE = True
        elif pool == "F":
            make_PoolF = True
        elif pool == "G":
            make_PoolG = True
        elif pool == "H":
            make_PoolH = True
          
        DATEINAME = "Preview_Pool_" + pool
        """
    
    # list of problems to be created
    filenames_aufgaben = []
    
    # if a pool is selected, all its problems will be added to the creation list
    if pool is not None:
        DATEINAME = "Preview_Pool_" + pool
        filenames_aufgaben.extend(glob.glob("Aufgaben/Pool" + pool + "/aufgabe*.tex"))
        
        """ 
    if make_PoolA:
        filenames_aufgaben.extend(glob.glob("Aufgaben/PoolA/aufgabe*.tex"))
    
    if make_PoolB:
        filenames_aufgaben.extend(glob.glob("Aufgaben/PoolB/aufgabe*.tex"))
    
    if make_PoolC:
        filenames_aufgaben.extend(glob.glob("Aufgaben/PoolC/aufgabe*.tex"))
        
    if make_PoolD:
        filenames_aufgaben.extend(glob.glob("Aufgaben/PoolD/aufgabe*.tex"))
        
    if make_PoolE:
        filenames_aufgaben.extend(glob.glob("Aufgaben/PoolE/aufgabe*.tex"))
        
    if make_PoolF:
        filenames_aufgaben.extend(glob.glob("Aufgaben/PoolF/aufgabe*.tex"))
        
    if make_PoolG:
        filenames_aufgaben.extend(glob.glob("Aufgaben/PoolG/aufgabe*.tex"))
        
    if make_PoolH:
        filenames_aufgaben.extend(glob.glob("Aufgaben/PoolH/aufgabe*.tex"))"""
    
    # if problem is provided, it is added to the preview creation list
    if aufgabe is not None:
        filenames_aufgaben.extend(glob.glob("Aufgaben/Pool*/" + aufgabe + ".tex"))
        DATEINAME = "Preview_" + aufgabe
    
    # if make_all is selected the preview creation list contains all problems
    if make_all:
        filenames_aufgaben = glob.glob("Aufgaben/Pool*/*.tex")
        DATEINAME = "Preview_all"
    
    specific_verzeichnis = os.path.join(os.getcwd(), "Previews")
    
    # veraendert den Namen der Datei, falls bereits eine gleichbenannte vorhanden ist
    i = 1
    while Path(os.path.join(specific_verzeichnis, DATEINAME + ".pdf")).is_file():
        DATEINAME = DATEINAME + "_" + str(i)
        i += 1
        
        
        
    #---------------Settings End-----------------#
    
    #-------------Creation of the PDF File-------------#
    
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
    process = subprocess.Popen("pdflatex -interaction=nonstopmode {0}.tex".format(DATEINAME),
                               shell=True)
    process.wait()
    
    if process.returncode == 0:
        process = subprocess.Popen("del {0}.aux {0}.log {0}.tex".format(DATEINAME), shell=True)
    else:
        print("Fehler")
    
    # creating new folder if not already existend
    if not os.path.isdir(specific_verzeichnis):
        os.mkdir(specific_verzeichnis)
    
    # moving pdf file to Previews directory
    shutil.move(DATEINAME + ".pdf", specific_verzeichnis)
