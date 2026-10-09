import unittest
from module_03_ci_culture_beginning.homework.hw2 import decrypt


class TestDecrypt(unittest.TestCase):
    def test_single_dot_after_letter(self):
        """Тесты: буква. → оставить букву"""
        self.subTest("абра-кадабра.")
        self.assertEqual(decrypt("абра-кадабра."), "абра-кадабра")

        self.subTest("абр......a.")
        self.assertEqual(decrypt("абр......a."), "a")


    def test_double_dots_delete_previous(self):
        """Тесты: .. → удалить символ перед ними"""
        self.subTest("абраа..-кадабра")
        self.assertEqual(decrypt("абраа..-кадабра"), "абра-кадабра")


        self.subTest("абраа..-.кадабра")
        self.assertEqual(decrypt("абраа..-.кадабра"), "абра-кадабра")

        self.subTest("абра--..кадабра")
        self.assertEqual(decrypt("абра--..кадабра"), "абра-кадабра")


    def test_multiple_dots_combinations(self):
        """Тесты: сложные комбинации точек"""
        self.subTest("абрау...-кадабра")
        self.assertEqual(decrypt("абрау...-кадабра"), "абра-кадабра")


    def test_empty_result_cases(self):
        """Тесты: результат = пустая строка"""
        self.subTest("абра........")
        self.assertEqual(decrypt("абра........"), "")


        self.subTest(".")
        self.assertEqual(decrypt("."), "")

        self.subTest("1.......................")
        self.assertEqual(decrypt("1......................."), "")


    def test_digits_and_special_chars(self):
        """Тесты: цифры и спецсимволы"""
        self.subTest("1..2.3")
        self.assertEqual(decrypt("1..2.3"), "23")


if __name__ == '__main__':
    unittest.main(verbosity=2)
