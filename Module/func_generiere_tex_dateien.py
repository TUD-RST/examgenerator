# Das Script nutzt einige Betriebssystembefehle, die derzeit nur fuer Windows implementiert sind.
import os
import glob


def generieren_tex_dateien(latex_verzeichnis, template_verzeichnis, anzahl_gruppen, test_liste_variante,
                           name_variante, titel_praktikum, semester, test_saetze_pro_gruppe):
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
            
    return dateinamen_aufgaben_pdf, dateinamen_loesungen_pdf
