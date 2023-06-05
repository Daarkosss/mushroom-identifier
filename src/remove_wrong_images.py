import os
from PIL import Image

# Definiowanie ścieżek
base_dir = 'data/pre_images'

# Przechodzenie przez każdy folder (gatunek) w folderze bazowym
for folder in os.listdir(base_dir):
    current_dir = os.path.join(base_dir, folder)
    if os.path.isdir(current_dir):
        for image_name in os.listdir(current_dir):
            image_path = os.path.join(current_dir, image_name)
            try:
                img = Image.open(image_path)
                img.verify()  # Potwierdz, ze plik jest obrazem
            except (IOError, SyntaxError):
                print('Uszkodzony plik:', image_path)
                os.remove(image_path)
