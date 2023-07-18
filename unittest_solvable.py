import unittest
from solvable import solvable

class TestSolvable(unittest.TestCase):
    # tests solvable function with known solvable tile orders
    # and known unsolvable tile orders
    def test_init(self):
        a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 15]
        self.assertEqual(solvable(len(a), a), True)
        b = [1, 2, 3, 4, 5, 6, 7, 9, 8]
        self.assertEqual(solvable(len(b), b), True)
        c = [1, 3, 2, 4]
        self.assertEqual(solvable(len(c), c), False)

def main():
    unittest.main(verbosity=3)

main()
