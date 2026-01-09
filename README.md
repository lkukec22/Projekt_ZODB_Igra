# ZODB Top Down Survival Shooter Projekt

Jednostavna Top Down Survival Shooter igra razvijena sa **ZODB (Zope Object Database)** objektnom bazom podataka i **PyGame** frameworkom.

## Značajke (ZODB Fokus)
- **Transparentna Perzistencija**: Automatsko spremanje cijelog grafa objekata (Igrač -> Inventar -> Predmeti).
- **BTrees (OOBTree)**: Korištenje B-stabala za efikasno pohranjivanje i dohvaćanje High Score tablice.
- **Triggeri (Okidači)**: Automatska promjena stanja objekta implementirana kroz Python `@property` settere. Primjer:
  ```python
  @hp.setter
  def hp(self, value):
      self._hp = min(100, max(0, value))
      if self._hp == 0:
          self.status = "Defeated"  # Automatski okidač
      self._p_changed = True
  ```
- **Objektna Poslovna Logika**: Kompleksna logika igre (npr. `use_item()`, `take_damage()`, `add_score()`) implementirana kao metode perzistentnih objekata - prava objektna paradigma bez SQL.
- **Upiti (Queries)**: Napredni upiti nad BTree strukturama za efikasno dohvaćanje i rangiranje top rezultata.
- **Dinamički Difficulty**: Težina igre se povećava s vremenom preživljavanja (1.0x + vrijeme/60s), utječući na brzinu neprijatelja i spawn rate.

## Instalacija

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

## Kako igrati
Pokrenite igru naredbom:
```bash
python src/main.py
```
- **Kretanje**: Tipke **W / A / S / D**.
- **Pucanje**: **Lijevi klik miša** (ciljanje mišem).
- **Pauza / Izbornik**: Tipka **ESC** (automatski radi `commit` transakcije).
- **Restart**: Tipka **R** nakon poraza.
- **Cilj**: Preživite što duže protiv hordi neprijatelja (crveni krugovi) i skupljajte predmete (žuti kvadrati) za HP i bodove.
- **Napredak Težine**: Što duže igrate, brže se pojavljuju jači neprijatelji. Težina se izračunava kao `1.0 + (vrijeme_preživljavanja / 60s)`.

## Resetiranje stanja
Ako želite obrisati sve podatke i krenuti ispočetka, pokrenite:
```bash
python reset_db.py
```
Ovo će obrisati mapu `data/` i sve spremljene igrače te rezultate.

## Struktura projekta
- `src/main.py`: Glavna petlja igre (Game Loop), upravljanje stanjima (MENU, GAME, COUNTDOWN, GAMEOVER, LEADERBOARD, LOAD_GAME) i PyGame logika.
- `src/models.py`: Definicije perzistentnih objekata (`Player`, `Enemy`, `Bullet`, `Item`) s ugrađenom poslovnom logikom.
- `src/database.py`: `GameDB` klasa - upravljanje ZODB vezom, transakcijama, BTree upitima i high score tablicama.
- `src/menu.py`: Logika izbornika - New Game, Load Game, Leaderboard, Exit.
- `src/ui.py`: UI komponente (Button, TextField) za interaktivne elemente.
- `src/config.py`: Globalne konstante (WIDTH, HEIGHT, FPS, boje).
- `data/`: Mapa u kojoj se pohranjuju datoteke baze podataka (`game.fs`, `game.fs.index`).
- `dokument/Rad.tex`: Detaljna projektna dokumentacija u LaTeX-u s UML dijagramima i teorijskim okvirom.

## O projektu
Ovaj projekt je izrađen kao dio kolegija **Teorija baza podataka**. Demonstrira prednosti objektnih baza podataka (ZODB) u razvoju igara, fokusirajući se na:
- **ACID transakcije**: Osiguravanje integriteta podataka pri svakom spremanju (`transaction.commit()`).
- **Transparentna perzistencija**: Izbjegavanje *impedance mismatch* problema - Python objekti se direktno spremaju bez ORM sloja.
- **Napredne strukture**: Korištenje `OOBTree` za efikasno rangiranje rezultata, `PersistentList` za dinamičke kolekcije.
- **Objektni okidači**: Implementacija poslovne logike kroz Python `@property` settere koji automatski reagiraju na promjene (npr. HP=0 → Status="Defeated").
- **Graf objekata**: ZODB čuva cijeli graf - Player → PersistentList(Enemies, Bullets, Items) - omogućujući Save/Load funkcionalnost stotina objekata istovremeno.

**Za detaljnu tehničku dokumentaciju, UML dijagrame i teorijsku pozadinu, pogledajte `dokument/Rad.pdf`.**
