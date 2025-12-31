from persistent import Persistent
from persistent.list import PersistentList

class Item(Persistent):
    def __init__(self, name, power):
        self.name = name
        self.power = power

class Player(Persistent):
    def __init__(self, name):
        self.name = name
        self._hp = 100
        self.x = 400
        self.y = 300
        self.score = 0
        self.inventory = PersistentList()
        self.status = "Aktivan"

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        # Ograniči kretanje unutar ekrana (800x600)
        self.x = max(0, min(self.x, 760))
        self.y = max(0, min(self.y, 560))
        self._p_changed = True

    def reset(self):
        self._hp = 100
        self.x = 400
        self.y = 300
        self.score = 0
        self.status = "Aktivan"
        self._p_changed = True

    # --- POHRANJENA PROCEDURA (Logika unutar objekta) ---
    def take_damage(self, amount):
        self.hp -= amount # Koristimo setter za trigger

    def add_score(self, points):
        self.score += points
        self._p_changed = True

    # --- OKIDAČ (TRIGGER) putem property-ja ---
    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = max(0, value)
        # OKIDAČ: Ako je HP 0, promijeni status u "Poražen"
        if self._hp == 0:
            self.status = "Poražen"
        self._p_changed = True # Javljamo ZODB-u da spremi promjenu