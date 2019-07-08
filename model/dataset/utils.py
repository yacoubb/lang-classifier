import sys
import os
import numpy as np
import random
import csv
import re
import unidecode

max_word_length = 20

folder_path = "/".join(__file__.split("/")[:-1])

if not os.path.isdir(os.path.join(folder_path, "languages_converted")):
    os.mkdir(os.path.join(folder_path, "languages_converted"))


def get_default_languages():
    languages = ["random"] + list(
        map(
            lambda x: x[:-4],
            filter(
                lambda x: x.endswith(".txt"),
                os.listdir(os.path.join(folder_path, "languages_converted")),
            ),
        )
    )
    return languages


def initalise_language_vectors():
    global languages
    global language_vectors
    for i in range(len(languages)):
        vec = [0 for j in range(len(languages))]
        vec[i] = 1
        language_vectors[languages[i]] = vec


languages = get_default_languages()
language_vectors = {}
initalise_language_vectors()

alphabet = "abcdefghijklmnopqrstuvwxyz"
alphabet_vectors = {}
for char in alphabet:
    vec = [0 for i in range(len(alphabet))]
    vec[alphabet.index(char)] = 1
    alphabet_vectors[char] = vec


def vectorize_word(word):
    parsed_word = []
    for char in word:
        global alphabet_vectors
        if not char in alphabet_vectors.keys():
            # print("missed letter " + char + ", " + word)
            continue
        parsed_word.extend(alphabet_vectors[char])
    parsed_word.extend(
        [0 for i in range(max_word_length * len(alphabet_vectors) - len(parsed_word))]
    )
    return parsed_word


zero_vec = [0 for i in range(len(alphabet_vectors))]


def vectorize_word_2d(word):
    parsed_word = []
    for char in word:
        global alphabet_vectors
        if not char in alphabet_vectors.keys():
            # print("missed letter " + char + ", " + word)
            continue
        parsed_word.append(alphabet_vectors[char])
    parsed_word.extend([zero_vec for i in range(max_word_length - len(parsed_word))])
    return np.array(parsed_word)


def get_parsed_data(n=1000, langs=None, include_random=False):
    if langs == None:
        langs = get_default_languages()
    parsed_data = []
    labels = []
    print("language list", langs)
    for lang in langs:
        langfile_path = os.path.join(
            folder_path, "languages_converted", (lang + ".txt")
        )
        if os.path.exists(langfile_path):
            print("loading:", lang)
            with open(langfile_path, "r", newline="") as langfile:
                words = langfile.readlines()
                words = list(
                    filter(lambda x: len(x) < max_word_length and len(x) > 0, words)
                )
                word_count = len(words)
                print(lang, word_count)
                selection = random.choices(words, k=n)
                parsed_data.extend(list(map(lambda x: vectorize_word_2d(x), selection)))
                labels.extend([language_vectors[lang] for j in range(len(selection))])
                del selection
    if include_random:
        random_words = []
        for i in range(n):
            random_words.append(
                "".join(
                    random.choice(alphabet)
                    for _ in range(random.randint(4, max_word_length))
                )
            )
        parsed_data.extend(list(map(lambda x: vectorize_word_2d(x), random_words)))
        labels.extend([language_vectors["random"] for j in range(len(random_words))])
        del random_words

    return (np.array(parsed_data), np.array(labels))


def vector_to_language(vec, langs):
    if langs != None:
        return langs[np.argmax(vec)]
    return languages[np.argmax(vec)]


def manual_conversion(word):
    diacritics = {
        u"Ä": "ae",
        u"Ö": "oe",
        u"Ü": "ue",
        u"ä": "ae",
        u"ö": "oe",
        u"ü": "ue",
        u"å": "oa",
        u"š": "sh",
        u"í": "ee",
        u"ð": "th",
        u"þ": "th",
    }
    for key, value in diacritics.items():
        if key in word:
            word = word.replace(key, value)
    return word


def total_conversion(line):
    converted_line = manual_conversion(line)
    converted_line = unidecode.unidecode(line)
    converted_line = converted_line.lower()
    converted_line = re.sub("[^a-zA-Z ]+", " ", converted_line)
    return converted_line


if __name__ == "__main__":
    get_parsed_data(2000)
