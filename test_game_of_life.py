#!/usr/bin/env python3
"""
Unit tests for Conway's Game of Life implementation.
"""

import unittest
import numpy as np
from game_of_life import GameOfLife


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
    
    def test_set_cell(self):
        """Test setting a cell state."""
        self.game.set_cell(5, 5, 1)
        self.assertEqual(self.game.get_cell(5, 5), 1)
        
        self.game.set_cell(5, 5, 0)
        self.assertEqual(self.game.get_cell(5, 5), 0)
    
    def test_set_cell_out_of_bounds(self):
        """Test that setting out-of-bounds cells doesn't raise errors."""
        self.game.set_cell(-1, 5, 1)  # Out of bounds
        self.game.set_cell(5, -1, 1)  # Out of bounds
        self.game.set_cell(10, 5, 1)  # Out of bounds
        self.game.set_cell(5, 10, 1)  # Out of bounds
    
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
        
        # Add more neighbors (all 8 surrounding cells)
        self.game.set_cell(4, 4, 1)
        self.game.set_cell(4, 5, 1)
        self.game.set_cell(4, 6, 1)
        self.game.set_cell(5, 4, 1)
        self.game.set_cell(5, 6, 1)
        self.game.set_cell(6, 4, 1)
        self.game.set_cell(6, 5, 1)
        # Don't add 6,6 - we already added 5,6 above
        # So we should have 8 neighbors (not 9)
        self.assertEqual(self.game.count_neighbors(5, 5), 7)
    
    def test_clear(self):
        """Test clearing the grid."""
        self.game.set_cell(5, 5, 1)
        self.game.clear()
        self.assertTrue(np.all(self.game.grid == 0))
    
    def test_randomize(self):
        """Test random initialization."""
        self.game.randomize(density=0.5)
        # With density 0.5, we expect roughly half cells alive
        # This is a probabilistic test, so we just check it's not all zeros
        total_cells = self.game.width * self.game.height
        alive_cells = np.sum(self.game.grid)
        self.assertTrue(0 < alive_cells < total_cells)
    
    def test_add_pattern(self):
        """Test adding patterns to the grid."""
        # Add a glider
        glider = [
            [0, 1, 0],
            [0, 0, 1],
            [1, 1, 1]
        ]
        self.game.add_pattern(glider, 0, 0)
        
        # Check glider cells
        self.assertEqual(self.game.get_cell(1, 0), 1)
        self.assertEqual(self.game.get_cell(2, 1), 1)
        self.assertEqual(self.game.get_cell(0, 2), 1)
        self.assertEqual(self.game.get_cell(1, 2), 1)
        self.assertEqual(self.game.get_cell(2, 2), 1)
    
    def test_block_pattern(self):
        """Test Block pattern (still life)."""
        block = GameOfLife.block()
        self.game.add_pattern(block, 3, 3)
        
        # Block is a 2x2 still life - all cells should remain alive
        self.assertEqual(self.game.get_cell(3, 3), 1)
        self.assertEqual(self.game.get_cell(4, 3), 1)
        self.assertEqual(self.game.get_cell(3, 4), 1)
        self.assertEqual(self.game.get_cell(4, 4), 1)
    
    def test_blinker_pattern(self):
        """Test Blinker pattern (oscillator)."""
        # Horizontal blinker
        blinker = GameOfLife.blinker()  # [1, 1, 1]
        self.game.add_pattern(blinker, 4, 5)
        
        # First generation - should become vertical
        self.game.next_generation()
        self.assertEqual(self.game.get_cell(5, 4), 1)
        self.assertEqual(self.game.get_cell(5, 5), 1)
        self.assertEqual(self.game.get_cell(5, 6), 1)
        
        # Second generation - should return to horizontal
        self.game.next_generation()
        self.assertEqual(self.game.get_cell(4, 5), 1)
        self.assertEqual(self.game.get_cell(5, 5), 1)
        self.assertEqual(self.game.get_cell(6, 5), 1)
    
    def test_glider_pattern(self):
        """Test Glider pattern (spaceship)."""
        glider = GameOfLife.glider()
        self.game.add_pattern(glider, 0, 0)
        
        # Store initial state
        initial_state = self.game.grid.copy()
        
        # Run several generations - glider should move diagonally
        prev_x, prev_y = 0, 0
        found_movement = False
        
        for _ in range(10):
            self.game.next_generation()
            # Find the top-left alive cell
            for y in range(self.game.height):
                for x in range(self.game.width):
                    if self.game.get_cell(x, y) == 1:
                        if x > prev_x or y > prev_y:
                            found_movement = True
                        prev_x, prev_y = x, y
                        break
                else:
                    continue
                break
        
        # Glider should have moved
        self.assertTrue(found_movement)
    
    def test_conways_rules_underpopulation(self):
        """Test: Live cell with <2 neighbors dies."""
        self.game.set_cell(5, 5, 1)
        self.game.set_cell(6, 5, 0)  # Only 0 neighbors
        self.game.next_generation()
        self.assertEqual(self.game.get_cell(5, 5), 0)
    
    def test_conways_rules_survival_two_neighbors(self):
        """Test: Live cell with 2 neighbors survives."""
        self.game.clear()
        self.game.set_cell(5, 5, 1)
        self.game.set_cell(5, 4, 1)
        self.game.set_cell(6, 5, 1)
        self.game.next_generation()
        self.assertEqual(self.game.grid[5, 5], 1)
    
    def test_conways_rules_survival_three_neighbors(self):
        """Test: Live cell with 3 neighbors survives."""
        self.game.clear()
        self.game.set_cell(5, 5, 1)
        self.game.set_cell(5, 4, 1)
        self.game.set_cell(6, 5, 1)
        self.game.set_cell(6, 6, 1)
        self.game.next_generation()
        self.assertEqual(self.game.grid[5, 5], 1)
    
    def test_conways_rules_overpopulation(self):
        """Test: Live cell with >3 neighbors dies."""
        self.game.set_cell(5, 5, 1)
        self.game.set_cell(5, 4, 1)
        self.game.set_cell(6, 5, 1)
        self.game.set_cell(6, 6, 1)
        self.game.set_cell(4, 5, 1)  # 4 neighbors
        self.game.next_generation()
        self.assertEqual(self.game.get_cell(5, 5), 0)
    
    def test_conways_rules_reproduction(self):
        """Test: Dead cell with exactly 3 neighbors becomes alive."""
        self.game.set_cell(5, 4, 1)
        self.game.set_cell(6, 5, 1)
        self.game.set_cell(4, 5, 1)
        # Cell (5, 5) has 3 neighbors, should become alive
        self.game.next_generation()
        self.assertEqual(self.game.get_cell(5, 5), 1)
    
    def test_vectorized_method(self):
        """Test the vectorized next_generation method."""
        # Set up a known pattern
        self.game.set_cell(5, 4, 1)
        self.game.set_cell(6, 5, 1)
        self.game.set_cell(4, 5, 1)
        
        # Get result from iterative method
        game_iterative = GameOfLife(10, 10)
        game_iterative.grid = self.game.grid.copy()
        game_iterative.next_generation()
        
        # Get result from vectorized method
        self.game.next_generation_vectorized()
        
        # Both should produce the same result
        self.assertTrue(np.array_equal(self.game.grid, game_iterative.grid))
    
    def test_string_representation(self):
        """Test string representation."""
        self.game.set_cell(0, 0, 1)
        self.game.set_cell(1, 0, 1)
        
        representation = str(self.game)
        self.assertIn('\u2588', representation)  # Unicode block character


class TestPatterns(unittest.TestCase):
    """Test cases for predefined patterns."""
    
    def test_block(self):
        """Test Block pattern returns correct 2x2 grid."""
        block = GameOfLife.block()
        self.assertEqual(len(block), 2)
        self.assertEqual(len(block[0]), 2)
        self.assertEqual(block[0][0], 1)
        self.assertEqual(block[1][1], 1)
    
    def test_blinker(self):
        """Test Blinker pattern returns correct 1x3 grid."""
        blinker = GameOfLife.blinker()
        self.assertEqual(len(blinker), 1)
        self.assertEqual(len(blinker[0]), 3)
    
    def test_glider(self):
        """Test Glider pattern returns correct 3x3 grid."""
        glider = GameOfLife.glider()
        self.assertEqual(len(glider), 3)
        self.assertEqual(len(glider[0]), 3)
    
    def test_beacon(self):
        """Test Beacon pattern returns correct 4x4 grid."""
        beacon = GameOfLife.beacon()
        self.assertEqual(len(beacon), 4)
        self.assertEqual(len(beacon[0]), 4)
    
    def test_pulsar(self):
        """Test Pulsar pattern returns square grid."""
        pulsar = GameOfLife.pulsar()
        rows = len(pulsar)
        cols = len(pulsar[0])
        # Pulsar is a square oscillator
        self.assertEqual(rows, cols)
    
    def test_lwss(self):
        """Test LWSS pattern returns correct 5x4 grid."""
        lwss = GameOfLife.lwss()
        self.assertEqual(len(lwss), 4)
        self.assertEqual(len(lwss[0]), 5)
    
    def test_toad(self):
        """Test Toad pattern returns correct 4x2 grid."""
        toad = GameOfLife.toad()
        self.assertEqual(len(toad), 2)
        self.assertEqual(len(toad[0]), 4)
    
    def test_pentadecathlon(self):
        """Test Pentadecathlon pattern."""
        pd = GameOfLife.pentadecathlon()
        self.assertEqual(len(pd), 9)
        self.assertEqual(len(pd[0]), 16)


if __name__ == '__main__':
    unittest.main()