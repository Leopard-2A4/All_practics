import unittest
from module_05_processes_and_threads.homework.hw3.block_errors import BlockErrors


class TestBlockErrors(unittest.TestCase):

    def test_ignore_single_exception_type(self):
        with BlockErrors([ValueError]):
            raise ValueError("test")

    def test_ignore_multiple_exception_types(self):
        with BlockErrors([ValueError, TypeError, KeyError]):
            raise ValueError("test")

    def test_normal_exit_no_exception(self):
        with BlockErrors([ValueError]):
            x = 42
        assert x == 42

    def test_ignore_exception_subclasses(self):

        class CustomValueError(ValueError):
            pass

        with BlockErrors([ValueError]):
            raise CustomValueError("test")

    def test_exception_order_independent(self):
        with BlockErrors([TypeError, ValueError]):
            raise ValueError("test")

if __name__ == '__main__':
    unittest.main()
