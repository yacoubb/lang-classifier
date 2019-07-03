import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import sys
import os
import shutil

sys.path.append("./dataset/")
import utils

alphabet_size = len(utils.alphabet)


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


data, labels = utils.get_parsed_data(1000000)
# data, labels = test_data()
print(data[0], labels[0])
# double_shuffle(data, labels)
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

print(model.summary())

# Configure a model for categorical classification.
model.compile(
    # optimizer=tf.train.RMSPropOptimizer(0.01),
    optimizer=tf.keras.optimizers.RMSprop(lr=0.001, rho=0.9, epsilon=None, decay=0.0),
    loss=tf.keras.losses.categorical_crossentropy,
    metrics=[tf.keras.metrics.categorical_accuracy],
)


model.fit(
    data, labels, epochs=40, batch_size=128, validation_data=(val_data, val_labels)
)

if os.path.isdir("./model"):
    shutil.rmtree("./model")
os.mkdir("./model")
model.save("model/lang_predictor_RMS.h5")
with open("model/metadata.json", "w+") as metadata_file:
    metadata = {
        "maxWordLength": utils.max_word_length,
        "alphabet": utils.alphabet,
        "languages": utils.languages,
    }
    import json

    metadata_file.write(json.dumps(metadata, indent=4))
