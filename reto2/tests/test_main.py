# Standard libs:
import unittest

# Our libs:
import reto2


# Classes:
class TestReto2(unittest.TestCase):
    """Test reto2 main."""

    # Setup and teardown:
    def setUp(self):
        pass

    def tearDown(self):
        pass

    # Test cases:
    def test_2a(self):
        word = "2[a]"
        expected = "aa"
        
        out = reto2.translate_word(word)
        
        self.assertEqual(out, expected)
    
    def test_1h2ol2a(self):
        word = "1[h2[ol2[a]]]"
        expected = "holaaolaa"

        out = reto2.translate_word(word)

        self.assertEqual(out, expected)

    def test_2ad1io1s(self):
        word = "2[ad1[io1[s]]]"
        expected = "adiosadios"
    
        out = reto2.translate_word(word)
    
        self.assertEqual(out, expected)

    def test_2c1u2i2d2a2d2o(self):
        word = "2[c1[u2[i2[d2[a2[d2[o]]]]]]]"
        expected = "cuidadoodooadoodoodadoodooadoodooidadoodooadoodoodadoodooadoodoocuidadoodooadoodoodadoodooadoodooidadoodooadoodoodadoodooadoodoo"
    
        out = reto2.translate_word(word)
    
        self.assertEqual(out, expected)

