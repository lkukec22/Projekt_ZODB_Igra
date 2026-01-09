import ZODB, ZODB.FileStorage
import transaction
import os
import time
from persistent.mapping import PersistentMapping
from BTrees.OOBTree import OOBTree

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class GameDB:
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = os.path.join(BASE_DIR, 'data', 'game.fs')
        
        if not os.path.dirname(db_path):
            db_path = os.path.join('.', db_path)
        
        try:
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            self.storage = ZODB.FileStorage.FileStorage(db_path)
            self.db = ZODB.DB(self.storage)
            self.connection = self.db.open()
            self.root = self.connection.root()

            if 'players' not in self.root:
                self.root['players'] = PersistentMapping()
            
            if 'high_scores' not in self.root:
                self.root['high_scores'] = OOBTree()
            elif not isinstance(self.root['high_scores'], OOBTree):
                old_scores = self.root['high_scores']
                new_scores = OOBTree()
                for key, value in old_scores.items():
                    new_scores[key] = value
                self.root['high_scores'] = new_scores
                transaction.commit()
            
            if 'world_state' not in self.root:
                self.root['world_state'] = PersistentMapping({'last_login': None})
        except Exception as e:
            print(f"Error opening database: {e}")
            raise

    def save(self):
        transaction.commit()

    def pack(self, days=0):
        try:
            self.db.pack(time.time() - days * 86400)
        except Exception as e:
            print(f"Error packing DB: {e}")

    def get_top_scores(self, limit=5):
        items = list(self.root['high_scores'].items())
        items.sort(key=lambda x: x[1][0], reverse=True)
        return [(name, val[0], val[1]) for name, val in items[:limit]]

    def add_high_score(self, name, score, time_survived):
        current_entry = self.root['high_scores'].get(name)
        current_score = current_entry[0] if current_entry else 0
        if score > current_score:
            self.root['high_scores'][name] = (score, time_survived)
            self.save()

    def get_all_active_players(self):
        players = [p for p in self.root['players'].values() if p.status == "Active"]
        players.sort(key=lambda x: x.name)
        return players

    def close(self):
        transaction.abort()
        self.connection.close()
        self.db.close()