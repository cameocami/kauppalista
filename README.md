# Kauppalista

## Sovelluksen tämänhetkiset toiminnot

* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään tuotteita tietokantaan nimellä ja hinnalla.
* Käyttäjä pystyy muokkaamaan ja poistamaan tuotteita.
* Käyttäjä näkee sovellukseen lisätyt tuotteet.
* Käyttäjä pystyy etsimään tuotteita hakusanalla.
* Luodessaan uutta tuotetta käyttäjä pystyy valitsemaan tuotteelle osaston ja yksikön.

## Sovellukseen tulevat toiminnot

* Käyttäjä pystyy muokkaamaan tuotteen osastoa ja yksikköä.
* Käyttäjä pystyy luomaan kauppalistan tuotteista.
* Käyttäjä näkee sovellukseen lisätyt kauppalistat.
* Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja ja käyttäjän lisäämät kauppalistat.

## Sovelluksen asennus

Asenna `flask`-kirjasto:

```
$ pip install flask
```

Luo tietokannan taulut:

```
$ sqlite3 database.db < schema.sql
```

Voit käynnistää sovelluksen näin:

```
$ flask run
```
