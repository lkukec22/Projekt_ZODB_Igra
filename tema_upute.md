Računalna igra (ZODB + PyGame)

Upute za izradu projekta

Projekt se treba sastojati od aplikacije (implementacije) i odgovarajuće dokumentacije te treba pokazati da je student samostalno u stanju obuhvatiti proizvoljnu aplikacijsku domenu, odabrati odgovarajuću metodiku te implementirati aplikaciju koja je spremna za korištenje. Projekti se rade samostalno, rad u timu je isključen.
Aplikacija

Aplikacija se treba sastojati od implementacije modela baze podataka u nekom od jezika/tehnologija prikazanih na laboratorijskim vježbama (Datalog, napredniji PostgreSQL, PostGIS, ZODB, eXist, MongoDB, Flora-2, Kafka, Neo4J), implementacije odgovarajućih pogleda, upita, predikata, okidača, pohranjenih procedura, funkcija, metoda i sl. u ovisnosti o odabranoj tehnologiji, implementacije aplikacije s grafičkim sučeljem koja će omogućiti korištenje baze podataka u proizvoljnom programskom jeziku.

Programski kod aplikacije treba postaviti na odgovarajući javni sustav za verzioniranje (npr. GitHub) pod otvorenom licencom (npr. GPL).

Aplikacija se predaje u obliku jedinstvene arhive sa svim datotekama potrebnim za izvođenje te treba sadržavati instalacijsku skriptu koja će omogućiti automatiziranu kreiranje baze podataka i poveznicu na repozitorij sustava za verzioniranje.
Dokumentacija

Dokumentacija se treba sastojati od sljedećih dijelova (poglavlja):

    Opis aplikacijske domene - treba jasno opisati domenu koju se želi implementirati (naznačiti koncepte, relacije, specifičnosti domene i sl.) te dati motivaciju za korištenje odabrane tehnologije (zašto baš ta tehnologija, a ne neka druga).
    Teorijski uvod - prikazati osnove pristupa bazama podataka koji se koristi pri implementaciji (aktivne, deduktivne temporalne, poopćene, objektno-relacijske, objektno-orijentirane, polustrukturirane baze podataka) objasniti koje su njezine prednosti i nedostaci u odnosu na druge pristupe obzirom na aplikacijsku domenu.
    Model baze podataka - treba opisati model baze podataka i prikazati ga u nekom od jezika za konceptualno modeliranje (ERA, UML, ORM i sl.).
    Implementacija - prikazati osnovne dijelove implementacije baze podataka i odgovarajuće aplikacije.
    Primjeri korištenja - prikazati nekoliko primjera korištenja aplikacije s bazom podataka uz odgovarajuće opise.
    Zaključak - treba sadržavati procjenu tehnologije kao platforme za implementaciju odabrane aplikacijske domene, ograničenja implementacije i sl.
    Literatura - navesti koncizno i precizno sve korištene izvore i citirati ih u tekstu.

Prilikom pisanja dokumentacije valja obratiti pozornost na izgled početne stranice, citiranje izvora i literaturu, numeriranje tablica, prikaza, slika i grafikona itd. Projektnu dokumentaciju treba napisati korištenjem LaTeX predloška, prema predlošku i Pravilniku o završnom i diplomskom radu (preporuka je koristiti Overleaf, no svi drugi sustavi dolaze u obzir). Svaka referenca u literaturi mora biti citirana u tekstu i obrnuto, svaka korištena literatura mora biti u popisu literature. Korišteni izvori trebaju biti referencirani IEEE stilom.