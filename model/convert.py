import tensorflowjs as tfjs
from tensorflow import keras
import shutil
import os


def convert():
    model_path = "./all_models/RMS_model_triple/"
    model = keras.models.load_model(model_path + "model.h5")
    model.compile(
        optimizer=keras.optimizers.RMSprop(lr=0.001, rho=0.9, epsilon=None, decay=0.0),
        loss=keras.losses.categorical_crossentropy,
        metrics=[keras.metrics.categorical_accuracy],
    )
    if os.path.isdir("../web/server/converted_model/"):
        shutil.rmtree("../web/server/converted_model/")
    os.makedirs("../web/server/converted_model/")
    tfjs.converters.save_keras_model(model, "../web/server/converted_model/")
    shutil.copy(
        model_path + "metadata.json", "../web/server/converted_model/metadata.json"
    )


if __name__ == "__main__":
    convert()
