# Kauppalista

## Sovelluksen tämänhetkiset toiminnot

* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään tuotteita tietokantaan nimellä ja hinnalla.
* Käyttäjä pystyy muokkaamaan ja poistamaan tuotteita.
* Käyttäjä näkee sovellukseen lisätyt tuotteet.
* Käyttäjä pystyy etsimään tuotteita hakusanalla.
* Luodessaan uutta tuotetta käyttäjä pystyy valitsemaan tuotteelle osaston ja yksikön.
* Käyttäjä pystyy muokkaamaan tuotteen osastoa ja yksikköä.
* Käyttäjällä on kauppalista, johon hän pystyy lisäämään tuotteita. 
* Käyttäjä pystyy muokkaamaan tuotteen määrää kauppalistallaan.
* Käyttäjä pystyy poistamaan tuotteita kauppalistaltaan.

## Sovellukseen tulevat toiminnot

* Käyttäjä näkee kunkin tuotteen kohdalla kenen kauppalistoilla tuote on.
* Käyttäjä pystyy tallentamaan ja avaamaan uuden kauppalistan.
* Käyttäjä näkee sovellukseen lisätyt kauppalistat.
* Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja ja käyttäjän lisäämät kauppalistat ja tuotteet.

## Sovelluksen asennus

Asenna `flask`-kirjasto:

```
$ pip install flask
```

Luo tietokannan taulut:

```
$ sqlite3 database.db < schema.sql

```
Alusta tietokannan tiedot:
```
$ sqlite3 database.db < init.sql
```

Käynnistä sovellus komennolla:

```
$ flask run
```
