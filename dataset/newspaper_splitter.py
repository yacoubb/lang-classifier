import os, csv, re, shutil

lang_count = 67
folder_path = "/".join(__file__.split("/")[:-1])
if len(folder_path) == 0:
    folder_path = "."


def save_language(lang, words):
    print("saving", len(words), "words to", lang + ".txt")
    with open("./languages/" + lang + ".txt", "w+") as langfile:
        for word in words:
            langfile.write(word + "\n")
    print("done")


def save_chars(lang, chars):
    print("saving", len(chars), "chars to", lang + ".txt")
    with open("./chars/" + lang + ".txt", "w+") as charfile:
        for char in chars:
            charfile.write(char + "\n")
    print("done")


def split_newspaper():
    if os.path.isdir("./languages"):
        print("removing languages folder")
        shutil.rmtree("./languages")
    os.mkdir("./languages")
    file_path = os.path.join(folder_path, "old_newspaper.tsv")
    print("=" * 100)
    print("loading big ass tsv file")
    with open(file_path, "r", encoding="utf-8", newline="") as movies_tsv:
        reader = csv.reader(movies_tsv, delimiter="\t")
        next(reader)
        current_lang = "Afrikaans"
        words = []
        for row in reader:
            if row[0] != current_lang:
                save_language(current_lang, words)
                words = []
                current_lang = row[0]
            # stripped = re.sub("[^a-zA-Z ]+", "", row[-1])
            stripped = row[-1]
            words.extend(list(filter(lambda x: len(x) > 0, stripped.split(" "))))


def get_all_chars():
    if os.path.isdir("./chars"):
        print("removing chars folder")
        shutil.rmtree("./chars")
    os.mkdir("./chars")

    file_path = os.path.join(folder_path, "old_newspaper.tsv")
    print("=" * 100)
    print("loading big ass tsv file")
    with open(file_path, "r", encoding="utf-8", newline="") as movies_tsv:
        reader = csv.reader(movies_tsv, delimiter="\t")
        next(reader)
        current_lang = "Afrikaans"
        lang_chars = set()
        count = 1
        for row in reader:
            if row[0] != current_lang:
                print(current_lang)
                save_chars(current_lang, lang_chars)
                lang_chars = set()
                current_lang = row[0]
                print(count, "/", lang_count)
                count += 1
            for word in row[-1].split(" "):
                for char in word:
                    lang_chars.add(char)


def compare_chars_to_languages():
    char_folder_path = os.path.join(folder_path, "chars")
    lang_folder_path = os.path.join(folder_path, "languages")
    char_files = []
    lang_files = []
    for f in os.listdir(char_folder_path):
        char_files.append(f)
    for f in os.listdir(lang_folder_path):
        lang_files.append(f)

    print("missing langfiles:")
    for x in char_files:
        if not x in lang_files:
            print(x)

    print("=" * 20)
    print("missing charfiles:")
    for x in lang_files:
        if not x in char_files:
            print(x)

    print(len(char_files) == len(lang_files))


if __name__ == "__main__":
    split_newspaper()
    # get_all_chars()
    # compare_chars_to_languages()

