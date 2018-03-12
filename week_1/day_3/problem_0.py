import re

ru2eng = {
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "е": "e",
    "ё": "e",
    "ж": "zh",
    "з": "z",
    "и": "i",
    "й": "y",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "kh",
    "ц": "ts",
    "ч": "ch",
    "ш": "sh",
    "щ": "shch",
    "ъ": "",
    "ы": "",
    "ь": "",
    "э": "e",
    "ю": "yu",
    "я": "ya"
}
glasn = "ёуеаоэяию"


def translit_word(word):
    """ Translit single word by rules https://www.nic.ru/dns/translit.shtml """

    output_str = ""

    for i, ch in enumerate(word):
        ch_lower = ch.lower()
        to_ch = ru2eng.get(ch.lower(), None)
        end = False

        if ch_lower in "её":
            if i == 0 or word[i - 1].lower() in glasn:
                to_ch = "ye"

        if ch_lower == "я":
            if i > 0 and word[i - 1].lower() == "ь":
                to_ch = "ia"

        if i == len(word) - 2 and word[i + 1].lower() == "й":
            if ch_lower == "и":
                to_ch = "y"
                end = True
            if ch_lower == "ы":
                to_ch = "iy"
                end = True

        if to_ch is None:
            to_ch = ch
        if ch.isupper():
            output_str += to_ch.capitalize()
        else:
            output_str += to_ch

        if end:
            break

    return output_str


def translit_text(text):
    """ Function to translit text"""

    # find all substrings: word or punstuation
    substrings = re.findall(r"[-А-Яа-я]+|[^-А-Яа-я]+", text)

    # translit all substrings and join it
    return "".join(map(translit_word, substrings))
