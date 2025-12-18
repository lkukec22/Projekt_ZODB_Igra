# 🎮 KOMPLETAN VODIČ - ZODB + PYGAME IGRA

## 📋 PREGLED PROJEKTA

**Tema:** Razvoj računalne igre sa ZODB-om i PyGame-om  
**Obaveza:** Samostalna izrada  
**Dostava:** Aplikacija (GitHub) + LaTeX dokumentacija + Arhiva

---

## 📚 SAŽETAK ŠTO TREBATE NAUČITI

### 1. OBJEKTNO-ORIJENTIRANE BAZE PODATAKA (ZODB)

#### Što je ZODB?
- Baza koja pohrani **Python objekte** direktno
- Bez SQL-a - koristiš obični Python kod
- `transaction.commit()` = spremi sve promjene

#### ACID Svojstva
```
Atomarnost  → Sve ili ništa (ako padne, ništa se ne sprema)
Konzistentnost → Igrač nikad ne može imati -5 HP-a
Izolacija → Multiplayer igrači se ne miješaju
Trajnost → Spremi se trajno, nikad se ne gubi
```

#### Minimal Kod - ZODB

```python
from ZODB import FileStorage, DB
from persistent import Persistent
import transaction

# 1. Persistent klasa - može se pohraniti
class Player(Persistent):
    def __init__(self, name):
        self.name = name
        self.health = 100

# 2. Otvorite bazu
storage = FileStorage.FileStorage('igra.fs')
db = DB(storage)
connection = db.open()
root = connection.root()

# 3. Kreirajte i spremi
player = Player("Hero")
root['player'] = player
transaction.commit()  # ← VAŽNO!

# 4. Učitajte
loaded_player = root['player']
print(loaded_player.name)  # "Hero"

# 5. Zatvori
connection.close()
db.close()
```

---

### 2. PYGAME - IGRA S GRAFIKOM

#### Što je game loop?
```
┌─────────────────────────────┐
│    60 puta u sekundi        │
├─────────────────────────────┤
│ 1. Procesuiraj događaje     │
│ 2. Ažuriraj logiku          │
│ 3. Nacrtaj na ekran         │
│ ← Repeat                    │
└─────────────────────────────┘
```

#### Minimal Kod - PyGame

```python
import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
FPS = 60

running = True
while running:
    clock.tick(FPS)
    
    # 1. EVENTI
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # 2. UPDATE
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= 5
    
    # 3. DRAW
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (0, 255, 0), (player_x, 300, 40, 40))
    pygame.display.flip()

pygame.quit()
```

#### Sprite Klase

```python
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5

# Korištenje
all_sprites = pygame.sprite.Group()
player = Player(400, 300)
all_sprites.add(player)

# U game loop
all_sprites.update()
all_sprites.draw(screen)
```

---

### 3. INTEGRACIJA - ZODB + PYGAME

#### Spremi Igru

```python
def save_game(player_obj):
    root['player'] = player_obj
    root['player'].position = [player_sprite.rect.x, player_sprite.rect.y]
    transaction.commit()
    print("Igra je spremljena!")

# U igri
if event.key == pygame.K_s:
    save_game(player_data)
```

#### Učitaj Igru

```python
def load_game():
    if 'player' in root:
        player_obj = root['player']
        return player_obj
    return None

# Na početku
player_data = load_game()
if player_data:
    player_sprite.rect.x = player_data.position[0]
    player_sprite.rect.y = player_data.position[1]
```

---

## 🛠️ TEHNIČKI ZAHTJEVI

### Instalacija

```bash
# 1. Virtualna okruženja
python -m venv venv
source venv/bin/activate  # Linux/Mac

# 2. Instalacija paketa
pip install ZODB pygame transaction

# 3. Kreiraj main.py i pokrenite
python main.py
```

### requirements.txt

```
ZODB==6.0
pygame==2.1.2
transaction==3.0
```

---

## 📖 DOKUMENTACIJA - 6 POGLAVLJA

### 1. Opis Aplikacijske Domene
- Što je igra? (RPG, platformer, itd.)
- Likovi i entiteti
- Mehanike igre
- **Zašto ZODB?** - Motivacija za izbor

### 2. Teorijski Uvod
- Osnove OOBP
- Razlike od relacijskih BD
- ACID svojstva
- PyGame arhitektura
- Prednosti i nedostaci

### 3. Model Baze Podataka
- UML dijagram
- Klase i svojstva
- Relacije između objekata

### 4. Implementacija
- Inicijalizacija ZODB-a
- Persistent klase
- Game loop
- Sustav sprema/učitaj

### 5. Primjeri Korištenja
- Screenshots
- Opis što se dogodilo
- Podatci koji su spravljeni

### 6. Zaključak
- Procjena tehnologije
- Ograničenja
- Buduća proširenja
- Što ste naučili

---

## 📝 LATEX STRUKTURA

```latex
\documentclass[12pt,a4paper,croatian]{article}
\usepackage[utf8]{inputenc}
\usepackage[croatian]{babel}
\usepackage{graphicx}
\usepackage[square,numbers]{natbib}
\bibliographystyle{ieeetr}

\title{Računalna igra sa ZODB i PyGame}
\author{Ime Prezime}
\date{\today}

\begin{document}
\maketitle
\tableofcontents

\section{Opis Aplikacijske Domene}
% Tekst

\section{Teorijski Uvod}
% Tekst

% ... itd 6 poglavlja

\bibliography{literatura}
\end{document}
```

---

## 💾 DOSTAVA - ŠTA TREBATE

### 1. GitHub Repozitorij

```
github.com/vase_korisnicko_ime/igra-zodb-pygame

Datoteke:
├── main.py
├── requirements.txt
├── install.sh
├── install.bat
├── README.md
├── LICENSE (GPL)
└── dokumentacija.pdf
```

### 2. Instalacijska Skripta

**install.sh** (Linux/Mac):
```bash
#!/bin/bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

**install.bat** (Windows):
```batch
@echo off
python -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt
python main.py
```

### 3. Arhiva

```
igra_ZODB_PyGame.zip
├── main.py
├── requirements.txt
├── install.sh
├── install.bat
├── README.md
├── dokumentacija.pdf
├── projekt.tex
└── repository_link.txt
```

---

## ⏱️ VREMENSKA PROCJENA

| Faza | Vrijeme |
|------|---------|
| Setup & osnove | 5 sati |
| Pygame base | 8 sati |
| Mehanike igre | 10 sati |
| ZODB integracija | 8 sati |
| Testing & balansiranje | 5 sati |
| Dokumentacija | 10 sati |
| Instalacijska skripta | 2 sata |
| **UKUPNO** | **~50 sati** |

---

## 🎮 PRIMJER MINI IGRE

```python
import pygame
from ZODB import FileStorage, DB
from persistent import Persistent
import transaction

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Persistent klasa
class GamePlayer(Persistent):
    def __init__(self):
        self.health = 100
        self.score = 0
        self.position = [WIDTH//2, HEIGHT//2]

# Database
storage = FileStorage.FileStorage('game.fs')
db = DB(storage)
connection = db.open()
root = connection.root()

if 'player' not in root:
    root['player'] = GamePlayer()
    transaction.commit()

player_data = root['player']

# Game loop
running = True
clock_sprite_x = player_data.position[0]

while running:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.key == pygame.K_s:
            player_data.position = [clock_sprite_x, 300]
            transaction.commit()
            print("Spravljeno!")
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        clock_sprite_x -= 5
    if keys[pygame.K_RIGHT]:
        clock_sprite_x += 5
    
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (0, 255, 0), (clock_sprite_x, 300, 40, 40))
    pygame.display.flip()

connection.close()
db.close()
pygame.quit()
```

---

## ✅ CHECKLIST PRIJE PREDAJE

- [ ] `python main.py` radi bez greške
- [ ] Igra se može igrati do kraja
- [ ] Sprema i učitaj funkcionira
- [ ] GitHub repozitorij je kreiran
- [ ] `install.sh` i `install.bat` funkcioniraju
- [ ] LaTeX dokumentacija je gotova (6 poglavlja)
- [ ] PDF izgleda profesionalno
- [ ] IEEE stil citiranja je korišten
- [ ] Arhiva je kreirana
- [ ] Sve datoteke su u arhivi

---

## 🐛 ČESTA GREŠKA

### ❌ Zaboravili ste `transaction.commit()`

```python
❌ KRIVO:
player.health = 50
# Promjena se NE sprema!

✅ TOČNO:
player.health = 50
transaction.commit()
```

### ❌ Sprite nema `.rect`

```python
❌ KRIVO:
class Player(pygame.sprite.Sprite):
    def __init__(self):
        self.x = 100
        self.y = 100

✅ TOČNO:
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.rect = self.image.get_rect()
```

### ❌ Bez FPS ograničenja

```python
❌ KRIVO:
while running:
    # CPU zagrijava!

✅ TOČNO:
clock = pygame.time.Clock()
while running:
    clock.tick(60)  # Max 60 FPS
```

---

## 🚀 BRZI START

```bash
# 1. Setup
mkdir igra && cd igra
python -m venv venv
source venv/bin/activate
pip install ZODB pygame transaction

# 2. Kreirajte main.py (kopirajte primjer iznad)

# 3. Pokrenite
python main.py

# 4. Testirajte
# Strelice za pokretanje
# S za spremi
# Q za izlaz
```

---

## 📚 DODATNE REFERENCE

- **ZODB:** https://zodb.org
- **Pygame:** https://pygame.org/docs
- **Python:** https://docs.python.org/3
- **IEEE Citiranje:** Google "IEEE citation style"

---

## 💡 FINALNI SAVJETI

1. **Počnite jednostavno** - Mali projekt > veliki koji nije gotov
2. **Testirajte često** - Svaku novu funkcionalnost odmah
3. **Commit često** - `git commit` svakog sata
4. **Dokumentirajte tijekom razvoja** - Ne na kraju!
5. **Ne odustajte** - Sve greške su normalne

---

**SRETNO! 🎮✨**
