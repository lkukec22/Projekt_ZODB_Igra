# Prednosti ZODB-a u Razvoju Igara (vs. SQL)

Ovaj dokument opisuje ključne prednosti korištenja Objektno-Orijentirane Baze Podataka (ZODB) u odnosu na Relacijske Baze (SQL) na konkretnom primjeru naše igre.

## 1. Pohrana Kompleksnog Stanja Svijeta (World State Persistence)

### Scenarij
Želimo spremiti **točne pozicije svih neprijatelja i metaka** kada igrač izađe iz igre, kako bi nastavak igre bio identičan trenutku izlaska (onemogućavanje "bijega" od teške situacije).

### Implementacija u SQL-u (Relacijski Model)
Da bismo ovo postigli u SQL-u, morali bismo:
1.  Kreirati tablicu `Enemies` (id, player_id, x, y, hp, type...).
2.  Kreirati tablicu `Bullets` (id, player_id, x, y, dx, dy...).
3.  Prilikom spremanja (Save):
    *   Obrisati sve stare zapise za tog igrača.
    *   Iterirati kroz listu objekata i izvršiti `INSERT` za svaki objekt.
4.  Prilikom učitavanja (Load):
    *   Izvršiti `SELECT * FROM Enemies WHERE player_id = X`.
    *   Ručno re-kreirati Python objekte iz dobivenih redaka (Object-Relational Mapping).

**Rezultat:** Puno "boilerplate" koda, sporije izvođenje, gubitak konteksta objekata.

### Implementacija u ZODB-u (Objektni Model)
U našem projektu, implementacija je trivijalna jer ZODB sprema **graf objekata**.

```python
# U klasi Player
self.saved_enemies = PersistentList()

# Prilikom spremanja
player.saved_enemies = current_enemies_list 
transaction.commit()
```

To je sve! ZODB automatski:
1.  Prepoznaje da je `saved_enemies` dio `Player` objekta.
2.  Serijalizira svaki `Enemy` objekt unutar te liste (uključujući `x`, `y`, `hp` itd.).
3.  Sprema cijelu strukturu na disk.

## 2. Ključne Prednosti Demonstrirane u Projektu

1.  **Transparentnost**: Nismo pisali niti jedan upit (Query). Radimo s Python listama i objektima kao da su u memoriji, a baza radi "ispod haube".
2.  **Brzina Razvoja**: Dodavanje nove funkcionalnosti (spremanje metaka) zahtijevalo je samo dodavanje liste u klasu. Nije bilo potrebe za migracijom sheme baze (ALTER TABLE).
3.  **Performanse**: Učitavanje je trenutno jer ZODB ne mora raditi skupe `JOIN` operacije, već samo učita objekt s diska u RAM.

## Zaključak
Korištenje ZODB-a omogućilo nam je implementaciju naprednog "Save/Load" sustava s perzistencijom stotina dinamičkih objekata (metaka, neprijatelja) uz minimalan napor, što bi u SQL-u bio kompleksan zadatak.
