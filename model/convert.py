import tensorflowjs as tfjs
import tensorflow as tf
from tensorflow.keras.models import load_model


def convert():
    model = load_model("./lang_predictor_RMS.h5")
    model.compile(
        optimizer=tf.keras.optimizers.RMSprop(
            lr=0.001, rho=0.9, epsilon=None, decay=0.0
        ),
        loss=tf.keras.losses.categorical_crossentropy,
        metrics=[tf.keras.metrics.categorical_accuracy],
    )
    tfjs.converters.save_keras_model(model, "./web/server/converted_model/")


if __name__ == "__main__":
    convert()
