import random
from warnings import warn
import re


class Pool:
    """Represents each pool with its corresponding problems.

    Construction:

            >>> Pool(name, dateinamen_tex)

            * name:
                name of the pool

            * dateinamen_tex:
                list of all Problem-Solution-file names"""

    def __init__(self, name, dateinamen_tex):
        """creates new pool instance

        * name:
            name of the pool for example: A1, CV21, DV07

        * dateinamen_tex:
            list of all Problem-Solution-file names"""

        self.name = name

        self.stapel_verfuegbar = []
        """
        [(dateiname_aufgabe, dateiname_loesung)]; problems that can be chosen from
        """

        self.stapel_gezogen = []
        """
        [(dateiname_aufgabe, dateiname_loesung)]; selected problems for corresponding group
        """

        self.stapel_ablage = []
        """
        [(dateiname_aufgabe, dateiname_loesung)]; problems which were pulled by last group
        """
        # Erstellt eine Liste mit allen Aufgaben aus gefragten Pool
        aufgaben_regex = re.compile(f"^aufgabe_{name}_\\d+\\.tex$")
        dateinamen_pool_aufgaben = [
            datei
            for datei in dateinamen_tex
            if re.match(aufgaben_regex, datei) is not None
        ]

        # Ueberpruefung, ob es im Pool Aufgaben mit dazugehörigen Loesungen gibt
        if len(dateinamen_pool_aufgaben) == 0:
            warn(f"The is no more problems available in Pool {self.name}")

        # Sucht nach der Loesung zur jeweiligen Aufgabe
        for datei in dateinamen_pool_aufgaben:
            datei_loesung = datei.replace("aufgabe", "loesung")

            # Hinzufuegen der Aufgabe und Loesung zum Stapel falls Lösung vorhanden
            if datei_loesung in dateinamen_tex:
                self.stapel_verfuegbar.append((datei, datei_loesung))

            # Warnung, falls keine passende Loesung gefunden
            else:
                warn(
                    f"{datei} does not have a corresponding solution file {datei_loesung}"
                )

    def ziehen(self):
        """Pulls a random problem + solution from the pool"""
        if len(self.stapel_verfuegbar) == 0:
            # Stapel mit verfuegbaren Aufgaben ist leer,
            # Ablagestapel wird zum neuen verfuegbaren Stapel

            if len(self.stapel_ablage) > 0:
                self.stapel_verfuegbar = self.stapel_ablage
                self.stapel_ablage = []
            else:
                raise RuntimeError(
                    f"Pool {self.name} ist echausted, problems might repeat within the group"
                )
        # Zufaellige Auswahl einer Aufgabe+Loesung aus verfuegbaren Stapel
        aufg_loes = self.stapel_verfuegbar.pop(
            random.randint(0, len(self.stapel_verfuegbar) - 1)
        )
        self.stapel_gezogen.append(aufg_loes)

        return aufg_loes

    def ablegen(self):
        """Discards all pulled problems to the discard pile"""
        self.stapel_ablage.extend(self.stapel_gezogen)
        self.stapel_gezogen = []
