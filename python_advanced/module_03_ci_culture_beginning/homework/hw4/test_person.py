import unittest
from datetime import datetime
from module_03_ci_culture_beginning.homework.hw4.person import Person  # замените на ваш модуль


class TestPerson(unittest.TestCase):
    def setUp(self):
        self.person = Person("Иван", 1990)

    def test_init_correct(self):
        """Проверка корректной инициализации"""
        person = Person("Анна", 1985, "ул. Ленина 1")
        self.assertEqual(person.name, "Анна")
        self.assertEqual(person.yob, 1985)
        self.assertEqual(person.address, "ул. Ленина 1")

    def test_get_age_correct_calculation(self):
        """✅ get_age работает правильно"""
        now = datetime.now()
        expected_age = now.year - 1990
        self.assertEqual(self.person.get_age(), expected_age)

    def test_get_name_works(self):
        """✅ get_name возвращает имя"""
        self.assertEqual(self.person.get_name(), "Иван")

    def test_set_name_does_not_change(self):
        """❌ set_name НЕ ИЗМЕНЯЕТ имя (баг!)"""
        original_name = self.person.name
        self.person.set_name("Петр")
        self.assertEqual(self.person.name, original_name)

    def test_set_address_assignment_error(self):
        """❌ set_address использует == вместо = (баг!)"""
        self.person.set_address("ул. Мира 5")
        self.assertEqual(self.person.address, "ул. Мира 5")

    def test_get_address_works(self):
        """✅ get_address возвращает адрес"""
        person_with_address = Person("Мария", 1995, "ул. Пушкина 10")
        self.assertEqual(person_with_address.get_address(), "ул. Пушкина 10")

    def test_is_homeless_logic_error(self):
        """❌ is_homeless проверяет не тот объект (баг!)"""
        self.assertFalse(self.person.is_homeless())

        person_homeless = Person("Бездомный", 1980, "")
        self.assertFalse(person_homeless.is_homeless())  # баг!

        person_with_home = Person("Домовладелец", 1990, "ул. Дом 1")
        self.assertFalse(person_with_home.is_homeless())  # случайно правильно


if __name__ == '__main__':
    unittest.main()
