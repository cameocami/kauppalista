# Kauppalista

## Sovelluksen tämänhetkiset toiminnot

* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään tuotteita tietokantaan. 
* Käyttäjä pystyy muokkaamaan ja poistamaan tuotteita.
* Käyttäjä näkee sovellukseen lisätyt tuotteet.
* Käyttäjä pystyy etsimään tuotteita hakusanalla.

## Sovellukseen tulevat toiminnot

* Käyttäjä pystyy valitsemaan tuotteelle yhden tai useamman luokittelun (tuotteen osasto, esim. hevi, maitotuotteet, tuotteen yksikön esim. kg, litra, tölkki ja tuotteen hinnan).
* Käyttäjä pystyy luomaan kauppalistan tuotteista.
* Käyttäjä näkee sovellukseen lisätyt kauppalistat.
* Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja ja käyttäjän lisäämät kauppalistat.

## Sovelluksen asennus

Asenna `flask`-kirjasto:

```
$ pip install flask
```

Luo tietokannan taulut ja lisää alkutiedot:

```
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
```

Voit käynnistää sovelluksen näin:

```
$ flask run
```
