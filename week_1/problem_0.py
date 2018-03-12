def transliteration():
    single_letters = {
        "а": "a",
        "б": "b",
        "в": "v",
        "г": "g",
        "д": "d",
        "е": "e",
        "з": "z",
        "и": "i",
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
        "ц": "c",
    }

    not_capitalize_letters = {
        "ь": "'",
        "ъ": "\"",
        "ы": "y",
    }

    pairs_letters = {
        'й': "jj",
        "ё": "jo",
        "ж": "zh",
        "х": "kh",
        "ч": "ch",
        "ш": "sh",
        "э": "eh",
        "ю": "ju",
        "я": "ja",
    }

    triples_letters = {
        "щ": "shh",
    }
    capitalize_single_letters = {k.upper(): v.upper() for k, v in single_letters.items()}
    capitalize_pairs_letters = {k.capitalize(): v.capitalize() for k, v in pairs_letters.items()}
    capitalize_triples_letters = {k.capitalize(): v.capitalize() for k, v in triples_letters.items()}

    def rus2eng(string):
        """ Function to translit string"""

        for dictionary in (capitalize_triples_letters, capitalize_pairs_letters, capitalize_single_letters):
            for cyrillic_string, latin_string in dictionary.items():
                string = string.replace(cyrillic_string, latin_string)

        for dictionary in (triples_letters, pairs_letters, single_letters, not_capitalize_letters):
            for cyrillic_string, latin_string in dictionary.items():
                string = string.replace(cyrillic_string, latin_string)

        return string

    def eng2rus(string):
        """ Function to translit string"""

        for dictionary in (capitalize_triples_letters, capitalize_pairs_letters, capitalize_single_letters):
            for cyrillic_string, latin_string in dictionary.items():
                string = string.replace(latin_string, cyrillic_string)

        for dictionary in (triples_letters, pairs_letters, single_letters, not_capitalize_letters):
            for cyrillic_string, latin_string in dictionary.items():
                string = string.replace(latin_string, cyrillic_string)

        return string

    return rus2eng, eng2rus
