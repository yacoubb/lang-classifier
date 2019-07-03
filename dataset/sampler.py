import os
import random
import json


def get_sample(n=1000):
    sample = {}
    for lang in os.listdir("./languages_converted"):
        if not lang.endswith(".txt"):
            continue
        print(lang[:-4])
        sample[lang[:-4]] = []
        with open("./languages_converted/" + lang, "r", newline="") as lang_file:
            lines = lang_file.readlines()
            sample[lang[:-4]] = [random.choice(lines).lower() for j in range(n)]

    for key in sample:
        sample[key] = list(map(lambda x: x.replace("\n", ""), sample[key]))

    with open("./test_words.json", "w+") as test_file:
        test_file.write(json.dumps(sample, indent=4))

