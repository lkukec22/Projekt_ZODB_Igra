# Računalna igra (ZODB + PyGame)

## Upute za izradu projekta

Projekt se treba sastojati od aplikacije (implementacije) i odgovarajuće dokumentacije te treba pokazati da je student samostalno u stanju obuhvatiti proizvoljnu aplikacijsku domenu, odabrati odgovarajuću metodiku te implementirati aplikaciju koja je spremna za korištenje. Projekti se rade samostalno, rad u timu je isključen.

---

## Aplikacija

Aplikacija se treba sastojati od:
- **Implementacije modela baze podataka** u nekom od jezika/tehnologija prikazanih na laboratorijskim vježbama (Datalog, napredniji PostgreSQL, PostGIS, ZODB, eXist, MongoDB, Flora-2, Kafka, Neo4J)
- **Implementacije odgovarajućih komponenti** kao što su pogledi, upiti, predikati, okidači, pohranjene procedure, funkcije, metode i sl. u ovisnosti o odabranoj tehnologiji
- **Implementacije aplikacije s grafičkim sučeljem** koja će omogućiti korištenje baze podataka u proizvoljnom programskom jeziku

### Zahtjevi za predaju

1. **Verzioniranje**: Programski kod aplikacije treba postaviti na odgovarajući javni sustav za verzioniranje (npr. GitHub) pod otvorenom licencom (npr. GPL)
2. **Arhiva**: Aplikacija se predaje u obliku jedinstvene arhive sa svim datotekama potrebnim za izvođenje
3. **Instalacijska skripta**: Arhiva treba sadržavati instalacijsku skriptu koja će omogućiti automatiziranu kreiranje baze podataka i poveznicu na repozitorij sustava za verzioniranje

---

## Dokumentacija

Dokumentacija se treba sastojati od sljedećih dijelova (poglavlja):

### 1. Opis aplikacijske domene
- Jasno opisati domenu koju se želi implementirati
- Naznačiti koncepte, relacije, specifičnosti domene i sl.
- Dati motivaciju za korištenje odabrane tehnologije (zašto baš ta tehnologija, a ne neka druga)

### 2. Teorijski uvod
- Prikazati osnove pristupa bazama podataka koji se koristi pri implementaciji:
  - Aktivne, deduktivne, temporalne, poopćene, objektno-relacijske, objektno-orijentirane, polustrukturirane baze podataka
- Objasniti prednosti i nedostaci u odnosu na druge pristupe obzirom na aplikacijsku domenu

### 3. Model baze podataka
- Opisati model baze podataka
- Prikazati model u nekom od jezika za konceptualno modeliranje:
  - ERA (Entity-Relationship-Attribute)
  - UML (Unified Modeling Language)
  - ORM (Object-Role Modeling)

### 4. Implementacija
- Prikazati osnovne dijelove implementacije baze podataka
- Prikazati odgovarajuće dijelove aplikacije

### 5. Primjeri korištenja
- Prikazati nekoliko primjera korištenja aplikacije s bazom podataka
- Dodati odgovarajuće opise uz svaki primjer

### 6. Zaključak
- Procjena tehnologije kao platforme za implementaciju odabrane aplikacijske domene
- Ograničenja implementacije
- Moguća poboljšanja

### 7. Literatura
- Navesti koncizno i precizno sve korištene izvore
- Citirati sve izvore u tekstu

---

## Napomene za pisanje dokumentacije

> **Važno:** Prilikom pisanja dokumentacije valja obratiti pozornost na:
> - Izgled početne stranice
> - Citiranje izvora i literaturu
> - Numeriranje tablica, prikaza, slika i grafikona

### Format dokumentacije
- Projektnu dokumentaciju treba napisati korištenjem **LaTeX predloška**
- Preporučeno koristiti [Overleaf](https://www.overleaf.com/), no svi drugi sustavi dolaze u obzir
- Slijediti predložak i **Pravilnik o završnom i diplomskom radu**

### Citiranje
- Svaka referenca u literaturi mora biti citirana u tekstu
- Svaka korištena literatura mora biti u popisu literature
- Korišteni izvori trebaju biti referencirani **IEEE stilom**