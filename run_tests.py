import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import load_model
import numpy as np
import sys
import json

sys.path.append("./datasets")
import utils


def estimate_model_accuracy(model):
    def predict(word):
        word = utils.total_conversion(word)
        word = word[: utils.max_word_length]
        vector_word = utils.vectorize_word(word)
        vector_word = np.array([vector_word])

        result = model.predict(vector_word)

        return utils.vector_to_language(result)

    test_words = {}
    with open("./datasets/test_words.json", "r") as test_word_file:
        test_words = json.load(test_word_file)
        # test_words = test_word_file.read().splitlines()

    results = []
    for key in test_words:
        print(key)
        correct = 0.0
        total = 0.0
        for word in test_words[key]:
            total += 1.0
            prediction = predict(word)
            if predict(word) == key:
                correct += 1.0
        results.append((key, correct * 100.0 / total))

    # results = []
    # for word in test_words:
    #     if len(word) == 0:
    #         print("")
    #         continue
    #     results.append(predict(word))

    from tabulate import tabulate

    summary = ""
    summary += tabulate(results, headers=["language", "accuracy"])
    summary += "\n"
    summary += "overall accuracy: {:2f}".format(
        sum(map(lambda x: x[1], results)) / len(results)
    )
    summary += "\n"
    return summary


total_testing = ""
total_testing += "RMS\n"
total_testing += estimate_model_accuracy(load_model("lang_predictor_RMS.h5"))
total_testing += "=" * 30 + "\n"
total_testing += "sgd\n"
total_testing += estimate_model_accuracy(load_model("lang_predictor_sgd.h5"))

with open("./testing_results.txt", "w+") as test_file:
    test_file.write(total_testing)
