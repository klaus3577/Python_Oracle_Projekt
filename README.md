# Egyetemi Adatkezelő Rendszer (Python + Oracle)

Python alapú adatkezelő alkalmazás, amely egy egyetemi domain modellt (egyetemek,
hallgatók, kurzusok, beiratkozások) generál, több fájlformátumban tárol és olvas
vissza, relációs Oracle-adatbázisban kezel, végül összesítő, diagramos elemzési
riportot készít. A projekt a teljes adat-életutat lefedi: **generálás → tárolás →
adatbázis → elemzés**.

## Funkciók

- **Adatgenerálás** valósághű tesztadatokkal (Faker), objektumorientált modellel
  (Python `dataclass`-ok).
- **Több formátumú tárolás és visszaolvasás:** CSV, JSON és XLSX, újrahasznosítható
  handler-osztályokkal.
- **Relációs adatbázis:** Oracle táblák létrehozása elsődleges és külső kulcsokkal,
  `ON DELETE CASCADE` és `UNIQUE` megszorításokkal, majd az adatok betöltése
  (cx_Oracle).
- **Adatelemzés és vizualizáció:** automatikusan generált Excel-riport oszlop-, kör-
  és vonaldiagramokkal (hallgatói eloszlás, szakok népszerűsége, GPA-elemzés,
  beiratkozási trendek).

## Technológiák

- Python 3
- [Faker](https://faker.readthedocs.io/) – tesztadat-generálás
- [openpyxl](https://openpyxl.readthedocs.io/) – XLSX írás/olvasás és diagramok
- [cx_Oracle](https://oracle.github.io/python-cx_Oracle/) – Oracle-adatbázis kapcsolat
- [python-dotenv](https://pypi.org/project/python-dotenv/) *(opcionális)* – `.env` betöltése

## Projektstruktúra

```
data/
├── app.py                      # Belépési pont – a teljes folyamat vezérlése
├── basics/
│   ├── model_dataclasses.py    # Adatmodellek (University, Student, Course, Enrollment)
│   ├── handler.py              # CSV / JSON / XLSX handler-ek
│   └── handler/
│       └── oracle_handler.py   # Oracle kapcsolat és tábla kezelés
└── extra/
    └── analytics.py            # Elemzési riport diagramokkal
```

## Előfeltételek

- Python 3.10+
- (Az Oracle lépéshez) elérhető Oracle adatbázis és Oracle Instant Client

A függőségek telepítése:

```bash
pip install faker openpyxl cx_Oracle python-dotenv
```

## Futtatás

```bash
python data/app.py
```

## Kimenet

A program az `output/` mappába dolgozik:

```
output/
├── csv/        # universities, students, courses, enrollments (.csv)
├── json/       # ugyanezek JSON-ben
├── xlsx/       # data.xlsx – minden tábla külön munkalapon
└── analytics_report.xlsx   # diagramos elemzési riport
```
