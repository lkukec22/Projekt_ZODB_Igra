import ZODB, ZODB.FileStorage
import transaction
import os
from persistent.mapping import PersistentMapping
from BTrees.OOBTree import OOBTree # type: ignore # Object-Object BTree za efikasne upite

class GameDB:
    def __init__(self, db_path='data/game.fs'):
        try:
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            
            self.storage = ZODB.FileStorage.FileStorage(db_path)
            self.db = ZODB.DB(self.storage)
            self.connection = self.db.open()
            self.root = self.connection.root()

            if 'players' not in self.root:
                self.root['players'] = PersistentMapping()
            
            # --- NAPREDNA STRUKTURA: BTree za High Scores ---
            if 'high_scores' not in self.root:
                self.root['high_scores'] = OOBTree() 
                
            if 'world_state' not in self.root:
                self.root['world_state'] = PersistentMapping({'last_login': None})
        except Exception as e:
            print(f"Greska pri otvaranju baze: {e}")
            raise

    def save(self):
        transaction.commit()

    # --- NAPREDNI UPIT (BTree Range Query) ---
    def get_top_scores(self, limit=5):
        """Vraca top rezultate koristeci BTree efikasnost"""
        # OOBTree je sortiran po kljucu. Za top scores koristimo (score, name) kao kljuc
        # ili jednostavno sortiramo, ali BTree nam omogucuje brze range upite.
        scores = list(self.root['high_scores'].items())
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:limit]

    def add_high_score(self, name, score):
        self.root['high_scores'][name] = max(self.root['high_scores'].get(name, 0), score)
        self.save()

    # --- UPIT (Query) ---
    def get_all_active_players(self):
        """Vraca sve igrace koji nisu porazeni"""
        return [p for p in self.root['players'].values() if p.status == "Aktivan"]

    def close(self):
        transaction.abort() # Osiguraj da nema aktivnih transakcija prije zatvaranja
        self.connection.close()
        self.db.close()