import os
from PIL import Image


image_dirs = ['data/train', 'data/validation']

for image_dir in image_dirs:
    for folder in os.listdir(image_dir):
        folder_path = os.path.join(image_dir, folder)
        for image_name in os.listdir(folder_path):
            image_path = os.path.join(folder_path, image_name)
            try:
                img = Image.open(image_path)
                img.verify()  # Potwierdź, plik jest obrazem
            except (IOError, SyntaxError):
                print('Uszkodzony plik:', image_path)
                os.remove(image_path)
