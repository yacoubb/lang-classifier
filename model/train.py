from tensorflow import keras
from sklearn.model_selection import train_test_split
import numpy as np
import sys
import os
import shutil


sys.path.append("/".join(os.path.abspath(__file__).split("/")[:-2]))
from model.dataset import utils

alphabet_size = len(utils.alphabet)


def train_and_save_model(model_path="", n=1000, langs=None):
    data, labels = utils.get_parsed_data(n, langs)
    x_train, x_valid, y_train, y_valid = train_test_split(
        data, labels, test_size=0.33, shuffle=True
    )
    print(x_train.shape, y_train.shape)

    model = keras.Sequential()
    model.add(keras.layers.Flatten(input_shape=(utils.max_word_length, alphabet_size)))
    model.add(keras.layers.Dense(128, activation="relu"))
    model.add(keras.layers.Dropout(0.2))
    model.add(keras.layers.Dense(64, activation="relu"))
    model.add(keras.layers.Dense(len(utils.languages), activation="softmax"))

    if model_path != None:
        model = keras.models.load_model(model_path)

    print(model.summary())

    # Configure a model for categorical classification.
    model.compile(
        # optimizer=tf.train.RMSPropOptimizer(0.01),
        # optimizer=keras.optimizers.RMSprop(lr=0.0005, rho=0.9, epsilon=None, decay=0.0),
        optimizer="adam",
        loss=keras.losses.categorical_crossentropy,
        metrics=[keras.metrics.categorical_accuracy],
    )

    reduce_lr = keras.callbacks.ReduceLROnPlateau(
        monitor="val_loss", factor=0.2, patience=3, min_lr=0.00001
    )

    early_stopping = keras.callbacks.EarlyStopping(monitor="val_loss", patience=5)

    model.fit(
        x_train,
        y_train,
        epochs=100,
        batch_size=1024,
        validation_data=(x_valid, y_valid),
        # callbacks=[reduce_lr, early_stopping],
        callbacks=[early_stopping],
    )

    if os.path.isdir("saved_model"):
        shutil.rmtree("saved_model")
    os.mkdir("saved_model")
    model.save("saved_model/model.h5")
    with open("saved_model/metadata.json", "w+") as metadata_file:
        metadata = {
            "maxWordLength": utils.max_word_length,
            "alphabet": utils.alphabet,
            "languages": utils.languages,
        }
        import json

        metadata_file.write(json.dumps(metadata, indent=4))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Train language classification algorithm."
    )
    parser.add_argument(
        "trainsamples",
        metavar="samplecount",
        type=int,
        help="number of training samples to use",
    )

    parser.add_argument(
        "-langs", nargs="*", help="(optional) languages to use", required=False
    )

    parser.add_argument(
        "-load", help="(optional) model path to load and train from", required=False
    )

    args = parser.parse_args()
    train_and_save_model(args.load, args.trainsamples, args.langs)

