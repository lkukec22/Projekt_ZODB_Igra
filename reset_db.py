import os
import shutil

def reset_database():
    db_path = 'data'
    if os.path.exists(db_path):
        print(f"Brisanje baze podataka u {db_path}...")
        try:
            # Brišemo cijeli data folder jer ZODB kreira više datoteka (.fs, .index, .lock, .tmp)
            shutil.rmtree(db_path)
            print("Baza uspješno obrisana.")
        except Exception as e:
            print(f"Greška pri brisanju: {e}")
            print("Provjerite je li igra zatvorena (ZODB zaključava datoteke dok su u upotrebi).")
    else:
        print("Baza podataka ne postoji, nema se što resetirati.")

    # Ponovno kreiranje praznog foldera
    os.makedirs(db_path, exist_ok=True)
    print("Spreman za novi početak. Pokrenite src/main.py za inicijalizaciju nove baze.")

if __name__ == "__main__":
    reset_database()
