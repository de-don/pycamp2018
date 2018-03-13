from unittest import TestCase

from .problem_0 import transliteration


class Problem0Tests(TestCase):
    def setUp(self):
        self.rus2eng, self.eng2rus = transliteration()

    def test_one_word(self):
        rus = 'Привет'
        eng = self.rus2eng(rus)
        self.assertEqual(eng, 'Privet')
        self.assertEqual(self.eng2rus(eng), rus)

    def test_punctuation(self):
        rus = '!ЗдравсТвуй, Юзер!'
        eng = self.rus2eng(rus)
        self.assertEqual(eng, '!ZdravsTvujj, Juzer!')
        self.assertEqual(self.eng2rus(eng), rus)

    def test_complex(self):
        rus = 'не нее, льняной, тощий'
        eng = self.rus2eng(rus)
        self.assertEqual(eng, 'ne nee, l\'njanojj, toshhijj')
        self.assertEqual(self.eng2rus(eng), rus)
