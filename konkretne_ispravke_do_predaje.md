# 🔧 KONKRETNE ISPRAVKE - KOD KOJI TREBATE DODATI

## 1. ✅ **database.py** - Dodajte `import transaction`

### TRENUTNO (nepotpuno):
```python
import ZODB, ZODB.FileStorage
import os
from persistent.mapping import PersistentMapping
```

### TREBAM (dodajte):
```python
import ZODB, ZODB.FileStorage
import transaction  # ← DODAJTE OVO!
import os
from persistent.mapping import PersistentMapping
```

---

## 2. ✅ **requirements.txt** - Kreirajte novu datoteku

Sadržaj:
```
ZODB==6.0
pygame==2.1.2
persistent==4.9.0
BTrees==4.10.1
transaction==3.0
```

**Kako kreirajte:**
```bash
# 1. Manualno kreirajte datoteku "requirements.txt"
# 2. Kopirajte sadržaj iznad

# Ili, ako ste već instalirali pakete:
pip freeze > requirements.txt
```

---

## 3. ✅ **README.md** - Kreirajte novu datoteku

```markdown
# ZODB RPG Projekt

Jednostavna RPG igra razvijena sa ZODB objektnom bazom podataka i PyGame frameworkom.

## Instalacija

### Automatski (preporučeno)
```bash
python setup.py
```

### Manualnim
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ili
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

## Pokretanje Igre

```bash
python main.py
```

## Kontrole

| Tipka | Akcija |
|-------|--------|
| A | Pomjeranje lijevo |
| D | Pomjeranje desno |
| SPACE | Primanje 20 štete |
| X | Spremi i izađi |

## Resetiranje Baze Podataka

Ako trebate obrisati sve podatke i početi iznova:

```bash
python reset_db.py
```

## Struktura Projekta

```
zodb-rpg-projekt/
├── main.py              # Glavna igra
├── models.py            # Player i Item klase
├── database.py          # GameDB klasa
├── setup.py             # Instalacijska skripta
├── reset_db.py          # Reset baze
├── requirements.txt     # Zavisnosti
├── README.md            # Ova datoteka
├── projekt_dokumentacija.tex  # LaTeX dokumentacija
└── data/                # ZODB datoteke (automatski kreirano)
```

## Kako Funkcionira

1. Igra koristi **ZODB** za pohranjevanje igrača u `data/game.fs`
2. Svaka promjena igrača (HP, pozicija) se automatski prati
3. Pritiskom X ili zatvaranjem igre, sve se sprema
4. Pri sljedećem pokretanju, igrač se učitava sa zadnjim vrijednostima

## Primjer Gameplay-a

```
1. Pokrenite igru: python main.py
2. Vidite zeleni kvadrat (igrač) na sredini ekrana
3. Premjestite se s A/D
4. Pritisnite SPACE - primite 20 štete (vidite HP se smanjuje)
5. Nakon 5 puta SPACE - igrač je poražen (kvadrat postaje crven)
6. Pritisnite X - igra se sprema i zatvara
7. Pokrenite ponovno - igrač je na istoj poziciji s istim HP!
```

## Zahtjeve

- Python 3.8+
- ZODB
- pygame
- persistent

## Licence

GPL v3

## Autor

[Vaše ime]

## Projekt za Kolegij

Projekt iz Baza Podataka - Fakultet Elektrotehnike i Računarstva
```

---

## 4. ✅ **.gitignore** - Kreirajte novu datoteku

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# ZODB baze
data/game.fs*
data/game.fs.lock
data/game.fs.tmp

# Lokalni test datoteke
test_*.py
*.log
```

---

## 5. ✅ **install.sh** (Linux/Mac) - Kreirajte novu datoteku

```bash
#!/bin/bash

echo "=== Instalacija ZODB RPG Projekta ==="

# 1. Virtualna okruženja
echo "Kreiram virtualnu okruženja..."
python3 -m venv venv

# 2. Aktivacija
echo "Aktiviram virtualna okruženja..."
source venv/bin/activate

# 3. Instalacija paketa
echo "Instaliram pakete..."
pip install -r requirements.txt

echo ""
echo "✓ Instalacija je uspješna!"
echo ""
echo "Za pokretanje igre, izvršite:"
echo "  source venv/bin/activate"
echo "  python main.py"
```

**Kako koristiti:**
```bash
chmod +x install.sh
./install.sh
```

---

## 6. ✅ **install.bat** (Windows) - Kreirajte novu datoteku

```batch
@echo off

echo === Instalacija ZODB RPG Projekta ===

REM 1. Virtualna okruženja
echo Kreiram virtualnu okruženja...
python -m venv venv

REM 2. Aktivacija
echo Aktiviram virtualnu okruženja...
call venv\Scripts\activate.bat

REM 3. Instalacija paketa
echo Instaliram pakete...
pip install -r requirements.txt

echo.
echo Instalacija je uspjesna!
echo.
echo Za pokretanje igre, izvrsit ce:
echo   venv\Scripts\activate.bat
echo   python main.py

pause
```

**Kako koristiti:**
```batch
install.bat
```

---

## 7. ✅ **Spakujte Sve Za Dostavu**

### Struktura Finalne Arhive

```
zodb_rpg_projekt.zip
│
├── main.py
├── models.py
├── database.py
├── setup.py
├── reset_db.py
│
├── requirements.txt
├── README.md
├── .gitignore
├── install.sh
├── install.bat
│
├── projekt_dokumentacija.tex
├── projekt_dokumentacija.pdf  (generirano iz .tex)
│
└── repository_link.txt  (link na GitHub)
```

### Kako Kreirajte Arhivu

**Linux/Mac:**
```bash
zip -r zodb_rpg_projekt.zip \
    main.py models.py database.py \
    setup.py reset_db.py \
    requirements.txt README.md .gitignore \
    install.sh install.bat \
    projekt_dokumentacija.tex projekt_dokumentacija.pdf \
    repository_link.txt
```

**Windows (koristite Explorer):**
1. Selektirajte sve datoteke
2. Desni klik → Send to → Compressed (zipped) folder
3. Imenujte `zodb_rpg_projekt.zip`

---

## 8. ✅ **repository_link.txt** - Kreirajte novu datoteku

```
GitHub Repozitorij
==================

Link: https://github.com/vase_korisnicko_ime/zodb-rpg

Instrukcije za kloniranje:
git clone https://github.com/vase_korisnicko_ime/zodb-rpg.git
```

---

## ✅ FINALNI CHECKLIST - PRIJE PREDAJE

### Datoteke (trebam provjeriti)
- [x] main.py (već imate)
- [x] models.py (već imate)
- [ ] database.py **+ `import transaction`** ← Dodajte import
- [x] setup.py (već imate)
- [x] reset_db.py (već imate)
- [ ] requirements.txt ← **KREIRAJTE**
- [ ] README.md ← **KREIRAJTE**
- [ ] .gitignore ← **KREIRAJTE**
- [ ] install.sh ← **KREIRAJTE**
- [ ] install.bat ← **KREIRAJTE**
- [ ] projekt_dokumentacija.tex ← **Već kreiran (artifact: 59)**
- [ ] projekt_dokumentacija.pdf ← **Trebam generirati (pdflatex)**

### GitHub
- [ ] Kreirajte repozitorij
- [ ] `git init` i `git add .`
- [ ] `git commit -m "Initial commit - ZODB RPG"`
- [ ] `git push`
- [ ] [ ] Kreirajte `repository_link.txt`

### Testiranje
- [ ] `python setup.py` - radi bez greške
- [ ] `python main.py` - igra se pokreće
- [ ] A/D - pokretanje radi
- [ ] SPACE - damage radi
- [ ] X - sprema radi
- [ ] `python reset_db.py` - reset radi
- [ ] Arhiva se raspakuje ispravno

---

## 🎯 REDOSLIJED AKCIJA

### KORAK 1: Ispravke (5 minuta)
1. Dodajte `import transaction` u database.py

### KORAK 2: Nove Datoteke (10 minuta)
1. Kreirajte requirements.txt
2. Kreirajte README.md
3. Kreirajte .gitignore
4. Kreirajte install.sh
5. Kreirajte install.bat
6. Kreirajte repository_link.txt

### KORAK 3: GitHub (5 minuta)
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/vase_korisnicko_ime/zodb-rpg.git
git push -u origin main
```

### KORAK 4: LaTeX (5 minuta)
- Generirajte PDF:
```bash
pdflatex projekt_dokumentacija.tex
# Ili koristite Overleaf
```

### KORAK 5: Arhiva (2 minute)
- Spakujte sve datoteke u `zodb_rpg_projekt.zip`

### KORAK 6: Testiranje (10 minuta)
- Testirajte da sve radi

---

## 📝 NAPOMENA

Svi primjeri koda iznad su **gotovi za kopirati-paste**. Samo zamijenite:
- `vase_korisnicko_ime` → Vaše GitHub korisničko ime
- `Ime Prezime` → Vaše ime
- `12345678` → Vaš matični broj

**Ukupno vremena:** ~30 minuta za sve! 🚀
