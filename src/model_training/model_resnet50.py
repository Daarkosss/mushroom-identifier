# Imports needed
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras import Model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
import pathlib
import os
import json


def split_data(path_to_dataset):
    dataset_directory = pathlib.Path(path_to_dataset)

    image_count = len(list(dataset_directory.glob('*/*.jpg')))
    print(image_count)

    batch_size = 16
    img_height = 224
    img_width = 224

    train_ds = tf.keras.utils.image_dataset_from_directory(
        dataset_directory,
        labels='inferred',
        label_mode='int',
        validation_split=0.2,
        subset='training',
        seed=123,
        shuffle='True',
        image_size=(img_height, img_width),
        batch_size=batch_size)

    val_ds = tf.keras.utils.image_dataset_from_directory(
        dataset_directory,
        labels='inferred',
        label_mode='int',
        validation_split=0.2,
        subset='validation',
        seed=123,
        shuffle='True',
        image_size=(img_height, img_width),
        batch_size=batch_size)

    return train_ds, val_ds


def create_callbacks():
    checkpoint = ModelCheckpoint(
        'prediction_model/model_resnet50.h5',
        monitor='val_accuracy',
        verbose=1,
        save_best_only=True,
        save_weights_only=False,
        mode='auto',
        save_freq='epoch')

    early = EarlyStopping(
        monitor='val_accuracy',
        min_delta=0,
        patience=40,
        verbose=1,
        mode='auto')

    reduce_lr = ReduceLROnPlateau(
        monitor='val_accuracy',
        factor=0.1,
        mode='max',
        cooldown=2,
        patience=2,
        min_lr=0)

    return checkpoint, early, reduce_lr


def create_model_from_resnet(num_classes):
    resnet_model = ResNet50(weights='imagenet')

    last_layer = resnet_model.get_layer('avg_pool')
    resnet_layers = Model(
        inputs=resnet_model.inputs,
        outputs=last_layer.output)

    model = Sequential()
    model.add(resnet_layers)
    model.add(Dense(num_classes))

    model.layers[0].trainable = False

    return model


def get_class_names(path_to_dataset):
    class_names = os.listdir(path_to_dataset)
    class_names.sort()

    return class_names


def save_class_names_to_json(class_names):
    class_names_dict = {i: name for i, name in enumerate(class_names)}

    with open('prediction_model/class_names.json', 'wb') as f:
        json.dump(class_names_dict, f)


def train_model(path_to_dataset):
    tf.config.optimizer.set_jit(False)  # Turn off to avoid problems

    train_ds, val_ds = split_data(path_to_dataset)

    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

    class_names = get_class_names(path_to_dataset)
    save_class_names_to_json(class_names)

    model = create_model_from_resnet(len(class_names))
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
        loss=tf.keras.losses.SparseCategoricalCrossentropy(
            from_logits=True),
        metrics=['accuracy'])
    model.summary()

    checkpoint, early, reduce_lr = create_callbacks()
    epochs = 30
    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        callbacks=[checkpoint, early, reduce_lr])


if __name__ == '__main__':
    train_model('data/pre_images')
