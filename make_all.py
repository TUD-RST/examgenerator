# Dieses Skript packt alle Aufgaben und Lösungen im Verzeichnis Latex/Aufgaben in eine
# Datei und compiliert diese in eine pdf-Datei mit dem in der Variablen DATEINAME
# festgelegten Namen.
#
# Nützlich zur Korrekturlesung etc.
import glob
import subprocess

DATEINAME = "alle_aufgaben"

filenames_aufgaben = glob.glob("Latex/Aufgaben/aufgabe*.tex")

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

    # Aufgaben und Lösungen
    for name in filenames_aufgaben:
        name = name.replace("\\", "/")
        f.write("\\textbf{{{0}}}\n\n".format(name.replace("_", "\\_")))
        f.write("\\input{{{0}}}\n\n".format(name))
        f.write("\\textbf{Lösung:}\\\\\n\n")
        f.write("\\input{{{0}}}\n\n".format(name.replace("aufgabe", "loesung")))
        f.write("\\hrulefill\n\n\n")

    # Dokumentende
    f.write("\\end{document}\n")

# Kompilieren und im Erfolgsfalle temporäre Dateien löschen
process = subprocess.Popen("pdflatex -interaction=nonstopmode {0}.tex".format(DATEINAME),
                           shell=True)
process.wait()

if process.returncode == 0:
    process = subprocess.Popen("del {0}.aux {0}.log".format(DATEINAME), shell=True)
else:
    print("Fehler")
