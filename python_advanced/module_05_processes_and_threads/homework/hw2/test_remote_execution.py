import unittest
from module_05_processes_and_threads.homework.hw2.remote_execution import app


class TestAppEndpoints(unittest.TestCase):

    def test_app_exists(self):
        self.assertIsNotNone(app)

    def test_run_code_endpoint(self):
        with app.test_client() as client:
            response = client.post('/run_code',
                                   json={'code': 'print("Hello")', 'timeout': 5})
            self.assertEqual(response.status_code, 200)
            self.assertIn('Hello', response.get_json()['result'])

    def test_run_code_timeout(self):
        with app.test_client() as client:
            response = client.post('/run_code',
                                   json={'code': 'import time; time.sleep(10)', 'timeout': 1})
            self.assertIn('истекло', response.get_json()['result'])

if __name__ == '__main__':
    unittest.main()
