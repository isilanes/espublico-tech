# Standard libs:
import unittest

# Our libs:
import reto4


# Classes:
class TestReto4(unittest.TestCase):
    """Test reto4 main."""

    # Setup and teardown:
    def setUp(self):
        pass

    def tearDown(self):
        pass

    # Test cases:
    def test_case_01(self):
        family = reto4.parse_input("tests/input_01.txt")

