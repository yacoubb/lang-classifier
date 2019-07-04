import tensorflow as tf
from tf import keras
from tf.keras import layers
from tf.keras.models import load_model
from tf.keras.callbacks import ReduceLROnPlateau, EarlyStopping
from sklearn.utils import shuffle
import numpy as np
import sys
import os
import shutil


sys.path.append("./dataset/")
import utils

alphabet_size = len(utils.alphabet)


def train_and_save_model(model_path="", n=1000, langs=None):
    def double_shuffle(a, b):
        rng_state = np.random.get_state()
        np.random.shuffle(a)
        np.random.set_state(rng_state)
        np.random.shuffle(b)

    def test_data():
        data = ["hello", "how", "are", "you", "hej", "san", "hur", "gah", "det"]
        data = np.array(list(map(lambda x: utils.vectorize_word_2d(x), data)))
        labels = np.array(
            [[0, 0, 0, 0, 1, 0, 0, 0] for i in range(4)]
            + [[0, 0, 1, 0, 0, 0, 0, 0] for i in range(5)]
        )
        return (data, labels)

    data = []
    labels = []
    if langs != None:
        data, labels = utils.get_parsed_data(n, langs)
    else:
        data, labels = utils.get_parsed_data(n)
    # data, labels = test_data()
    print(data[0], labels[0])
    data, labels = shuffle(data, labels)
    val_data = data[int(len(data) * 0.9) :]
    val_labels = labels[int(len(labels) * 0.9) :]
    data = data[: int(len(data) * 0.9) :]
    labels = labels[: int(len(labels) * 0.9)]

    print(data.shape)
    model = tf.keras.Sequential(
        [
            layers.Flatten(input_shape=(utils.max_word_length, alphabet_size)),
            layers.Dense(128, activation="relu"),
            layers.Dense(len(utils.languages), activation="softmax"),
        ]
    )
    if model_path != None:
        model = load_model(model_path)

    print(model.summary())

    # Configure a model for categorical classification.
    model.compile(
        # optimizer=tf.train.RMSPropOptimizer(0.01),
        optimizer=tf.keras.optimizers.RMSprop(
            lr=0.0005, rho=0.9, epsilon=None, decay=0.0
        ),
        loss=tf.keras.losses.categorical_crossentropy,
        metrics=[tf.keras.metrics.categorical_accuracy],
    )

    reduce_lr = ReduceLROnPlateau(
        monitor="val_loss", factor=0.2, patience=3, min_lr=0.00001
    )

    early_stopping = tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience=5)

    model.fit(
        data,
        labels,
        epochs=40,
        batch_size=256,
        validation_data=(val_data, val_labels),
        callbacks=[reduce_lr, early_stopping],
    )

    if os.path.isdir("RMS_model"):
        shutil.rmtree("RMS_model")
    os.mkdir("RMS_model")
    model.save("RMS_model/model.h5")
    with open("RMS_model/metadata.json", "w+") as metadata_file:
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

