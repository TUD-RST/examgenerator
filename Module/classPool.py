import random
from warnings import warn
import re

class Pool:
    """Repraesentiert die einzelnen Pools mit den dazugehoerigen Aufgaben.
    
    Konstruktion:
            
            >>> Pool(name, dateinamen_tex)
            
            * name:
                Der Name des Pools
                
            * dateinamen_tex:
                Liste aller Latex Aufgaben-Loesung-Dateinamen"""
            
    
    def __init__(self, name, dateinamen_tex):
        """Instanziert einen neuen Pool
        
        * name:
            Der Name des Pools z.B. A1, CV21, DV07
            
        * dateinamen_tex:
            Liste aller Latex Aufgaben-Loesung-Dateinamen"""
               
        self.name = name

        self.stapel_verfuegbar = []
        """
        [(dateiname_aufgabe, dateiname_loesung)]; Zur Auswahl verfuegbare Aufgaben
        """

        self.stapel_gezogen = []
        """
        [(dateiname_aufgabe, dateiname_loesung)]; Aufgaben, die fuer die aktuelle Gruppe gezogen 
        wurden
        """

        self.stapel_ablage = []
        """
        [(dateiname_aufgabe, dateiname_loesung)]; Aufgaben, die von den letzten Gruppen gezogen 
        wurden
        """
        # Erstellt eine Liste mit allen Aufgaben aus gefragten Pool
        aufgaben_regex = re.compile(f"^aufgabe_{name}_\\d+\\.tex$")
        dateinamen_pool_aufgaben = [datei for datei in dateinamen_tex if
                                    re.match(aufgaben_regex, datei) is not None]
        
        # Ueberpruefung, ob es im Pool Aufgaben mit dazugehörigen Loesungen gibt
        if len(dateinamen_pool_aufgaben) == 0:
            warn(f"Keine Aufgaben im Pool {self.name} gefunden")

        # Sucht nach der Loesung zur jeweiligen Aufgabe
        for datei in dateinamen_pool_aufgaben:
            datei_loesung = datei.replace("aufgabe", "loesung")

            # Hinzufuegen der Aufgabe und Loesung zum Stapel falls Lösung vorhanden
            if datei_loesung in dateinamen_tex:
                self.stapel_verfuegbar.append((datei, datei_loesung))

            # Warnung, falls keine passende Loesung gefunden
            else:
                warn(f"{datei} besitzt keine passende Loesungsdatei {datei_loesung}")

    def ziehen(self):
        """Zieht eine zufaellige Aufgabe + Loesung eines Pools"""
        if len(self.stapel_verfuegbar) == 0:
            # Stapel mit verfuegbaren Aufgaben ist leer,
            # Ablagestapel wird zum neuen verfuegbaren Stapel

            if len(self.stapel_ablage) > 0:
                self.stapel_verfuegbar = self.stapel_ablage
                self.stapel_ablage = []
            else:
                raise RuntimeError(
                    f"Pool {self.name} ist erschoepft, Aufgaben wuerden sich in Gruppe wiederholen")
        # Zufaellige Auswahl einer Aufgabe+Loesung aus verfuegbaren Stapel
        aufg_loes = self.stapel_verfuegbar.pop(random.randint(0, len(self.stapel_verfuegbar) - 1))
        self.stapel_gezogen.append(aufg_loes)

        return aufg_loes

    def ablegen(self):
        """Legt alle gezogen Aufgaben auf den Ablagestapel"""
        self.stapel_ablage.extend(self.stapel_gezogen)
        self.stapel_gezogen = []

