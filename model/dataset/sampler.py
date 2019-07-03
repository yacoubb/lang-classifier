import os
import random
import json
import sys

sys.path.append("./")
import utils


def get_sample(n=1000, languages=utils.get_default_languages()):
    sample = {}
    folder_path = "/".join(__file__.split("/")[:-1])
    for lang in languages:
        if not os.path.exists(os.path.join(folder_path, (lang + ".txt"))):
            continue
        lang = lang + ".txt"
        print(lang[:-4])
        sample[lang[:-4]] = []
        with open(
            os.path.join(folder_path, "languages_converted/", lang), "r", newline=""
        ) as lang_file:
            lines = lang_file.readlines()
            sample[lang[:-4]] = [random.choice(lines).lower() for j in range(n)]

    for key in sample:
        sample[key] = list(map(lambda x: x.replace("\n", ""), sample[key]))

    with open(os.path.join(folder_path, "test_words.json"), "w+") as test_file:
        test_file.write(json.dumps(sample, indent=4))

