RUS_TO_ENG = {
    'а': 'a',
    'б': 'b',
    'в': 'v',
    'г': 'g',
    'д': 'd',
    'е': 'e',
    'з': 'z',
    'и': 'i',
    'к': 'k',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'о': 'o',
    'п': 'p',
    'р': 'r',
    'с': 's',
    'т': 't',
    'у': 'u',
    'ф': 'f',
    'ц': 'c',
    'ь': '\'',
    'ъ': '\"',
    'ы': 'y',
    'й': 'jj',
    'ё': 'jo',
    'ж': 'zh',
    'х': 'kh',
    'ч': 'ch',
    'ш': 'sh',
    'э': 'eh',
    'ю': 'ju',
    'я': 'ja',
    'щ': 'shh',
}
ENG_TO_RUS = dict(map(reversed, RUS_TO_ENG.items()))


def transliteration(string, direction='rus2eng'):
    """ Function to transliterate string.

    Args:
        string(str): string to transliterate.
        direction(str): direction of transliterate. "eng2rus" or "rus2eng"

    Returns:
        str: translited string

    """

    if direction == 'rus2eng':
        diction = RUS_TO_ENG
    elif direction == 'eng2rus':
        diction = ENG_TO_RUS
    else:
        raise ValueError(f'Direction "{direction}" is not supported')

    # max replace length in diction
    max_replace_len = max(map(len, diction.keys()))

    position = 0
    out_string = []
    while position < len(string):

        # check all substrings from longest to shortest
        for substring_len in range(max_replace_len, 0, -1):
            substring = string[position:position + substring_len].lower()

            # if replace is found, remember it and break loop
            if substring in diction:
                replace = diction[substring]
                break
        else:
            # if replace not found, set symbol without changes
            substring_len = 1
            replace = string[position]

        # if current symbol is upper, capitalized all replace
        if string[position].isupper():
            replace = replace.capitalize()

        out_string.append(replace)
        position += substring_len

    return ''.join(out_string)
