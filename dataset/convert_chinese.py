import pinyin


def convert(file_path):
    converted_lines = []
    with open(file_path, "r") as chinese_file:
        print("opened original file")
        original_lines = chinese_file.readlines()
        for line in original_lines:
            converted_lines.append(pinyin.get(line, format="strip", delimiter=" "))
    with open(file_path[:-4] + "_converted" + file_path[-4:], "w+") as converted_file:
        print("writing conversion")
        for line in converted_lines:
            converted_file.write(line + "\n")


if __name__ == "__main__":
    convert("./languages/Chinese (Simplified).txt")
    convert("./languages/Chinese (Traditional).txt")

