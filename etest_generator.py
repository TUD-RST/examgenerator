# -*- coding: utf-8 -*-
"""
This script creates tests based on given problems and settings

From a pool of problems, test will be created in  a way, that there will be no
repetition for all experiments and groups.

There is two LaTeX templates in the Templates Directory:
One for the problems and one for the sample solution and evaluation.
In these templates there is placeholders, which will be replaced by
this script.

The problems are located in the Aufgaben directory which is furthermore separated into
the main pools (PoolA, PoolB, PoolC, PoolD). They usually differ between general problems,
that are used in every test, and problems, that are specific for the given experiment.

Tests are combined via instances of the class TestTyp and managed via instances of the class Pool.
Solutions are saved in separate files.
Files for problems have the prefix "aufgabe_", solutions the prefix "loesung_".
The scheme is the following: 
    aufgabe_A1_2.tex -> 2. problem of type A1
or for an experiment:
    aufgabe_CV03_1.tex -> 2. problem from experiment (V) number 03 of type C
for a more detailed breakdown of the nomenclature view the read.me file in the Aufgaben folder
Please avoid using combinations of more than one capital letter describing your pools
except for combinations with V (which stands for experiment) since this could lead to 
problems during the compiling process.

Subtasks of a problem should be structured in an enumerate-surrounding.

Within the solution files the solution text has to be written in between
\begin{Loesung} \end{Loesung}. The solution of every subtask starts with the 
key \lsgitem.

It is possible to assign points to problems and solutions with the macro \Pkte{n}.
During the compiling process the given points will be added automatically for the entire test

Optionally, all tests and sample solutions can be combined into one "sumo-file". 
This allows creating the tests for the entire semester in one go. However, this
is only useful if the problems and solutions are final and will not have to be corrected
afterwards.

There is the following options for the test creation, which can be configured in a
json settings file:
    
    * anzahl_gruppen:
        Determines the amount of group pairs
        for example:  6 => group pairs 01-12
        
    * name_variante:
        Name of the variant/ degree the test is created for 
        There already exists prefactored tests for:
            * ET1
            * ET2
            * MT
            * RES
        If you would like to create a custom test, you have a free choice with the name
    
    * semester:
        Current Semester
        for example: WS 2021/22
    
    * sumo_seiten_pro_blatt_test:
        4 - double paged A5
    
    * sumo_kopien_pro_test:
       Number of copies per test
    
    * sumo_seiten_pro_blatt_loesung:
        4 - double paged A5
    
    * generiere_einzel_pdf:
        Should individual pdf files be created for each problem/ solution (true/ false)
    
    * generiere_sumo_pdf:
        Should a sumo-file be created (true/ false)
    
    * temp_dateien_loeschen:
        Should temporary data be deleted (true; false)
        true is recommendet unless there is issues with compiling
    
    * use_custom_test:
        Should a custom test with self-defined test types and lists be created? (true/ false)
        If you would like to use a prefactored test, this setting has to be on false!
        
        If you would like to create a custom test, you will have to provide the test types
        as lists in the json settings file. If you only provide one test type, that one will
        be used. If you provide multiple, the script will choose randomly from them.
        The first argument of the list is the name of the test type and all following arguments
        are the pools to be used for the test. When adding another test type it is important
        to following the ascending nomenclature in the test_types dictionary. For more info
        you can have a look at the settings template under Einstellungen/einstellungen.json
        

Calling Syntax:
-------------

This script can either be called with the help of a python interpreter
or --in case python is not installed on the working computer-- as a
stand-alone application. The second scenario only works on Windows.

**Syntax when using a python interpreter**::
    
    python etest_generator.py [-h] [-ct] SETTINGS_FILE [-ma] [-mp] POOL [-ms] PROBLEM
   
**Syntax for the stand-alone application**::
    
    etest_generator.exe [-h] [-ct] SETTINGSFILE [-ma] [-mp] POOL [-ms] PROBLEM
    
Based on the sample template it is possible to create as many settings templates to your
liking. They have to be saved in the Einstellung directory.

With these it is now possible to easily create tests:
    
    * -ct [name of the chosen settings file.json] (--create_test [name of the chosen settings file.json])
        creates a folder in which the created tests, based on the provided settings, are saved
            
Additionally, the script can help with the creation/ review of problems/ solutions:
    
    * -ma (--make_all) 
        creates a folder Previews in which a file with a preview for every problem/ solution is displayed
      
    * -mp [Pool] (--make_pool [Pool]) 
        creates a preview file for all problems/ solutions for the given pool
      
    * -ms [name of the problem] (--make_specific [name of the problem]) 
        creates a preview file for the given problem
        name of the problem without ".tex"

In order to recieve help type:
    
    * -h (--help)

This script uses operating commands, which are currently only implemented on Windows.

"""

import os
import glob
import random
from warnings import warn
import json
import argparse as ap
import textwrap as tw


def test_generator(args):
    """
    Main function which combines all modules of this program.
    
    Parameters:
        
        * args.create_test:
            Would the user like to create a test
        
        * args.make_all:
            Would the user like to create a preview for all problems
        
        * args.make_pool
            Pool which the user would like to create a preview for
        
        * args.make_specific
            Name of the problem the user would like to create a preview for
    """
    if args.create_test is not None:
        # ================ Settings =============================
        
        #%% click on the left to view options
        
        # Settings are adjusted in the settings json files in the Einstellungen directory and then loaded into Python
        # No change of settings in this program!
        einstellungen = args.create_test
        
        path_einstellungen = os.path.join(os.getcwd(), "Einstellungen", str(einstellungen))
        
        # Loading the json settings into a Python dictionary
        with open(path_einstellungen, 'r') as json_datei:
            einstellungen_dictionary = json.load(json_datei)
        
        # Determines the amount of group pairs
        # for example:  6 => group pairs 01-12
        # 01+02, 03+04, ..., have the same problems
        anzahl_gruppen = einstellungen_dictionary['anzahl_gruppen']
        
        # Degree for which the test is created
        # Prefactored options: ET1, ET2, MT, RES
        name_variante = einstellungen_dictionary['name_variante']
        
        # Semester
        semester = einstellungen_dictionary['semester']
        
        # SUMO-pdf:
        # File contains all tests for the entire semester
        # Creates the test for the whole smester in one go
        sumo_seiten_pro_blatt_test = einstellungen_dictionary['sumo']['sumo_seiten_pro_blatt_test']  
        # 4 = printing double paged A5
        
        sumo_kopien_pro_test = einstellungen_dictionary['sumo']['sumo_kopien_pro_test']  
        # Has to match the number of participants per groups
        
        sumo_seiten_pro_blatt_loesung = einstellungen_dictionary['sumo']['sumo_seiten_pro_blatt_loesung']
        sumo_kopien_pro_loesung = einstellungen_dictionary['sumo']['sumo_kopien_pro_loesung']
        
        # Settings of what should be created and deleted
        generiere_einzel_pdfs = einstellungen_dictionary['loeschen_daten']['generiere_einzel_pdfs']
        generiere_sumo_pdf = einstellungen_dictionary['loeschen_daten']['generiere_sumo_pdf']
        temp_dateien_loeschen = einstellungen_dictionary['loeschen_daten']['temp_dateien_loeschen']
        #%%
        
        # ==================================
        # --- Classes ---
        # ==================================
        
        
        from Module import Pool
        
        from Module import TestTyp
      
        
        # ==================================
        # --- Configuration ---
        # ==================================
        
        #%% click on the left to view configurations
        
        random.seed()
        
        # Working directory for the LaTeX compiler
        latex_verzeichnis = os.path.join(os.getcwd(), "Aufgaben")
        
        # Template directory
        template_verzeichnis = os.path.join(os.getcwd(), "Templates")
        
        # Directory where the tests will be saved in (for example: Tests-ET1-WS201920)
        test_verzeichnis = os.path.join(os.getcwd(), "Tests-{}-{}".format(name_variante, semester).replace(
            " ", "").replace("/", ""))
        
        # Directory with the LaTeX source code for the problems (prob. unnecessary, working on it)
        poolA_verzeichnis = os.path.join(latex_verzeichnis, "poolA")
        poolB_verzeichnis = os.path.join(latex_verzeichnis, "poolB")
        poolC_verzeichnis = os.path.join(latex_verzeichnis, "poolC")
        poolD_verzeichnis = os.path.join(latex_verzeichnis, "poolD")
        poolE_verzeichnis = os.path.join(latex_verzeichnis, "poolE")
        poolF_verzeichnis = os.path.join(latex_verzeichnis, "poolF")
        poolG_verzeichnis = os.path.join(latex_verzeichnis, "poolG")
        poolH_verzeichnis = os.path.join(latex_verzeichnis, "poolH")
        
        
        
        
        # Creates a list of problem names for every pool (probably unnecessary, working on it)
        dateinamen_poolA_tex = [os.path.basename(fn) for fn in
                          glob.iglob(os.path.join(poolA_verzeichnis, "*.tex"))]
        
        dateinamen_poolB_tex = [os.path.basename(fn) for fn in
                          glob.iglob(os.path.join(poolB_verzeichnis, "*.tex"))]
        
        dateinamen_poolC_tex = [os.path.basename(fn) for fn in
                          glob.iglob(os.path.join(poolC_verzeichnis, "*.tex"))]
        
        dateinamen_poolD_tex = [os.path.basename(fn) for fn in
                          glob.iglob(os.path.join(poolD_verzeichnis, "*.tex"))]
        
        dateinamen_poolE_tex = [os.path.basename(fn) for fn in
                          glob.iglob(os.path.join(poolE_verzeichnis, "*.tex"))]
        
        dateinamen_poolF_tex = [os.path.basename(fn) for fn in
                          glob.iglob(os.path.join(poolF_verzeichnis, "*.tex"))]
        
        dateinamen_poolG_tex = [os.path.basename(fn) for fn in
                          glob.iglob(os.path.join(poolG_verzeichnis, "*.tex"))]
        
        dateinamen_poolH_tex = [os.path.basename(fn) for fn in
                          glob.iglob(os.path.join(poolH_verzeichnis, "*.tex"))]
        
        
        # combines the list of pools
        dateinamen_tex = (dateinamen_poolA_tex + dateinamen_poolB_tex + 
                          dateinamen_poolC_tex + dateinamen_poolD_tex +
                          dateinamen_poolE_tex + dateinamen_poolF_tex +
                          dateinamen_poolG_tex + dateinamen_poolH_tex)
                        
     #   pool_verzeichnis =  os.path.join(latex_verzeichnis, "pool*")
        
     #   dateinamen_tex = [os.path.basename(fn) for fn in
     #                     glob.iglob(os.path.join(pool_verzeichnis, "*.tex"))]
                                   
        
        # General problems for each test
        # A1, B1 -> for 5th Semester RT and 6th semester MT and RES
        # A2, B2 -> for 6th Semester RT (knowledge from RT 2 required)
        poolA1 = Pool("A1", dateinamen_tex)
        poolB1 = Pool("B1", dateinamen_tex)
        poolA2 = Pool("A2", dateinamen_tex)
        poolB2 = Pool("B2", dateinamen_tex)
        
        # Experiment specific problems for V1, V3, V7, V8, V15 und V21
        poolCV01 = Pool("CV01", dateinamen_tex)
        poolCV03 = Pool("CV03", dateinamen_tex)
        poolCV07 = Pool("CV07", dateinamen_tex)
        poolCV08 = Pool("CV08", dateinamen_tex)
        poolCV15 = Pool("CV15", dateinamen_tex)
        poolCV21 = Pool("CV21", dateinamen_tex)
        
        # More experiment specific problems, if there is not enough from C
        poolDV07 = Pool("DV07", dateinamen_tex)
        poolDV08 = Pool("DV08", dateinamen_tex)
        poolDV15 = Pool("DV15", dateinamen_tex)
        poolDV21 = Pool("DV21", dateinamen_tex)
        
        
        #------------Custom Testtype/ Testlist----------------#
        use_custom_test = einstellungen_dictionary['use_custom_test']
    
        # Loads the dictionary of custom tests
        test_types_dictionary_strings = einstellungen_dictionary['test_types']
    
        # will be final test list 
        custom_test_list = []
    
        # converts all test types (strings) to actual test types
        # and adds them to custom test list
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
        
        
        # Tests for RT1, MT and RES courses
        testV1 = TestTyp("V01", poolA1, poolB1, poolCV01)
        testV7 = TestTyp("V07", poolA1, poolB1, poolCV07, poolDV07)
        testV8_MT_RES = TestTyp("V08", poolA1, poolB1, poolCV08)
        testV15_MT_RES = TestTyp("V15", poolA1, poolB1, poolCV15, poolDV15)
        testV21 = TestTyp("V21", poolA1, poolB1, poolCV21, poolDV21)
        test_liste_ET1 = [testV1, testV7, testV21]
        test_liste_MT = [testV21, testV8_MT_RES]
        test_liste_RES = [testV21, testV8_MT_RES, testV15_MT_RES]
        
        # Tests for RT2 (6th Semester)
        testV3 = TestTyp("V03", poolA2, poolB2, poolCV03)
        testV8_ET = TestTyp("V08", poolA2, poolB2, poolCV08)
        testV15_ET = TestTyp("V15", poolA2, poolB2, poolCV15, poolDV15)
        test_liste_ET2 = [testV3, testV8_ET, testV15_ET]
        
        # for debugging
        pool_all = Pool(".*", dateinamen_tex)
        test_all = TestTyp("VX", *[pool_all for i in range(len(pool_all.stapel_verfuegbar))])
        test_liste_all = [test_all]
        # --------------
        
        # Assigning test lists to given variants
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
            
        # If a custom test is used
        if use_custom_test:
            titel_praktikum = f"Praktikum-{name_variante}"
            test_liste_variante = custom_test_list
        #%%    
        
        # ================================
        # --- Kombination der Aufgaben ---
        # ================================
        
        from Module import kombination_aufgaben
        
        test_saetze_pro_gruppe = kombination_aufgaben(anzahl_gruppen, test_liste_variante)
        
        # ==================================
        # --- Generating the TeX-Files ---
        # ==================================
        
        from Module import generieren_tex_dateien
        
        # Creating the the tuple which contains the pdf names of the problems and solutions
        # for more info view the module
        namen_aufg_loesungen_pdf = generieren_tex_dateien(latex_verzeichnis, template_verzeichnis, anzahl_gruppen, test_liste_variante,
                               name_variante, titel_praktikum, semester, test_saetze_pro_gruppe)
     
        
        
        # ===================
        # --- Compiling ---
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
   
    from Module import make_specific
    
    if args.make_all or args.make_pool or args.make_specific:
        make_specific(args.make_all, args.make_pool, args.make_specific)
        
        

 # ==========================================================
 
 # ==========================================================
 
if __name__ == "__main__":
    Descr = tw.dedent(u'''\
                      This script creates tests based on given problems and settings

                      From a pool of problems, test will be created in  a way, that there will be no
                      repetition for all experiments and groups.

                      There is two LaTeX templates in the Templates Directory:
                      One for the problems and one for the sample solution and evaluation.
                      In these templates there is placeholders, which will be replaced by
                      this script.

                      The problems are located in the Aufgaben directory which is furthermore separated into
                      the main pools (PoolA, PoolB, PoolC, PoolD). They usually differ between general problems,
                      that are used in every test, and problems, that are specific for the given experiment.

                      Tests are combined via instances of the class TestTyp and managed via instances of the class Pool.
                      Solutions are saved in separate files.
                      Files for problems have the prefix "aufgabe_", solutions the prefix "loesung_".
                      The scheme is the following: 
                          aufgabe_A1_2.tex -> 2. problem of type A1
                      or for an experiment:
                          aufgabe_CV03_1.tex -> 2. problem from experiment (V) number 03 of type C
                      for a more detailed breakdown of the nomenclature view the read.me file in the Aufgaben folder
                      Please avoid using combinations of more than one capital letter describing your pools
                      except for combinations with V (which stands for experiment) since this could lead to 
                      problems during the compiling process.

                      Subtasks of a problem should be structured in an enumerate-surrounding.

                      Within the solution files the solution text has to be written in between
                      \begin{Loesung} \end{Loesung}. The solution of every subtask starts with the 
                      key \lsgitem.

                      It is possible to assign points to problems and solutions with the macro \Pkte{n}.
                      During the compiling process the given points will be added automatically for the entire test

                      Optionally, all tests and sample solutions can be combined into one "sumo-file". 
                      This allows creating the tests for the entire semester in one go. However, this
                      is only useful if the problems and solutions are final and will not have to be corrected
                      afterwards.''')
                      
    parser = ap.ArgumentParser(description = Descr)
    
    parser.add_argument('-ct', '--create_test', help=u'Creates a test based on the provided json settings file')
    parser.add_argument('-ma','--make_all', action = 'store_true', help=u'Creates a preview for all problems')
    parser.add_argument('-mp','--make_pool', choices = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'], 
                        help=u'Creates a Preview for all problems of the given pool')
    parser.add_argument('-ms','--make_specific', help=u'Creates a Preview for only the given problem\
                        you will need to provide them problem´s name (without .tex)')
    
    args = parser.parse_args()    
    
    if ((args.create_test is None) and (args.make_all == False) and (args.make_pool is None) and (args.make_specific is None)):
        parser.error('Please choose at least one of the options. For help type: -h')
        
    else:
        test_generator(args)