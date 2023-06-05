import pandas as pd
import requests
import os

# Wczytaj plik .txt jako ramkę danych pandas
mushroom_species = 'macrolepiota_procera'
df = pd.read_csv(f'data/image_links/{mushroom_species}.txt', delimiter='\t')

# Stwórz folder na zdjęcia, jeśli nie istnieje
if not os.path.exists(f'data/pre_images/{mushroom_species}'):
    os.makedirs(f'data/pre_images/{mushroom_species}')

# Przejrzyj kolumnę 'identifier' w poszukiwaniu linków do zdjęć
index = 1
for _, row in df.iterrows():
    url = row['identifier']
    if pd.notna(url):
        try:
            response = requests.get(url)
            with open(
                f'data/pre_images/{mushroom_species}/image_{index}.jpg',
                'wb'
            ) as f:
                f.write(response.content)
                index += 1
        except requests.exceptions.RequestException as err:
            print(f"Blad pobierania obrazu z {url}: {err}")

print("Pobieranie zakończone")
