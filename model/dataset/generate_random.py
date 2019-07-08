import os
import sys
import random
from tqdm import tqdm

sys.path.append("/".join(os.path.abspath(__file__).split("/")[:-3]))
from model.dataset import utils


def generate_random_dataset(n=1000000):
    folder_path = "/".join(os.path.abspath(__file__).split("/")[:-1])
    if os.path.exists(os.path.join(folder_path, "languages_train", "random.txt")):
        os.remove(os.path.join(folder_path, "languages_train", "random.txt"))

    with open(
        os.path.join(folder_path, "languages_train", "random.txt"), "w+"
    ) as random_file:
        for i in tqdm(range(n)):
            rand_word = (
                "".join(
                    random.choice(utils.alphabet)
                    for _ in range(random.randint(2, utils.max_word_length))
                )
                + "\n"
            )
            random_file.write(rand_word)


if __name__ == "__main__":
    generate_random_dataset()
