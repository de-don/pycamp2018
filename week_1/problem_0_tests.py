from unittest import TestCase

from .problem_0 import transliteration


class Problem0Tests(TestCase):
    def test_one_word(self):
        rus = 'Привет'
        eng = transliteration(rus)
        self.assertEqual(eng, 'Privet')
        self.assertEqual(transliteration(eng, "eng2rus"), rus)

    def test_punctuation(self):
        rus = '!ЗдравсТвуй, Юзер!'
        eng = transliteration(rus)
        self.assertEqual(eng, '!ZdravsTvujj, Juzer!')
        self.assertEqual(transliteration(eng, "eng2rus"), rus)

    def test_complex(self):
        rus = 'не нее, льняной, тощий'
        eng = transliteration(rus)
        self.assertEqual(eng, 'ne nee, l\'njanojj, toshhijj')
        self.assertEqual(transliteration(eng, "eng2rus"), rus)

    def test_undefined_direction(self):
        with self.assertRaises(ValueError):
            transliteration('test', 'rus2ara')
