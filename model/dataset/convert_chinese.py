import pinyin


def convert(file_path):
    converted_lines = []
    with open(file_path, "r") as chinese_file:
        print("opened original file")
        original_lines = chinese_file.readlines()
        for line in original_lines:
            converted_line = pinyin.get(line, format="strip", delimiter="")
            # converted_line = ""
            # for word in line.split(" "):
            #     converted_line += pinyin.get(word, format="strip", delimiter="")
            #     converted_line += " "
            converted_lines.append(converted_line)
    with open(file_path[:-4] + "_converted" + file_path[-4:], "w+") as converted_file:
        print("writing conversion")
        for line in converted_lines:
            converted_file.write(line + "\n")


if __name__ == "__main__":
    convert("./languages/Chinese (Simplified).txt")
    # convert("./languages/Chinese (Traditional).txt")

