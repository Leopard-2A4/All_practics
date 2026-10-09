import unittest
import datetime

from module_03_ci_culture_beginning.homework.hw1.hello_word_with_day import app


class TestMaxNumberApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.base_url = '/hello-world/'

    def test_can_get_correct_max_number_in_series_of_two(self):
        days = (
            "понедельника",
            "вторника",
            "среды",
            "четверга",
            "пятницы",
            "субботы",
            "воскресенья"
        )

        weekday: int = datetime.datetime.today().weekday()
        now_day: str = days[weekday]

        username = 'username'
        response = self.app.get(self.base_url + username)

        response_text = response.data.decode()

        self.assertTrue(now_day in response_text)
        self.assertTrue(username in response_text)
