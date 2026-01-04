# 🎮 ZODB Top Down Survival Shooter Projekt

Jednostavna Top Down Survival Shooter igra razvijena sa **ZODB (Zope Object Database)** objektnom bazom podataka i **PyGame** frameworkom.

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
- **Kretanje**: Tipke **W / A / S / D**.
- **Pucanje**: **Lijevi klik miša** (ciljanje mišem).
- **Pauza / Izbornik**: Tipka **ESC** (automatski radi `commit` transakcije).
- **Restart**: Tipka **R** nakon poraza.
- **Cilj**: Preživite što duže protiv hordi neprijatelja (crveni krugovi) i skupljajte predmete (žuti kvadrati) za HP i bodove.

## 🧹 Resetiranje stanja
Ako želite obrisati sve podatke i krenuti ispočetka, pokrenite:
```bash
python reset_db.py
```
Ovo će obrisati mapu `data/` i sve spremljene igrače te rezultate.

## 📂 Struktura projekta
- `src/main.py`: Glavna petlja igre, upravljanje stanjima i PyGame logika.
- `src/models.py`: Definicije perzistentnih objekata (`Player`, `Enemy`, `Bullet`, `Item`).
- `src/database.py`: Upravljanje ZODB vezom, transakcijama i BTree upitima.
- `src/menu.py` & `src/ui.py`: Logika izbornika i UI komponenti (gumbi, input polja).
- `src/config.py`: Globalne konstante i postavke igre.
- `data/`: Mapa u kojoj se pohranjuju datoteke baze podataka (`game.fs`).
- `dokument/Rad.tex`: Detaljna projektna dokumentacija u LaTeX-u.

## 🎓 O projektu
Ovaj projekt je izrađen kao dio kolegija **Teorija baza podataka**. Demonstrira prednosti objektnih baza podataka (ZODB) u razvoju igara, fokusirajući se na:
- **ACID transakcije**: Osiguravanje integriteta podataka pri svakom spremanju.
- **Transparentna perzistencija**: Izbjegavanje *impedance mismatch* problema.
- **Napredne strukture**: Korištenje `OOBTree` za efikasno rangiranje rezultata.
- **Objektni okidači**: Implementacija poslovne logike kroz Python property settere.
