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


def get_replace(diction, substring):
    replace = diction.get(substring.lower(), "")
    if substring.istitle():
        replace = replace.title()
    return replace


def transliteration(string, direction='rus2eng'):
    """ Function to transliterate string.

    Args:
        string(str): string to transliterate.
        direction(str): direction of transliterate. "eng2rus" or "rus2eng"

    Returns:
        str: translited string

    """
    directions = {'rus2eng': RUS_TO_ENG, 'eng2rus': ENG_TO_RUS}
    diction = directions.get(direction, None)
    if not diction:
        raise ValueError(f'Direction "{direction}" is not supported')

    # max replace length in diction
    max_replace_len = max(map(len, diction.keys()))

    def gen_output():
        position = 0
        while position < len(string):
            # check all substrings from longest to shortest
            for substring_len in range(max_replace_len, 0, -1):
                substring = string[position:position + substring_len]
                replace = get_replace(diction, substring)

                # if replace is found, remember it and break loop
                if replace:
                    position += substring_len
                    break
            else:
                # if replace not found, set symbol without changes
                replace = string[position]
                position += 1

            yield replace

    return ''.join(gen_output())
