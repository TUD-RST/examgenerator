import os
import shutil
from warnings import warn
import subprocess


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
