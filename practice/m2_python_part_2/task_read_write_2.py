"""
Use function 'generate_words' to generate random words.
Write them to a new file encoded in UTF-8. Separator - '\n'.
Write second file encoded in CP1252, reverse words order. Separator - ','.

Example:
    Input: ['abc', 'def', 'xyz']

    Output:
        file1.txt (content: "abc\ndef\nxyz", encoding: UTF-8)
        file2.txt (content: "xyz,def,abc", encoding: CP1252)
"""


def generate_words(n=20):
    import string
    import random

    words = list()
    for _ in range(n):
        word = "".join(random.choices(string.ascii_lowercase, k=random.randint(3, 10)))
        words.append(word)

    return words


from pathlib import Path

CURR_DIRR = Path(__file__).parent
RES_FILE1 = CURR_DIRR / "file1.txt"
RES_FILE2 = CURR_DIRR / "file2.txt"


def write_files(words_list, res_file1, res_file2):
    with open(res_file1, "w", encoding="utf-8") as f:
        for word in words_list[:-1]:
            line = word + "\n"
            f.write(line)
        f.write(words_list[-1])

    reversed_words_list = reversed(words_list)
    with open(res_file2, "w", encoding="cp1252") as f:
        line = ",".join(reversed_words_list)
        f.write(line)


write_files(generate_words(), RES_FILE1, RES_FILE2)
