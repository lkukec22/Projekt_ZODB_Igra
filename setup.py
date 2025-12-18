import os
import subprocess
import sys

def setup():
    print("--- Pokretanje instalacije projekta ---")
    
    # 1. Instalacija paketa
    subprocess.check_call([sys.executable, "-m", "pip", "install", "zodb", "pygame", "persistent"])
    
    # 2. Kreiranje baze podataka
    if not os.path.exists('data'):
        os.makedirs('data')
        print("Kreiran direktorij za bazu podataka.")
    
    print("\nInstalacija uspješna. Pokrenite igru sa: python src/main.py")

if __name__ == "__main__":
    setup()