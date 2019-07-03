import os
import shutil
import sys
from multiprocessing import Pool

sys.path.append("./")
import utils


def convert(lang):
    print(lang)
    converted_lines = []
    with open("./languages_to_convert/" + lang, "r") as lang_file:
        with open("./languages_converted/" + lang, "w+") as converted_file:
            lines = lang_file.readlines()
            for line in lines:
                converted_line = utils.total_conversion(line)
                for word in converted_line.split(" "):
                    if len(word) < utils.max_word_length and len(word) > 0:
                        converted_file.write(word + "\n")
    print(lang, "finished converting")


def convert_all():
    if os.path.isdir("./languages_converted"):
        shutil.rmtree("./languages_converted")
    os.mkdir("./languages_converted")
    files = os.listdir("./languages_to_convert")
    files = list(filter(lambda x: x.endswith(".txt"), files))

    # files = ["english.txt", "chinese.txt"]

    pool = Pool(processes=len(files))
    pool.map(convert, files)


if __name__ == "__main__":
    convert_all()
    # convert("Swedish.txt")
