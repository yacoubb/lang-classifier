import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import load_model
import numpy as np
import sys
import json

sys.path.append("./dataset")
import utils
import sampler


def estimate_model_accuracy(model):
    def predict(word):
        word = utils.total_conversion(word)
        word = word[: utils.max_word_length]
        vector_word = utils.vectorize_word_2d(word)
        vector_word = np.array([vector_word])

        result = model.predict(vector_word)

        return utils.vector_to_language(result)

    sampler.get_sample(1000)

    test_words = {}
    with open("./dataset/test_words.json", "r") as test_word_file:
        test_words = json.load(test_word_file)

    results = []
    for key in test_words:
        print(key)
        correct = 0.0
        total = 0.0
        word_predictions = []
        for word in test_words[key]:
            total += 1.0
            prediction = predict(word)
            word_predictions.append((word, prediction))
            if predict(word) == key:
                correct += 1.0

        results.append((key, correct * 100.0 / total))

    from tabulate import tabulate

    summary = ""
    summary += tabulate(results, headers=["language", "accuracy"])
    summary += "\n"
    summary += "overall accuracy: {:2f}".format(
        sum(map(lambda x: x[1], results)) / len(results)
    )
    summary += "\n"
    return summary, word_predictions


summary, all_predictions = estimate_model_accuracy(load_model("./RMS_model/model.h5"))
print(summary)

with open("./RMS_model/testing.txt", "w+") as test_file:
    test_file.write(summary)
    test_file.write("=" * 20)
    for word, pred in all_predictions:
        test_file.write(word + ", " + pred + "\n")

