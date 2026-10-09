import unittest
from module_02_linux.homework.hw7.accounting import app, storage


class FinanceAppTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False

        cls.app = app.test_client()

        storage.update({
            "20250101": 100,
            "20250115": 300,
            "20250210": 500,
            "20260125": 250,
        })

    def test_add_valid_date(self):
        response = self.app.get("/add/20260126/100")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Добавлено 100 руб. за 20260126", response.get_data(as_text=True))
        self.assertEqual(storage["20260126"], 100)

    def test_calculate_year(self):
        response = self.app.get("/calculate/2025")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True), "900")

    def test_calculate_month(self):
        response = self.app.get("/calculate/2025/01")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True), "400")


if __name__ == "__main__":
    unittest.main()
