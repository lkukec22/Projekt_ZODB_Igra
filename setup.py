import os
import subprocess
import sys

def setup():

    # 1. Instalacija paketa iz requirements.txt
    print("\n[1/3] Instaliram potrebne pakete...")
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])
    
    # 2. Kreiranje data direktorija
    print("\n[2/3] Pripremam direktorij za bazu podataka...")
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print("  -> Kreiran direktorij 'data/'")
    else:
        print("  -> Direktorij 'data/' već postoji")
    
    print("\n[3/3] Pokrećem igru...")
    
    # 3. Pokretanje igre
    main_path = os.path.join(os.path.dirname(__file__), 'src', 'main.py')
    subprocess.call([sys.executable, main_path])

if __name__ == "__main__":
    setup()