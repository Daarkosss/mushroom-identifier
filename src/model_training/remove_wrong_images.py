import os
from PIL import Image


def validate_image(image_path):
    try:
        img = Image.open(image_path)
        img.verify()
    except (IOError, SyntaxError):
        print('Uszkodzony plik:', image_path)
        os.remove(image_path)
        return False
    return True


if __name__ == '__main__':
    base_dir = 'data/pre_images'
    for folder in os.listdir(base_dir):
        current_dir = os.path.join(base_dir, folder)
        if os.path.isdir(current_dir):
            for image_name in os.listdir(current_dir):
                image_path = os.path.join(current_dir, image_name)
                validate_image(image_path)
