import tensorflowjs as tfjs
import tensorflow as tf
from tensorflow.keras.models import load_model
import shutil
import os


def convert():
    model = load_model("./RMS_model/model.h5")
    model.compile(
        optimizer=tf.keras.optimizers.RMSprop(
            lr=0.001, rho=0.9, epsilon=None, decay=0.0
        ),
        loss=tf.keras.losses.categorical_crossentropy,
        metrics=[tf.keras.metrics.categorical_accuracy],
    )
    if os.path.isdir("../web/server/converted_model/"):
        shutil.rmtree("../web/server/converted_model/")
    os.makedirs("../web/server/converted_model/")
    tfjs.converters.save_keras_model(model, "../web/server/converted_model/")
    shutil.copy(
        "./RMS_model/metadata.json", "../web/server/converted_model/metadata.json"
    )


if __name__ == "__main__":
    convert()
