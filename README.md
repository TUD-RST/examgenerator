# Eingangstests für das Praktikum Regelungstechnik

**Diese können wie folgt generiert werden:**

```bash
python3 etest_generator.py
```

**Folgende Anpassungsmöglichkeiten gibt es für ``etest_generator.py``**
**Die Einstellungen erfolgen in ``einstellungen.json``**

```python
# ================ Einstellungen Beginn =============================
# Festlegung, wieviel Gruppenpaare erzeugt werden sollen
# z.B. 6: Gruppen 01 bis 12
# 01+02, 03+04, etc. haben jeweils die gleichen Aufgaben
anzahl_gruppen = 6

# Studiengang, für den erzeugt werden soll.
# Mögliche Optionen: ET1, ET2, MT, RES
name_variante = "ET1"

# Semester
semester = "WS 2019/20"

# Für Datei, die sämtliche Tests des Semesters zum Ausdruck enthält
sumo_seiten_pro_blatt_test = 4  # 4 = doppelseitig A5
sumo_kopien_pro_test = 6
sumo_seiten_pro_blatt_loesung = 4
sumo_kopien_pro_loesung = 1

# Einstellungen, was erzeugt und gelöscht werden soll.
generiere_einzel_pdfs = True
generiere_sumo_pdf = True
temp_dateien_loeschen = True
# ================ Einstellungen Ende =============================
```

Die generierten Tests finden sich dann im Verzeichnis
``Tests-[Studiengang]-[Semester]`` wieder.

**Ausgewählte Dateien/ Pools können wie folgt generiert werden:**
```bash
python3 make_specific.py
```
**Die Einstellungen hierfür erfolgen in ``einstellungen_make_specific.json``**

```json
{
 "datei_name": "Ihr Dateiname",
 "make_PoolA": false,
 "make_PoolB": false,
 "make_PoolC": false,
 "make_PoolD": false,
 "make_einzel_datei": false,
 "name_einzel_datei": "Name der ausgewählten Aufgabe"
}
```
