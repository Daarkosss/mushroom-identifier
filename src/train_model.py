from keras.models import Model
from keras.layers import Conv2D, MaxPooling2D, BatchNormalization
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping
from keras.applications.vgg16 import VGG16
import pickle

train_data_dir = 'data/train'
validation_data_dir = 'data/validation'
nb_train_samples = 9000  # Zmień na faktyczną liczbę obrazów treningowych
nb_validation_samples = 2000  # Zmień na faktyczną liczbę obrazów walidacyjnych
epochs = 50
batch_size = 32
num_classes = 10  # Liczba gatunków grzybów
img_width, img_height = 150, 150
input_shape = (img_width, img_height, 3)

# Ładowanie modelu VGG16 z wytrenowanymi wagami z ImageNet, bez ostatniej warstwy (top)
base_model = VGG16(
    weights='imagenet',
    include_top=False,
    input_shape=input_shape)

# Dodanie nowych warstw na końcu modelu
x = base_model.output
x = Flatten()(x)
x = Dense(256, activation='relu')(x)  # Można dodać dodatkowe warstwy, jeśli to konieczne
x = Dropout(0.5)(x)
predictions = Dense(num_classes, activation='softmax')(x)

# Nowy model
model = Model(inputs=base_model.input, outputs=predictions)

# Możemy zamrozić warstwy bazowego modelu (opcjonalne)
for layer in base_model.layers:
    layer.trainable = False

# Kompilacja modelu
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])


# Reszta kodu (trenowanie, walidacja) pozostaje taka sama

early_stopping = EarlyStopping(monitor='val_loss', patience=5)

train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1. / 255)

train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical')

validation_generator = test_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical')

model.fit(
    train_generator,
    steps_per_epoch=nb_train_samples // batch_size,
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps=nb_validation_samples // batch_size,
    callbacks=[early_stopping])

class_names = train_generator.class_indices
class_names = {v: k for k, v in class_names.items()}

with open('model/class_names_pre.pkl', 'wb') as file:
    pickle.dump(class_names, file)

model.save('model/model_pre_trained.h5')
