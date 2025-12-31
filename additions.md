add so the user can choose a name
make the enemy drops have a score multiplier like every drop is 0.1x multi and it adds up
need control keybinds displayed on screen
make the screen a bit bigger

### Dodatne ideje za proširenje projekta:
- **Persistent World State**: Spremanje pozicija neprijatelja i metaka u ZODB tako da se igra može nastaviti točno gdje je stala.
- **Sustav Postignuća (Achievements)**: Korištenje `OOBTree` za praćenje prekretnica (npr. "Prvih 1000 bodova", "10 skupljenih predmeta").
- **Score Multiplier Logika**: Implementacija `multiplier` polja u `Player` modelu koji se povećava sa svakim skupljenim predmetom.
- **Transactional "Undo"**: Korištenje `transaction.abort()` za implementaciju "života" - vraćanje na zadnji commit umjesto Game Over-a.
- **Napredni UI**: Prikaz kontrola na ekranu i vizualni indikator trenutnog množitelja bodova.
- **Više igrača**: Name selection ekran koji omogućuje različitim korisnicima da imaju svoje odvojene perzistentne objekte u istoj bazi.