def kombination_aufgaben(anzahl_gruppen, test_liste_variante):
    
   """For each group this function adds to a list which contains
       problems and their according solutions from given pools
       depending on the test variant.
       
      input: anzahl_gruppen, test_liste_variante
      
      output: test_saetze_pro_gruppe"""
    
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
       
   return test_saetze_pro_gruppe