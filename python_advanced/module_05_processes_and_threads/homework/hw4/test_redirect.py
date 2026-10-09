import unittest
import sys
from io import StringIO
from module_05_processes_and_threads.homework.hw4.redirect import Redirect  # Замените на ваш импорт


class TestRedirect(unittest.TestCase):

    def test_redirect_stdout_to_stringio(self):
        buffer = StringIO()

        with Redirect(stdout=buffer):
            print("Hello!")

        self.assertIn("Hello!", buffer.getvalue())

    def test_redirect_stderr_to_stringio(self):
        buffer = StringIO()

        with Redirect(stderr=buffer):
            print("Error!", file=sys.stderr)

        self.assertIn("Error!", buffer.getvalue())

    def test_redirect_both_streams(self):
        stdout_buf = StringIO()
        stderr_buf = StringIO()

        with Redirect(stdout=stdout_buf, stderr=stderr_buf):
            print("stdout test")
            print("stderr test", file=sys.stderr)

        self.assertIn("stdout test", stdout_buf.getvalue())
        self.assertIn("stderr test", stderr_buf.getvalue())

    def test_no_redirect_when_none(self):
        original_stdout = sys.stdout
        original_stderr = sys.stderr

        with Redirect():
            print("test")

        self.assertIs(sys.stdout, original_stdout)
        self.assertIs(sys.stderr, original_stderr)

    def test_restores_streams_after_exception(self):
        buffer = StringIO()
        original_stdout = sys.stdout

        try:
            with Redirect(stdout=buffer):
                raise ValueError("test")
        except ValueError:
            pass

        self.assertIs(sys.stdout, original_stdout)

    def test_only_stdout_not_stderr(self):
        stdout_buf = StringIO()

        with Redirect(stdout=stdout_buf):
            print("stdout message")
            print("stderr message", file=sys.stderr)

        self.assertIn("stdout message", stdout_buf.getvalue())
        self.assertNotIn("stderr message", stdout_buf.getvalue())

if __name__ == '__main__':
    unittest.main()
    # with open('test_results.txt', 'a') as test_file_stream:
    #     runner = unittest.TextTestRunner(stream=test_file_stream)
    #     unittest.main(testRunner=runner)
