import unittest
from puzzle_game import generate_solvable_tile_order
from solvable import solvable

class TestSolvable(unittest.TestCase):
    # tests function which guarantees a solvable tile_order with
    # different puzzle sizes
    def test_init(self):
        a = 4
        self.assertEqual(solvable(a, generate_solvable_tile_order(a)), True)
        b = 9
        self.assertEqual(solvable(b, generate_solvable_tile_order(b)), True)
        c = 16
        self.assertEqual(solvable(c, generate_solvable_tile_order(c)), True)
        d = 25
        self.assertEqual(solvable(d, generate_solvable_tile_order(d)), True)

def main():
    unittest.main(verbosity=3)

main()
