from tensorflow.keras.utils import img_to_array, load_img
from keras.models import load_model
import numpy as np
import pickle


def predict_mushroom_species(image_path):
    # Załaduj i przetwórz obraz
    img_width, img_height = 200, 200
    image = load_img(image_path, target_size=(img_width, img_height))
    image = img_to_array(image)
    image = image / 255.0
    image = np.expand_dims(image, axis=0)

    # Użyj modelu do przewidywania
    predictions = model.predict(image)

    # Wypisz gatunek grzyba
    for i in range(len(class_names)):
        class_name = class_names[i]
        probability = predictions[0][i]
        print(f'{class_name}, prawdopodobieństwo: {probability:.2f}')


if __name__ == '__main__':
    # Wczytanie modelu
    model = load_model('model/model.h5')

    # Wczytanie słownika z mapowaniem nazw klas
    with open('model/class_names.pkl', 'rb') as file:
        class_names = pickle.load(file)

    predict_mushroom_species('data/test_images/muchomor.jpg')
