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
echo "  python src/main.py"
