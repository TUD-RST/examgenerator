# -*- coding: utf-8 -*-

# Script zur Erstellung von Eingangstests fuer das Praktikum Regelungstechnik
#
# Aus einem Pool von Aufgaben werden Eingangstests fuer alle Versuche und alle Praktikumsgruppen
# erstellt und zwar so, dass sich die Aufgaben fuer eine Gruppe nicht wiederholen.
#
# Dazu gibt es im Verzeichnis Templates zwei LaTeX-Vorlagen: Eine fuer den Test, eine fuer
# die Musterloesung und Bewertung. In den Vorlagen gibt es Platzhalter, die von diesem Script
# mit dem entsprechenden Inhalt befuellt werden (Gruppennummer, Praktikumsname, Aufgaben, ...).
#
# Die Aufgaben finden sich im Verzeichnis Latex/Aufgaben. Diese ordnen sich nach allgemeinen
# Aufgaben, die in jedem Test vorkommen, und Aufgaben, die spezifisch fuer den jeweiligen Versuch
# sind. Die Zusammenstellung der Tests aus diesen Aufgaben erfolgt ueber Instanzen der Klasse
# TestTyp, die Verwaltung der Aufgaben ueber Instanzen vom Typ Pool. Die Loesungen sind in separaten
# Dateien abgelegt. Aufgabendateien haben das Praefix "aufgabe_", Loesungen das Praefix "loesung_".
# Das Schema lautet dann z.B.: aufgabe_A1_2.tex -> 2. Aufgabe vom Typ A1
#
# Die Teilaufgaben einer Aufgabe sollten mit der enumerate-Umgebung gegliedert werden.
#
# In den Loesungsdateien muss der Loesungstext in der Umgebung \begin{Loesung} \end{Loesung}
# liegen (anstelle von enumerate). Die Loesung einer jeden Teilaufgabe beginnt dann mit
# Schluesselwort \lsgitem.
# ToDo: Wenn man alles in eine LaTeX-Klasse packt koennte man das vereinfachen
#
# In den Aufgaben und Loesungen koennen mit dem Makro \Pkte{n} Punkte fuer die Teilaufgaben vergeben werden.
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
import glob
import random
from warnings import warn
import json
import argparse as ap

from Module import make_specific


def test_generator(args):
    
    if args.create_test is not None:
        # ================ Einstellungen =============================
        
        #%% click on the left to view options
        
        # Die Einstellungen werden ueber die einstellungen.json Datei festgelegt und dann in Python verarbeitet
        # Hier keine Veraenderung der Einstellungen!
        einstellungen = args.creat_test
        
        path_einstellungen = os.path.join(os.getcwd(), "Einstellungen", einstellungen)
        
        # Laden der Einstellungen aus json Datei in ein Python Dictionary
        with open(path_einstellungen, 'r') as json_datei:
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
        sumo_seiten_pro_blatt_test = einstellungen_dictionary['sumo']['sumo_seiten_pro_blatt_test']  
        # 4 = Ausdruck doppelseitig A5
        
        sumo_kopien_pro_test = einstellungen_dictionary['sumo']['sumo_kopien_pro_test']  
        # Muss der Anzahl der Mitglieder pro Doppelgruppe entsprechen
        
        sumo_seiten_pro_blatt_loesung = einstellungen_dictionary['sumo']['sumo_seiten_pro_blatt_loesung']
        sumo_kopien_pro_loesung = einstellungen_dictionary['sumo']['sumo_kopien_pro_loesung']
        
        # Einstellungen, was erzeugt und geloescht werden soll.
        generiere_einzel_pdfs = einstellungen_dictionary['loeschen_daten']['generiere_einzel_pdfs']
        generiere_sumo_pdf = einstellungen_dictionary['loeschen_daten']['generiere_sumo_pdf']
        temp_dateien_loeschen = einstellungen_dictionary['loeschen_daten']['temp_dateien_loeschen']
        #%%
        
        # ==================================
        # --- Klassen ---
        # ==================================
        
        
        from Module import Pool
        
        from Module import TestTyp
      
        
        # ==================================
        # --- Konfiguration ---
        # ==================================
        
        #%% click on the left to view configurations
        
        random.seed()
        
        # Arbeitsverzeichnis fuer den LaTeX-Compiler
        latex_verzeichnis = os.path.join(os.getcwd(), "Aufgaben")
        
        # Verzeichnis mit den Vorlagen
        template_verzeichnis = os.path.join(os.getcwd(), "Templates")
        
        # Ausgabeverzeichnis fuer die erstellten Tests (z.B. Tests-ET1-WS201920)
        test_verzeichnis = os.path.join(os.getcwd(), "Tests-{}-{}".format(name_variante, semester).replace(
            " ", "").replace("/", ""))
        
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
        
        
        #------------Custom Testtyp/ Testliste----------------#
        use_custom_test = einstellungen_dictionary['tests']['use_custom_test']
    
        #Loads the dictionary of custom tests
        test_types_dictionary_strings = einstellungen_dictionary['tests']['test_types']
    
        #will be final test list 
        custom_test_list = []
    
        #converts all test types (strings) to actual test types
        #and adds them to custom test list
        for i in range(test_types_dictionary_strings):
            custom_test_pools = []
            custom_test = []
            test_typ = test_types_dictionary_strings.get('test_typ' + str(i))
            custom_test_name = test_typ[0]
            test_typ = test_typ.pop(0)
            
            for a in range(len(test_typ)):
                custom_test_pools.append(Pool(test_typ[a], dateinamen_tex))
             
            custom_test = TestTyp(custom_test_name, *custom_test_pools)
            
            custom_test_list.append(custom_test)
        
        
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
            
        # Falls ein custom Test benutzt werden soll
        if use_custom_test:
            test_liste_variante = custom_test_list
        #%%    
        
        # ================================
        # --- Kombination der Aufgaben ---
        # ================================
        
        from Module import kombination_aufgaben
        
        test_saetze_pro_gruppe = kombination_aufgaben(anzahl_gruppen, test_liste_variante)
        
        # ==================================
        # --- Generieren der TeX-Dateien ---
        # ==================================
        
        from Module import generieren_tex_dateien
        
        # Erstellung des Tuples aus den Listen dateinamen_aufgaben_pdf, dateinamen_loesungen_pdf für Verarbeitung in Sumo
        namen_aufg_loesungen_pdf = generieren_tex_dateien(latex_verzeichnis, template_verzeichnis, anzahl_gruppen, test_liste_variante,
                               name_variante, titel_praktikum, semester, test_saetze_pro_gruppe)
     
        
        
        # ===================
        # --- Kompilieren ---
        # ===================
        from Module import kompilieren
        
        kompilieren(test_verzeichnis, latex_verzeichnis, generiere_einzel_pdfs, temp_dateien_loeschen)
    
        
        # ==================================
        # --- Sumo-Files ---
        # ==================================
        
        
        from Module import baue_sumo
        
        if generiere_sumo_pdf:
            namen_aufg_loesungen_pdf[0].sort()
            sumo_aufgaben_name = f"Sumo-{name_variante}-Aufgaben.pdf"
            baue_sumo(test_verzeichnis, sumo_aufgaben_name, namen_aufg_loesungen_pdf[0], sumo_seiten_pro_blatt_test,
                      sumo_kopien_pro_test)
        
            namen_aufg_loesungen_pdf[1].sort()
    
    
    
            sumo_loesungen_name = f"Sumo-{name_variante}-Loesungen.pdf"
            baue_sumo(test_verzeichnis, sumo_loesungen_name, namen_aufg_loesungen_pdf[1], sumo_seiten_pro_blatt_loesung,
                      sumo_kopien_pro_loesung)
    

    # ==================================
    # --- Make-Specific ---
    # ==================================
    
    if args.make_all or args.make_pool or args.make_specific:
        make_specific(args.make_all, args.make_pool, args.make_specific)
        
        

 # ==========================================================
 
 # ==========================================================
 
if __name__ == "__main__":
    
    parser = ap.ArgumentParser()
    
    parser.add_argument('-ct', '--create_test', help=u'Erstellt einen fertigen Test, nach den Einstellungen aus der\
                        angegeben json Datei')
    parser.add_argument('-ma','--make_all', action = 'store_true', help=u'Erstellt eine Preview Datei fuer alle Aufgaben')
    parser.add_argument('-mp','--make_pool', choices = ['A', 'B', 'C', 'D'], help=u'Erstellt eine Preview Datei mit den Aufgaben\
                        des angegeben Pools')
    parser.add_argument('-ms','--make_specific', help=u'Erstellt eine Preview Datei fuer eine ausgewaehlte Aufgabe (ohne .tex)')
    
    args = parser.parse_args()    
    
    if ((args.create_test is None) and (args.make_all == False) and (args.make_pool is None) and (args.make_specific is None)):
        parser.error('Bitte geben Sie an, was generiert werden soll. Für Hilfe benutzen Sie: -h')
        
    else:
        test_generator(args)