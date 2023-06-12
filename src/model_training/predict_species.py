import tensorflow as tf
from keras.models import load_model
import numpy as np
import pickle
import pathlib


def predict_mushroom_species(images_path):
    testing_files = list(images_path.glob('*.jpg'))

    for file in testing_files:
        img_width, img_height = 224, 224
        image = tf.keras.preprocessing.image.load_img(
            file,
            target_size=(img_height, img_width))

        image_array = tf.keras.utils.img_to_array(image)
        image_array = tf.expand_dims(image_array, 0)

        predictions = model.predict(image_array)
        score = tf.nn.softmax(predictions[0])

        print(f'The {file} most likely belongs to '
              f'{class_names[np.argmax(score)]} with a '
              f'{100 * np.max(score):.2f} percent confidence.')


if __name__ == '__main__':
    model = load_model('model/Model(ResNet50).h5')

    with open('prediction_models/class_names.pkl', 'rb') as file:
        class_names = pickle.load(file)

    images_path = pathlib.Path("data/test_images")
    predict_mushroom_species(images_path)
