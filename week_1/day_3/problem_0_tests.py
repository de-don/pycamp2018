from unittest import TestCase

from .problem_0 import translit_text


class Problem0Tests(TestCase):

    def test_one_word(self):
        self.assertEqual(translit_text("Привет"), "Privet")
        self.assertEqual(translit_text("Денис"), "Denis")
        self.assertEqual(translit_text("интересно"), "interesno")
        self.assertEqual(translit_text("есть"), "yest")
        self.assertEqual(translit_text("Есть"), "Yest")

    def test_punctuation(self):
        self.assertEqual(translit_text("Привет, Юзер!"), "Privet, Yuzer!")
        self.assertEqual(translit_text("!Привет, Юзер!"), "!Privet, Yuzer!")

    def test_pairs(self):
        self.assertEqual(translit_text("не нее"), "ne neye")
        self.assertEqual(translit_text("пьяный пьяный"), "pianiy pianiy")
        self.assertEqual(translit_text("тощий тощий"), "toshchy toshchy")
