import unittest
from main_algorithm import call_algorithm


class TestMainAlgorithm(unittest.TestCase):

    def test_algorithm(self):
        self.assertNotEqual(call_algorithm(), None)


if __name__ == '__main__':
    unittest.main()
