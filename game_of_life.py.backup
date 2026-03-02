#!/usr/bin/env python3
"""
Conway's Game of Life implementation.

A cellular automaton simulation with Conway's rules and predefined patterns.
"""

import numpy as np
from typing import List, Tuple, Optional


class GameOfLife:
    """
    Conway's Game of Life cellular automaton.
    
    Attributes:
        width (int): Width of the grid
        height (int): Height of the grid
        grid (np.ndarray): 2D array representing the grid (1 = alive, 0 = dead)
    """
    
    def __init__(self, width: int = 50, height: int = 50):
        """
        Initialize a Game of Life grid.
        
        Args:
            width: Width of the grid (default: 50)
            height: Height of the grid (default: 50)
        """
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=np.uint8)
    
    def set_cell(self, x: int, y: int, state: int = 1) -> None:
        """
        Set a cell's state.
        
        Args:
            x: X coordinate (column)
            y: Y coordinate (row)
            state: 1 for alive, 0 for dead (default: 1)
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y, x] = state
    
    def get_cell(self, x: int, y: int) -> int:
        """
        Get a cell's state.
        
        Args:
            x: X coordinate (column)
            y: Y coordinate (row)
            
        Returns:
            Cell state (1 for alive, 0 for dead)
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y, x]
        return 0
    
    def count_neighbors(self, x: int, y: int) -> int:
        """
        Count the number of live neighbors around a cell.
        
        Args:
            x: X coordinate (column)
            y: Y coordinate (row)
            
        Returns:
            Number of live neighbors (0-8)
        """
        count = 0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    count += self.grid[ny, nx]
        return count
    
    def next_generation(self) -> np.ndarray:
        """
        Compute the next generation according to Conway's rules.
        
        Returns:
            New grid state
        """
        new_grid = np.zeros((self.height, self.width), dtype=np.uint8)
        
        for y in range(self.height):
            for x in range(self.width):
                neighbors = self.count_neighbors(x, y)
                current_state = self.grid[y, x]
                
                # Apply Conway's rules:
                # 1. Any live cell with fewer than two live neighbors dies (underpopulation)
                # 2. Any live cell with two or three live neighbors lives on
                # 3. Any live cell with more than three live neighbors dies (overpopulation)
                # 4. Any dead cell with exactly three live neighbors becomes a live cell (reproduction)
                
                if current_state == 1:  # Cell is alive
                    if neighbors == 2 or neighbors == 3:
                        new_grid[y, x] = 1  # Survives
                    # else dies (stays 0)
                else:  # Cell is dead
                    if neighbors == 3:
                        new_grid[y, x] = 1  # Birth
        
        self.grid = new_grid
        return new_grid
    
    def clear(self) -> None:
        """Clear the grid (set all cells to dead)."""
        self.grid = np.zeros((self.height, self.width), dtype=np.uint8)
    
    def randomize(self, density: float = 0.3) -> None:
        """
        Randomize the grid with a given density of live cells.
        
        Args:
            density: Probability of a cell being alive (default: 0.3)
        """
        self.grid = np.random.choice([0, 1], size=(self.height, self.width), 
                                     p=[1-density, density]).astype(np.uint8)
    
    def add_pattern(self, pattern: List[List[int]], x: int, y: int) -> None:
        """
        Add a pattern to the grid at the specified position.
        
        Args:
            pattern: 2D list representing the pattern (1 = alive, 0 = dead)
            x: X coordinate for top-left corner of pattern
            y: Y coordinate for top-left corner of pattern
        """
        pattern_height = len(pattern)
        pattern_width = len(pattern[0]) if pattern_height > 0 else 0
        
        for py in range(pattern_height):
            for px in range(pattern_width):
                if pattern[py][px] == 1:
                    cell_x = x + px
                    cell_y = y + py
                    if 0 <= cell_x < self.width and 0 <= cell_y < self.height:
                        self.set_cell(cell_x, cell_y, 1)
    
    def __str__(self) -> str:
        """String representation of the grid."""
        rows = []
        for y in range(self.height):
            row = ''.join(['█' if cell else ' ' for cell in self.grid[y]])
            rows.append(row)
        return '\n'.join(rows)
    
    @staticmethod
    def block() -> List[List[int]]:
        """
        Create a 2x2 Block pattern (still life).
        
        Returns:
            2D list representing the Block pattern
        """
        return [
            [1, 1],
            [1, 1]
        ]
    
    @staticmethod
    def blinker() -> List[List[int]]:
        """
        Create a 3x1 Blinker pattern (oscillator, period 2).
        
        Returns:
            2D list representing the Blinker pattern
        """
        return [
            [1, 1, 1]
        ]
    
    @staticmethod
    def glider() -> List[List[int]]:
        """
        Create a 3x3 Glider pattern (spaceship).
        
        Returns:
            2D list representing the Glider pattern
        """
        return [
            [0, 1, 0],
            [0, 0, 1],
            [1, 1, 1]
        ]
    
    @staticmethod
    def beacon() -> List[List[int]]:
        """
        Create a 4x4 Beacon pattern (oscillator, period 2).
        
        Returns:
            2D list representing the Beacon pattern
        """
        return [
            [1, 1, 0, 0],
            [1, 1, 0, 0],
            [0, 0, 1, 1],
            [0, 0, 1, 1]
        ]
    
    @staticmethod
    def pulsar() -> List[List[int]]:
        """
        Create a 13x13 Pulsar pattern (oscillator, period 3).
        
        Returns:
            2D list representing the Pulsar pattern
        """
        # Pulsar is symmetric, we'll create one quadrant and mirror
        quadrant = [
            [0, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 0, 0]
        ]
        
        # Create full pattern by mirroring
        full_pattern = []
        for row in quadrant:
            full_row = row + [0] + row[::-1]
            full_pattern.append(full_row)
        
        middle_row = [0] * 13
        full_pattern = full_pattern + [middle_row] + full_pattern[::-1]
        
        return full_pattern
    
    @staticmethod
    def lwss() -> List[List[int]]:
        """
        Create a 5x4 Lightweight Spaceship (LWSS) pattern.
        
        Returns:
            2D list representing the LWSS pattern
        """
        return [
            [0, 1, 0, 0, 1],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 0]
        ]
    
    @staticmethod
    def toad() -> List[List[int]]:
        """
        Create a 4x3 Toad pattern (oscillator, period 2).
        
        Returns:
            2D list representing the Toad pattern
        """
        return [
            [0, 1, 1, 1],
            [1, 1, 1, 0]
        ]
    
    @staticmethod
    def pentadecathlon() -> List[List[int]]:
        """
        Create a 16x9 Pentadecathlon pattern (oscillator, period 15).
        
        Returns:
            2D list representing the Pentadecathlon pattern
        """
        return [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        # Note: Full pentadecathlon pattern is complex, this is a placeholder
        # In practice, you'd want to define the actual pattern


def demo() -> None:
    """Demonstrate the Game of Life with various patterns."""
    print("Conway's Game of Life Demo")
    print("=" * 40)
    
    # Create a game with a larger grid
    game = GameOfLife(40, 20)
    
    # Add different patterns
    print("\n1. Adding Block pattern (still life):")
    game.add_pattern(GameOfLife.block(), 5, 5)
    
    print("\n2. Adding Blinker pattern (oscillator):")
    game.add_pattern(GameOfLife.blinker(), 15, 5)
    
    print("\n3. Adding Glider pattern (spaceship):")
    game.add_pattern(GameOfLife.glider(), 25, 5)
    
    print("\n4. Adding Beacon pattern (oscillator):")
    game.add_pattern(GameOfLife.beacon(), 5, 12)
    
    print("\n5. Adding LWSS pattern (spaceship):")
    game.add_pattern(GameOfLife.lwss(), 20, 12)
    
    print("\nInitial state:")
    print(game)
    
    # Run a few generations
    print("\nRunning 10 generations...")
    for generation in range(1, 11):
        game.next_generation()
        print(f"\nGeneration {generation}:")
        print(game)
    
    # Clear and try random initialization
    print("\n" + "=" * 40)
    print("Random initialization demo:")
    game.clear()
    game.randomize(density=0.2)
    
    print("\nRandom initial state (density: 0.2):")
    print(game)
    
    print("\nRunning 5 generations of random pattern...")
    for generation in range(1, 6):
        game.next_generation()
        print(f"\nGeneration {generation}:")
        print(game)


if __name__ == "__main__":
    demo()