import pandas as pd
import requests
import os
from .remove_wrong_images import validate_image


def download_image(species, row, index):
    url = row['identifier']
    if pd.notna(url):
        try:
            response = requests.get(url, timeout=5)
            image_path = f'data/pre_images/{species}/image_{index}.jpg'
            with open(image_path, 'wb') as f:
                f.write(response.content)
                if validate_image(image_path):
                    index += 1
        except requests.exceptions.RequestException as err:
            print(f"Error while downloading image from {url}: {err}")
        finally:
            return index


if __name__ == '__main__':
    mushroom_species = 'tricholoma_equestre'
    df = pd.read_csv(
        f'data/image_links/{mushroom_species}.txt',
        delimiter='\t')

    if not os.path.exists(f'data/pre_images/{mushroom_species}'):
        os.makedirs(f'data/pre_images/{mushroom_species}')

    index = 1
    for _, row in df.iterrows():
        index = download_image(mushroom_species, row, index)

    print("Downloading finished")
