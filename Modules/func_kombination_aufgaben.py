def kombination_aufgaben(anzahl_gruppen, test_liste_variante):

    """For each group this function adds to a list which contains
     problems and their according solutions from given pools
     depending on the test variant.

    Parameters:

      * anzahl_gruppen:
          Number of different groups
          Defined in json settings file

      * test_liste_variante:
          List of test variants belonging to chosen overall variant
          Can be indirectly customized in json settings file by changing/ adding test types

    Returns:

      * test_saetze_pro_gruppe:
          List of problems/ solutions for each group"""

    test_saetze_pro_gruppe = []

    for i in range(anzahl_gruppen):
        test_satz = []

        # For each test from every pool a problem is pulled
        for test_typ in test_liste_variante:
            aufg_loes = []

            for pool in test_typ.pools:
                aufg_loes.append(pool.ziehen())

            test_satz.append(aufg_loes)

        # Sets aside the used problems of each pool
        for test_typ in test_liste_variante:
            for pool in test_typ.pools:
                pool.ablegen()

        test_saetze_pro_gruppe.append(test_satz)

    return test_saetze_pro_gruppe
