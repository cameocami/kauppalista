# Suorituskyky suurella tietomäärällä

Sovellusta testattattiin suurella tietomäärällä. Suuri tietomäärä luotiin tiedostolla [seed.py](./src/seed.py), jossa

- käyttäjiä oli 1 000
- tuotteita oli 100 000
- jokaisella käyttäjällä oli 0 - 50 tuotetta kauppalistassaan
- tuotteiden lukumäärä kaupalistoilla vaihteli 1 ja 10 välillä
- tuotearvosteluita oli 1 000 000

## Ennen indeksointia
| Toiminto | URL                                              | Kulunut aika  | 
|--------|--------------------------------------------------|-----------|
| etusivu    | http://localhost:5000/                           |  0.06s   |
| avaa tuote    | http://localhost:5000/product/100000                    | 0.87s   |
| etsi "pro"   | http://localhost:5000/find_product?query=pro             | 0.15s   |
| etsi "moi"    | http://localhost:5000/find_product?query=moi       | 0.21s |
| lisää tuote kauppalistaan    | http://localhost:5000/adjust_amount      | 0.19s    |


## Indeksoinnin jälkeen

Tietokantaan lisättiin sitten indeksit:

```sql
CREATE INDEX idx_products_user_id ON products(user_id);
CREATE INDEX idx_products_unit_id ON products(unit_id);
CREATE INDEX idx_products_department_id ON products(department_id);
```
ja testidata alustettiin uudestaan. Samoja toimintoja testatiin uudestaan ja mitattiin kulunut aika. 

| Toiminto | URL                                              | Kulunut aika  | 
|--------|--------------------------------------------------|-----------|
| etusivu    | http://localhost:5000/                           |  0.01s   |
| avaa tuote    | http://localhost:5000/product/100000                    | 0.13s   |
| etsi "pro"   | http://localhost:5000/find_product?query=pro             | 0.03s   |
| etsi "moi"    | http://localhost:5000/find_product?query=moi        | 0.04s |
| lisää tuote kauppalistaan    | http://localhost:5000/adjust_amount      | 0.04s    |

Sivujen lataukseen kului nyt murto-osa aikasemmista ajoista. Latausajat olivat keskimäärin viisi kertaa nopeampia kuin ennen indeksointia. 