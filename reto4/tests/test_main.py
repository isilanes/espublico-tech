# Standard libs:
import unittest
import numpy as np

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
        family.calculate_genotype_probabilities()
        
        expected_probabilities = {
            "Bor": np.array([0, 1, 0]),
            "Bestla": np.array([0, 1, 0]),
            "Ve": np.array([0.3333333, 0.6666666, 0]),
            "Odin": np.array([0, 0, 1]),
            "Jord": np.array([0, 1, 0]),
            "Sif": np.array([0.5, 0.5, 0]),
            "Thor": np.array([0, 0, 1]),
            "Jarnsaxa": np.array([0.5, 0.5, 0]),
            "Thrud": np.array([0, 1, 0]),
            "Modi": np.array([0, 1, 0]),
            "Magni": np.array([0, 1, 0]),
        }
        
        for name, expected in expected_probabilities.items():
            calculated = family.members[name].genotype_probabilities
            diff = sum(abs(calculated - expected))
            self.assertAlmostEqual(diff, 0, 6)

    def test_case_02(self):
        family = reto4.parse_input("tests/input_02.txt")
        family.calculate_genotype_probabilities()
    
        expected_probabilities = {
            "Bor": np.array([0, 1, 0]),
            "Bestla": np.array([0, 0, 1]),
            "Ve": np.array([0, 1, 0]),
            "Odin": np.array([0, 0, 1]),
            "Jord": np.array([0, 0, 1]),
            "Thor": np.array([0, 0, 1]),
            "Jarnsaxa": np.array([0.5, 0.5, 0]),
            "Magni": np.array([0, 1, 0]),
        }
    
        for name, expected in expected_probabilities.items():
            calculated = family.members[name].genotype_probabilities
            diff = sum(abs(calculated - expected))
            self.assertAlmostEqual(diff, 0, 6, f"{name} fails")

    def test_case_03(self):
        family = reto4.parse_input("tests/input_03.txt")
        family.calculate_genotype_probabilities()
    
        expected_probabilities = {
            "Bor": np.array([0, 1, 0]),
            "Bestla": np.array([0, 1, 0]),
            "Ve": np.array([0.3333333, 0.6666666, 0]),
            "Pepa": np.array([0.5, 0.5, 0]),
            "Vepe": np.array([0.5454545454545454, 0.45454545454545453, 0]),
            "Odin": np.array([0, 0, 1]),
            "Jord": np.array([0, 0, 1]),
            "Thor": np.array([0, 0, 1]),
            "Jarnsaxa": np.array([0.5, 0.5, 0]),
            "Magni": np.array([0, 1, 0]),
        }
    
        for name, expected in expected_probabilities.items():
            calculated = family.members[name].genotype_probabilities
            diff = sum(abs(calculated - expected))
            self.assertAlmostEqual(diff, 0, 6, f"{name} fails with {calculated}")

