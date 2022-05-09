import os
import shutil
from warnings import warn
import subprocess

def kompilieren(test_verzeichnis, latex_verzeichnis, generiere_einzel_pdfs, temp_dateien_loeschen):

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

