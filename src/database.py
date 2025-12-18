import ZODB, ZODB.FileStorage
import transaction
import os
from persistent.mapping import PersistentMapping

class GameDB:
    def __init__(self, db_path='data/game.fs'):
        try:
            # Osiguraj da folder postoji
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            
            self.storage = ZODB.FileStorage.FileStorage(db_path)
            self.db = ZODB.DB(self.storage)
            self.connection = self.db.open()
            self.root = self.connection.root()

            # Inicijalizacija korijenskih spremnika ako ne postoje
            if 'players' not in self.root:
                self.root['players'] = PersistentMapping() # Koristimo PersistentMapping za automatsko praćenje
            if 'world_state' not in self.root:
                self.root['world_state'] = PersistentMapping({'last_login': None})
        except Exception as e:
            print(f"Greška pri otvaranju baze: {e}")
            raise

    def save(self):
        transaction.commit()

    # --- UPIT (Query) ---
    def get_all_active_players(self):
        """Vraća sve igrače koji nisu poraženi"""
        return [p for p in self.root['players'].values() if p.status == "Aktivan"]

    def close(self):
        self.connection.close()
        self.db.close()