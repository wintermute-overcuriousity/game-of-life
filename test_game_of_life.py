#!/usr/bin/env python3
"""
Unit tests for Conway's Game of Life implementation.
Tests cover core functionality, patterns, rulesets, and new features.
"""

import unittest
import numpy as np
from game_of_life import GameOfLife, Ruleset, pentadecathlon


class TestGameOfLife(unittest.TestCase):
    """Test cases for the GameOfLife class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.game = GameOfLife(10, 10)
    
    def test_initialization(self):
        """Test that the grid is initialized correctly."""
        self.assertEqual(self.game.width, 10)
        self.assertEqual(self.game.height, 10)
        self.assertEqual(self.game.grid.shape, (10, 10))
        self.assertTrue(np.all(self.game.grid == 0))
    
    def test_initialization_with_ruleset(self):
        """Test initialization with custom ruleset."""
        game = GameOfLife(20, 20, ruleset=Ruleset.HIGHLIFE)
        self.assertEqual(game.ruleset, Ruleset.HIGHLIFE)
    
    def test_initialization_with_wrapping(self):
        """Test initialization with wrapping enabled."""
        game = GameOfLife(20, 20, wrapping=True)
        self.assertTrue(game.wrapping)
    
    def test_set_cell(self):
        """Test setting a cell state."""
        self.game.set_cell(5, 5, 1)
        self.assertEqual(self.game.get_cell(5, 5), 1)
        
        self.game.set_cell(5, 5, 0)
        self.assertEqual(self.game.get_cell(5, 5), 0)
    
    def test_set_cell_out_of_bounds(self):
        """Test that setting out-of-bounds cells doesn't raise errors."""
        self.game.set_cell(-1, 5, 1)
        self.game.set_cell(5, -1, 1)
        self.game.set_cell(10, 5, 1)
        self.game.set_cell(5, 10, 1)
    
    def test_get_cell_out_of_bounds(self):
        """Test that getting out-of-bounds cells returns 0."""
        self.assertEqual(self.game.get_cell(-1, 5), 0)
        self.assertEqual(self.game.get_cell(5, -1), 0)
        self.assertEqual(self.game.get_cell(10, 5), 0)
        self.assertEqual(self.game.get_cell(5, 10), 0)
    
    def test_count_neighbors(self):
        """Test neighbor counting."""
        # Empty grid should have 0 neighbors
        self.assertEqual(self.game.count_neighbors(5, 5), 0)
        
        # Add a neighbor
        self.game.set_cell(5, 6, 1)
        self.assertEqual(self.game.count_neighbors(5, 5), 1)
    
    def test_count_neighbors_wrapping(self):
        """Test neighbor counting with wrapping enabled."""
        game = GameOfLife(5, 5, wrapping=True)
        game.set_cell(0, 0, 1)
        # With wrapping, cell at (4,4) should see the cell at (0,0)
        self.assertEqual(game.count_neighbors(4, 4), 1)
    
    def test_clear(self):
        """Test clearing the grid."""
        self.game.set_cell(5, 5, 1)
        self.game.clear()
        self.assertTrue(np.all(self.game.grid == 0))
        self.assertEqual(self.game.generation, 0)
    
    def test_randomize(self):
        """Test random initialization."""
        self.game.randomize(density=0.5)
        total_cells = self.game.width * self.game.height
        alive_cells = np.sum(self.game.grid)
        self.assertTrue(0 < alive_cells < total_cells)
    
    def test_add_pattern(self):
        """Test adding patterns to the grid."""
        glider = [
            [0, 1, 0],
            [0, 0, 1],
            [1, 1, 1]
        ]
        self.game.add_pattern(glider, 0, 0)
        
        self.assertEqual(self.game.get_cell(1, 0), 1)
        self.assertEqual(self.game.get_cell(2, 1), 1)
        self.assertEqual(self.game.get_cell(0, 2), 1)
    
    def test_generation_counter(self):
        """Test that generation counter increments properly."""
        self.game.set_cell(5, 4, 1)
        self.game.set_cell(6, 5, 1)
        self.game.set_cell(4, 5, 1)
        
        initial_gen = self.game.generation
        self.game.next_generation()
        self.assertEqual(self.game.generation, initial_gen + 1)
    
    def test_conways_rules(self):
        """Test Conway's rules: underpopulation, survival, overpopulation, reproduction."""
        # Underpopulation: live cell with <2 neighbors dies
        game = GameOfLife(10, 10)
        game.set_cell(5, 5, 1)
        game.next_generation()
        self.assertEqual(game.get_cell(5, 5), 0)
        
        # Survival: live cell with 2-3 neighbors survives
        game = GameOfLife(10, 10)
        game.set_cell(5, 5, 1)
        game.set_cell(5, 4, 1)
        game.set_cell(6, 5, 1)
        game.next_generation()
        self.assertEqual(game.get_cell(5, 5), 1)
        
        # Overpopulation: live cell with >3 neighbors dies
        game = GameOfLife(10, 10)
        game.set_cell(5, 5, 1)
        game.set_cell(5, 4, 1)
        game.set_cell(6, 5, 1)
        game.set_cell(6, 6, 1)
        game.set_cell(4, 5, 1)
        game.next_generation()
        self.assertEqual(game.get_cell(5, 5), 0)
        
        # Reproduction: dead cell with exactly 3 neighbors becomes alive
        game = GameOfLife(10, 10)
        game.set_cell(5, 4, 1)
        game.set_cell(6, 5, 1)
        game.set_cell(4, 5, 1)
        game.next_generation()
        self.assertEqual(game.get_cell(5, 5), 1)


class TestRulesets(unittest.TestCase):
    """Test cases for alternative rulesets."""
    
    def test_highlife_rules(self):
        """Test HighLife rules: birth with 3 or 6 neighbors."""
        # HighLife unique feature: 6 neighbors causes birth
        game = GameOfLife(10, 10, ruleset=Ruleset.HIGHLIFE)
        # Set up 6 neighbors around center (5,5)
        neighbors = [(4,4), (4,5), (4,6), (5,4), (5,6), (6,5)]
        for nx, ny in neighbors:
            game.set_cell(nx, ny, 1)
        
        # Cell at (5,5) should become alive (birth with 6 neighbors)
        game.next_generation()
        self.assertEqual(game.get_cell(5, 5), 1)
    
    def test_seeds_rules(self):
        """Test Seeds rules: birth only with 2 neighbors, no survival."""
        game = GameOfLife(10, 10, ruleset=Ruleset.SEEDS)
        # Seeds: dead cell with exactly 2 neighbors becomes alive
        game.set_cell(5, 4, 1)
        game.set_cell(6, 6, 1)
        game.next_generation()
        # Should be born (2 neighbors)
        self.assertEqual(game.get_cell(5, 5), 1)
    
    def test_ruleset_change(self):
        """Test changing ruleset dynamically."""
        game = GameOfLife(10, 10)
        game.set_ruleset(Ruleset.HIGHLIFE)
        self.assertEqual(game.ruleset, Ruleset.HIGHLIFE)
    
    def test_wrapping_toggle(self):
        """Test toggling wrapping mode."""
        game = GameOfLife(10, 10)
        self.assertFalse(game.wrapping)
        game.set_wrapping(True)
        self.assertTrue(game.wrapping)


class TestPatterns(unittest.TestCase):
    """Test cases for predefined patterns."""
    
    def test_block(self):
        """Test Block pattern (still life)."""
        game = GameOfLife(10, 10)
        game.add_pattern(GameOfLife.block(), 3, 3)
        
        self.assertEqual(game.get_cell(3, 3), 1)
        self.assertEqual(game.get_cell(4, 3), 1)
        self.assertEqual(game.get_cell(3, 4), 1)
        self.assertEqual(game.get_cell(4, 4), 1)
    
    def test_blinker(self):
        """Test Blinker pattern (oscillator)."""
        game = GameOfLife(10, 10)
        blinker = GameOfLife.blinker()
        game.add_pattern(blinker, 4, 5)
        
        # First generation - should become vertical
        game.next_generation()
        self.assertEqual(game.get_cell(5, 4), 1)
        self.assertEqual(game.get_cell(5, 5), 1)
        self.assertEqual(game.get_cell(5, 6), 1)
    
    def test_glider(self):
        """Test Glider pattern (spaceship) moves."""
        game = GameOfLife(20, 20)
        game.add_pattern(GameOfLife.glider(), 0, 0)
        
        # Run several generations - glider should move
        prev_pos = None
        moved = False
        for _ in range(20):
            game.next_generation()
            # Find any alive cell
            for y in range(game.height):
                for x in range(game.width):
                    if game.get_cell(x, y) == 1:
                        if prev_pos is not None:
                            if (x, y) != prev_pos:
                                moved = True
                        prev_pos = (x, y)
                        break
                else:
                    continue
                break
        
        self.assertTrue(moved)
    
    def test_pentadecathlon(self):
        """Test Pentadecathlon pattern exists and has correct size."""
        pd = GameOfLife.pentadecathlon()
        self.assertEqual(len(pd), 9)
        self.assertEqual(len(pd[0]), 16)
    
    # New pattern tests
    def test_gosper_glider_gun(self):
        """Test Gosper Glider Gun pattern."""
        ggg = GameOfLife.gosper_glider_gun()
        self.assertEqual(len(ggg), 9)  # 9 rows
        self.assertEqual(len(ggg[0]), 36)  # 36 columns
        
        # Check some known cells
        game = GameOfLife(40, 10)
        game.add_pattern(ggg, 0, 0)
        # Should have alive cells
        self.assertTrue(np.sum(game.grid) > 0)
    
    def test_r_pentomino(self):
        """Test R-pentomino pattern."""
        rp = GameOfLife.r_pentomino()
        self.assertEqual(len(rp), 5)
        self.assertEqual(len(rp[0]), 5)
        
        # Check it has 5 cells (pentomino)
        cells = sum(sum(row) for row in rp)
        self.assertEqual(cells, 5)
    
    def test_diehard(self):
        """Test Diehard pattern."""
        dh = GameOfLife.diehard()
        self.assertEqual(len(dh), 3)
        cells = sum(sum(row) for row in dh)
        self.assertEqual(cells, 6)
    
    def test_acorn(self):
        """Test Acorn pattern."""
        ac = GameOfLife.acorn()
        self.assertEqual(len(ac), 3)
        cells = sum(sum(row) for row in ac)
        self.assertEqual(cells, 7)
    
    def test_hwss(self):
        """Test Heavy Weight Spaceship."""
        hwss = GameOfLife.hwss()
        self.assertEqual(len(hwss), 4)
        self.assertEqual(len(hwss[0]), 7)
    
    def test_eater(self):
        """Test Eater pattern."""
        eater = GameOfLife.eater()
        self.assertEqual(len(eater), 4)
        self.assertEqual(len(eater[0]), 5)
    
    def test_pattern_cache(self):
        """Test that patterns are cached."""
        # Get patterns multiple times
        p1 = GameOfLife.glider()
        p2 = GameOfLife.glider()
        # Should be the same object (cached)
        self.assertIs(p1, p2)
    
    def test_get_all_patterns(self):
        """Test getting all patterns."""
        patterns = GameOfLife.get_all_patterns()
        self.assertIsInstance(patterns, dict)
        self.assertIn('glider', patterns)
        self.assertIn('gosper_glider_gun', patterns)
        self.assertIn('r_pentomino', patterns)
        self.assertIn('acorn', patterns)


class TestVectorizedMethod(unittest.TestCase):
    """Test the vectorized next generation method."""
    
    def test_vectorized_equivalence(self):
        """Test that vectorized produces same results as iterative."""
        # Set up a known pattern
        game1 = GameOfLife(20, 20)
        game1.set_cell(10, 9, 1)
        game1.set_cell(11, 10, 1)
        game1.set_cell(9, 11, 1)
        
        # Copy to second game
        game2 = GameOfLife(20, 20)
        game2.grid = game1.grid.copy()
        
        # Both should produce the same result
        game1.next_generation()
        game2.next_generation_vectorized()
        
        self.assertTrue(np.array_equal(game1.grid, game2.grid))


class TestWrapping(unittest.TestCase):
    """Test toroidal wrapping mode."""
    
    def test_wrapping_creates_loop(self):
        """Test that wrapping creates continuous edges."""
        game = GameOfLife(5, 5, wrapping=True)
        # Place cell at edge
        game.set_cell(0, 0, 1)
        
        # Cell should be visible from opposite edge
        neighbors = game.count_neighbors(4, 4)
        self.assertEqual(neighbors, 1)


if __name__ == '__main__':
    unittest.main()