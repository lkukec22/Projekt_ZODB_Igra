# 🎮 ZODB RPG Projekt

Jednostavna RPG igra razvijena sa **ZODB (Zope Object Database)** objektnom bazom podataka i **PyGame** frameworkom.

## 🚀 Značajke (ZODB Fokus)
- **Transparentna Perzistencija**: Automatsko spremanje cijelog grafa objekata (Igrač -> Inventar -> Predmeti).
- **BTrees (OOBTree)**: Korištenje B-stabala za efikasno pohranjivanje i dohvaćanje High Score tablice.
- **Triggeri (Okidači)**: Automatska promjena stanja objekta (npr. HP -> Status) putem Python property-ja.
- **Pohranjene procedure**: Kompleksna logika igre (npr. `use_item`, `take_damage`) smještena unutar samih perzistentnih klasa.
- **Upiti (Queries)**: Napredni upiti nad BTree strukturama za dohvaćanje top rezultata.

## 🛠️ Instalacija

### Automatski (preporučeno)
Pokrenite instalacijsku skriptu koja će postaviti virtualno okruženje i instalirati zavisnosti:
```bash
python setup.py
```
Ili koristite specifične skripte za vaš OS:
- **Windows**: `install.bat`
- **Linux/Mac**: `install.sh`

### Ručno
```bash
pip install -r requirements.txt
```

## 🎮 Kako igrati
Pokrenite igru naredbom:
```bash
python src/main.py
```
- **Tipke W / A / S / D**: Slobodno kretanje igrača (2D).
- **Lijevi klik miša**: Pucanje na neprijatelje.
- **Tipka R**: Restart igre nakon poraza.
- **Tipka X / Zatvori prozor**: Automatsko spremanje napretka i izlaz.

## 🧹 Resetiranje stanja
Ako želite obrisati sve podatke i krenuti ispočetka, pokrenite:
```bash
python reset_db.py
```
Ovo će obrisati mapu `data/` i sve spremljene igrače.

## 📂 Struktura projekta
- `src/main.py`: Glavna petlja igre i PyGame logika.
- `src/models.py`: Definicije perzistentnih objekata (`Player`, `Item`).
- `src/database.py`: Upravljanje ZODB vezom i inicijalizacija baze.
- `data/`: Mapa u kojoj se pohranjuju datoteke baze podataka.
- `setup.py`: Skripta za inicijalnu instalaciju.
- `reset_db.py`: Skripta za brisanje baze podataka.
- `requirements.txt`: Popis potrebnih Python paketa.
- `projekt_dokumentacija.tex`: LaTeX izvorna datoteka dokumentacije.

## 🎓 O projektu
Ovaj projekt je izrađen kao dio kolegija **Baze podataka**. Demonstrira prednosti objektnih baza podataka u razvoju igara, fokusirajući se na ACID svojstva, transakcije i transparentnu perzistenciju objekata.
