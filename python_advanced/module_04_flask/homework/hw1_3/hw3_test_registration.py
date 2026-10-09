"""
Для каждого поля и валидатора в эндпоинте /registration напишите юнит-тест,
который проверит корректность работы валидатора. Таким образом, нужно проверить, что существуют наборы данных,
которые проходят валидацию, и такие, которые валидацию не проходят.
"""

import unittest

from module_04_flask.homework.hw1_3.hw1_registration import app


class TestRegistration(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['TESTING'] = True

    def test_all_fields_invalid(self):
        response = self.client.post('/registration', data={
            'email': 'example@Gmail.com',
            'phone': '1234567890',
            'name': 'Gonsales',
            'address': 'Hope street',
            'index': '12',
        })
        self.assertEqual(response.status_code, 200)

    def test_gmail_error_1(self):
        response = self.client.post('/registration', data={
            'email': 'exampleGmail.com',
            'phone': '1234567890',
            'name': 'Gonsales',
            'address': 'Hope street',
            'index': '12',
        })
        self.assertEqual(response.status_code, 400)

    def test_phone_more_than_limit_error(self):
        response = self.client.post('/registration', data={
            'email': 'example@Gmail.com',
            'phone': '123456789046578547857856985687658756856756865',
            'name': 'Gonsales',
            'address': 'Hope street',
            'index': '12',
        })
        self.assertEqual(response.status_code, 400)

    def test_phone_less_than_minimum_number(self):
        response = self.client.post('/registration', data={
            'email': 'example@Gmail.com',
            'phone': '1234567',
            'name': 'Gonsales',
            'address': 'Hope street',
            'index': '12',
        })
        self.assertEqual(response.status_code, 400)

    def test_no_something_error_1(self):
        response = self.client.post('/registration', data={
            'email': '',
            'phone': '1234567890',
            'name': 'Gonsales',
            'address': 'Hope street',
            'index': '12',
        })
        self.assertEqual(response.status_code, 400)

    def test_no_something_error_2(self):
        response = self.client.post('/registration', data={
            'email': 'example@Gmail.com',
            'phone': '',
            'name': 'Gonsales',
            'address': 'Hope street',
            'index': '12',
        })
        self.assertEqual(response.status_code, 400)

    def test_no_something_error_3(self):
        response = self.client.post('/registration', data={
            'email': 'example@Gmail.com',
            'phone': '1234567890',
            'name': '',
            'address': 'Hope street',
            'index': '12',
        })
        self.assertEqual(response.status_code, 400)

    def test_no_something_error_4(self):
        response = self.client.post('/registration', data={
            'email': 'example@Gmail.com',
            'phone': '1234567890',
            'name': 'Gonsales',
            'address': '',
            'index': '12',
        })
        self.assertEqual(response.status_code, 400)

    def test_no_something_error_5(self):
        response = self.client.post('/registration', data={
            'email': 'example@Gmail.com',
            'phone': '1234567890',
            'name': 'Gonsales',
            'address': 'Hope street',
            'index': '',
        })
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
