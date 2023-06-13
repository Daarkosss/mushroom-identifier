import tensorflow as tf
from keras.models import load_model
import numpy as np
import pickle
import pathlib


def predict_mushroom_species(file):
    model = load_model('prediction_models/Model(ResNet50).h5')
    with open('prediction_models/class_names.pkl', 'rb') as class_names_file:
        class_names = pickle.load(class_names_file)

    img_width, img_height = 224, 224
    image = tf.keras.preprocessing.image.load_img(
        file,
        target_size=(img_height, img_width))

    image_array = tf.keras.utils.img_to_array(image)
    image_array = tf.expand_dims(image_array, 0)

    predictions = model.predict(image_array)
    score = tf.nn.softmax(predictions[0])

    species, odds = class_names[np.argmax(score)], np.max(score) * 100
    return species, odds


def predict_mushroom_species_from_dir(images_path):
    testing_files = list(images_path.glob('*.jpg'))

    for file in testing_files:
        species, odds = predict_mushroom_species(file)
        print_mushroom_species(file, species, odds)


def print_mushroom_species(file, species, odds):
    print(f'The {file} most likely belongs to '
          f'{species} with a '
          f'{100 * odds:.2f} percent confidence.')


if __name__ == '__main__':
    images_path = pathlib.Path("data/test_images")
    predict_mushroom_species_from_dir(images_path)
