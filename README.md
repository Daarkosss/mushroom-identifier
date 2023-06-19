# Mushroom identifier

Web app to recognize mushroom species from images.  
  
Features:
- user authentication (registration and login),
- uploading mushroom images for recognition,
- saving uploaded photos of mushrooms in the database,
- commenting on other people's mushrooms.

## How to run it?
Using the `environment.yml` file, create an environment with all necessary dependencies.  
Then in the main path (in the mushroom_identifier folder) run the application in the console:
```
python -m src.web_app.app
```

`-m` is necessary to run it as script due to relative imports.

## Mushroom species translations
| Latin                 | Polish              |
|-----------------------|---------------------|
| amanita muscaria      | muchomor czerwony   |
| amanita phalloides    | muchomor zielonawy  |
| armillaria mellea     | opieńka miodowa     |
| boletus edulis        | borowik szlachetny  |
| cantharellus cibarius | pieprznik jadalny   |
| imleria badia         | podgrzybek brunatny |
| leccinum scabrum      | koźlarz babka       |
| macrolepiota procera  | czubajka kania      |
| suillus luteus        | maślak zwyczajny    |
| tricholoma equestre   | gąska zielonka      |

## Citations:
1. Mushroom images
    - GBIF.org (4 June 2023) GBIF Occurrence Download https://doi.org/10.15468/dl.g7rqm9
    - GBIF.org (4 June 2023) GBIF Occurrence Download https://doi.org/10.15468/dl.bdhmbp
    - GBIF.org (4 June 2023) GBIF Occurrence Download https://doi.org/10.15468/dl.hh4ve2
    - GBIF.org (4 June 2023) GBIF Occurrence Download https://doi.org/10.15468/dl.drc23v
    - GBIF.org (4 June 2023) GBIF Occurrence Download https://doi.org/10.15468/dl.mvydp2
    - GBIF.org (4 June 2023) GBIF Occurrence Download https://doi.org/10.15468/dl.8mj8gb
    - GBIF.org (4 June 2023) GBIF Occurrence Download https://doi.org/10.15468/dl.ek7tbw
    - GBIF.org (4 June 2023) GBIF Occurrence Download https://doi.org/10.15468/dl.3ngtjf
    - GBIF.org (4 June 2023) GBIF Occurrence Download https://doi.org/10.15468/dl.srmh6x
    - GBIF.org (4 June 2023) GBIF Occurrence Download https://doi.org/10.15468/dl.uhnda7

2. Favicon
    - https://twemoji.twitter.com/