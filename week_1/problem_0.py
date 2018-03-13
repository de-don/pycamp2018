def transliteration():
    """Function which create functions to transliteration

    Returns:
        function: function to transliteration from russian to english
        function: function to transliteration from english to russian
    """

    single_letters = {
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
    }
    not_capitalize_letters = {
        'ь': '\'',
        'ъ': '\"',
        'ы': 'y',
    }
    pairs_letters = {
        'й': 'jj',
        'ё': 'jo',
        'ж': 'zh',
        'х': 'kh',
        'ч': 'ch',
        'ш': 'sh',
        'э': 'eh',
        'ю': 'ju',
        'я': 'ja',
    }
    triples_letters = {
        'щ': 'shh',
    }

    # generate capitalized cases
    capitalize_single_letters = {
        k.upper(): v.upper() for k, v in single_letters.items()
    }
    capitalize_pairs_letters = {
        k.capitalize(): v.capitalize() for k, v in pairs_letters.items()
    }
    capitalize_triples_letters = {
        k.capitalize(): v.capitalize() for k, v in triples_letters.items()
    }

    def translite(string, rev=False):
        """ Function to translit string from Russian to English and reverse.

        Args:
            string(str): string to transliteration
            rev(bool): translit from russian to english (False),
                or from english to russian (True).

        Returns:
            string: translited string
        """

        for dicts in (capitalize_triples_letters, capitalize_pairs_letters,
                      capitalize_single_letters, triples_letters,
                      pairs_letters, single_letters, not_capitalize_letters):
            for cyrillic_string, latin_string in dicts.items():
                if rev:
                    string = string.replace(latin_string, cyrillic_string)
                else:
                    string = string.replace(cyrillic_string, latin_string)

        return string

    def rus2eng(string):
        """ Function to transliteration string from russian to english

        Args:
            string(str): string on russian

        Returns:
            string: string on english
        """

        return translite(string, False)

    def eng2rus(string):
        """ Function to to transliteration from english to russian

        Args:
            string(str): string on english

        Returns:
            string: string on russian
        """

        return translite(string, True)

    return rus2eng, eng2rus
