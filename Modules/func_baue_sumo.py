import os
from PyPDF2 import PdfFileReader, PdfFileWriter


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
