# Kauppalista

## Sovelluksen tämänhetkiset toiminnot

* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään tuotteita tietokantaan. Tuotteella on nimi, hinta, yksikkö ja osasto.
* Käyttäjä pystyy muokkaamaan ja poistamaan omaia tuotteitaan.
* Käyttäjä näkee sovellukseen lisätyt tuotteet.
* Käyttäjä pystyy etsimään tuotteita hakusanalla.
* Käyttäjä pystyy muokkaamaan omien tuotteidensa tietoja.
* Käyttäjä pystyy antamaan numeroarvion omien ja muiden tuotteista (toissijainen tietokohde).
* Tuotesivulla näkyy tuotteen tiedot sekä käyttäjäarvioiden keskiarvo.
* Käyttäjällä on oma kauppalista, johon hän pystyy lisäämään tuotteita. 
* Käyttäjä pystyy muokkaamaan tuotteiden määriä kauppalistallaan.
* Käyttäjä pystyy poistamaan tuotteita kauppalistaltaan.

## Sovellukseen tulevat toiminnot

* Käyttäjäsivuilla näkyy käyttäjän kauppalistan tilastoja
* Käyttäjäsivulla näkyy käyttäjän lisäämät tuotteet ja arviot.
* Käyttäjä pystyy tallentamaan ja avaamaan uuden kauppalistan.
* Käyttäjä näkee sovellukseen lisätyt kauppalistat.

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
