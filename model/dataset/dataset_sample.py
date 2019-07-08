import os
import sys
import random
import numpy as np
import shutil
from tqdm import tqdm

sys.path.append("/".join(os.path.abspath(__file__).split("/")[:-3]))
from model.dataset import generate_random
from model.dataset import utils


def sample_all_datasets(n=1000000):
    folder_path = "/".join(os.path.abspath(__file__).split("/")[:-1])
    if os.path.isdir(os.path.join(folder_path, "languages_train")):
        shutil.rmtree(os.path.join(folder_path, "languages_train"))
    os.mkdir(os.path.join(folder_path, "languages_train"))
    # generate_random.generate_random_dataset(n)
    for lang in os.listdir(os.path.join(folder_path, "languages_converted")):
        print("loading", lang)
        words = []
        with open(
            os.path.join(folder_path, "languages_converted", lang), "r", newline=""
        ) as original_lang_file:
            words = original_lang_file.readlines()
        words = list(
            filter(
                lambda x: len(x) > utils.min_word_length
                and len(x) < utils.max_word_length,
                words,
            )
        )
        print(lang, "with", len(words), "words")
        assert len(words) > n
        sample = np.random.choice(words, size=n)
        with open(
            os.path.join(folder_path, "languages_train", lang), "w+"
        ) as lang_file:
            for word in sample:
                lang_file.write(word + "\n")


if __name__ == "__main__":
    sample_all_datasets(500000)
