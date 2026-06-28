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
* Käyttäjäsivuilla näkyy käyttäjän kauppalista ja siihen liittyvät tilastot

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

## Toiminta suurella tietomäärällä

Sovellus toimii hyvin myös suurella tietomäärällä. Raportti aiheesta [täällä](performace_review.md).
