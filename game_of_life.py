#!/usr/bin/env python3
"""
Conway's Game of Life implementation.

A cellular automaton simulation with configurable rules and predefined patterns.
Supports multiple rulesets including Conway's Life, HighLife, Seeds, and Day & Night.
"""

import numpy as np
from typing import List, Tuple, Optional, Dict, Callable, Any
from enum import Enum


class Ruleset(Enum):
    """Enumeration of supported cellular automaton rulesets."""
    CONWAY = "conway"
    HIGHLIFE = "highlife"
    SEEDS = "seeds"
    DAY_NIGHT = "day_night"
    LIFE_WITHOUT_DEATH = "life_without_death"


class GameOfLife:
    """
    Conway's Game of Life cellular automaton.
    
    Attributes:
        width (int): Width of the grid
        height (int): Height of the grid
        grid (np.ndarray): 2D array representing the grid (1 = alive, 0 = dead)
        ruleset (Ruleset): Current ruleset being used
        wrapping (bool): Whether grid edges wrap around (toroidal mode)
    """
    
    # Class-level pattern cache to avoid recreating patterns
    _pattern_cache: Dict[str, List[List[int]]] = {}
    
    # Ruleset definitions: (birth_conditions, survival_conditions)
    # Each is a tuple of neighbor counts that trigger the event
    RULES: Dict[Ruleset, Tuple[Tuple[int, ...], Tuple[int, ...]]] = {
        Ruleset.CONWAY: ((3,), (2, 3)),
        Ruleset.HIGHLIFE: ((3, 6), (2, 3)),
        Ruleset.SEEDS: ((2,), ()),
        Ruleset.DAY_NIGHT: ((3, 6, 7, 8), (3, 4, 6, 7, 8)),
        Ruleset.LIFE_WITHOUT_DEATH: ((3,), tuple(range(9))),
    }
    
    def __init__(
        self, 
        width: int = 50, 
        height: int = 50,
        ruleset: Ruleset = Ruleset.CONWAY,
        wrapping: bool = False
    ) -> None:
        """
        Initialize a Game of Life grid.
        
        Args:
            width: Width of the grid (default: 50)
            height: Height of the grid (default: 50)
            ruleset: Ruleset to use (default: Ruleset.CONWAY)
            wrapping: Whether to wrap edges (default: False)
        """
        self.width = width
        self.height = height
        self.ruleset = ruleset
        self.wrapping = wrapping
        self.grid = np.zeros((height, width), dtype=np.uint8)
        self._generation = 0
    
    @property
    def generation(self) -> int:
        """Get current generation number."""
        return self._generation
    
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
    
    def _get_wrapped_coords(self, x: int, y: int) -> Tuple[int, int]:
        """Get wrapped coordinates for toroidal mode."""
        if self.wrapping:
            return (x % self.width, y % self.height)
        return (x, y)
    
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
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                
                if self.wrapping:
                    nx = nx % self.width
                    ny = ny % self.height
                    count += self.grid[ny, nx]
                elif 0 <= nx < self.width and 0 <= ny < self.height:
                    count += self.grid[ny, nx]
        return count
    
    def _get_neighbors_array(self) -> np.ndarray:
        """
        Get an array of neighbor counts for all cells.
        
        Returns:
            2D array of neighbor counts
        """
        if self.wrapping:
            # For wrapping mode, use roll operations
            return (
                np.roll(self.grid, 1, axis=0) +  # up
                np.roll(self.grid, -1, axis=0) +  # down
                np.roll(self.grid, 1, axis=1) +  # left
                np.roll(self.grid, -1, axis=1) +  # right
                np.roll(np.roll(self.grid, 1, axis=0), 1, axis=1) +  # up-left
                np.roll(np.roll(self.grid, 1, axis=0), -1, axis=1) +  # up-right
                np.roll(np.roll(self.grid, -1, axis=0), 1, axis=1) +  # down-left
                np.roll(np.roll(self.grid, -1, axis=0), -1, axis=1)  # down-right
            )
        else:
            # Non-wrapping mode with padding
            padded = np.pad(self.grid, pad_width=1, mode='constant', constant_values=0)
            return (
                padded[0:-2, 0:-2] +  # top-left
                padded[0:-2, 1:-1] +  # top
                padded[0:-2, 2:] +    # top-right
                padded[1:-1, 0:-2] +  # left
                padded[1:-1, 2:] +    # right
                padded[2:, 0:-2] +    # bottom-left
                padded[2:, 1:-1] +    # bottom
                padded[2:, 2:]        # bottom-right
            )
    
    def next_generation(self) -> np.ndarray:
        """
        Compute the next generation according to current ruleset.
        
        Returns:
            New grid state
        """
        birth_cond, survival_cond = self.RULES[self.ruleset]
        neighbors = self._get_neighbors_array()
        
        # Convert conditions to sets for O(1) lookup
        birth_set = set(birth_cond)
        survival_set = set(survival_cond)
        
        # Apply rules using vectorized operations
        live_cells = self.grid == 1
        dead_cells = self.grid == 0
        
        # Vectorized condition checking
        survive = live_cells & np.isin(neighbors, list(survival_set))
        birth = dead_cells & np.isin(neighbors, list(birth_set))
        
        self.grid = (survive | birth).astype(np.uint8)
        self._generation += 1
        return self.grid
    
    def next_generation_vectorized(self) -> np.ndarray:
        """
        Compute the next generation using NumPy vectorization.
        Alias for next_generation() for backwards compatibility.
        
        Returns:
            New grid state
        """
        return self.next_generation()
    
    def set_ruleset(self, ruleset: Ruleset) -> None:
        """
        Change the ruleset.
        
        Args:
            ruleset: New ruleset to use
        """
        self.ruleset = ruleset
    
    def set_wrapping(self, wrapping: bool) -> None:
        """
        Toggle grid wrapping (toroidal mode).
        
        Args:
            wrapping: Whether to wrap edges
        """
        self.wrapping = wrapping
    
    def clear(self) -> None:
        """Clear the grid (set all cells to dead) and reset generation counter."""
        self.grid = np.zeros((self.height, self.width), dtype=np.uint8)
        self._generation = 0
    
    def randomize(self, density: float = 0.3) -> None:
        """
        Randomize the grid with a given density of live cells.
        
        Args:
            density: Probability of a cell being alive (default: 0.3)
        """
        self.grid = np.random.choice(
            [0, 1], 
            size=(self.height, self.width),
            p=[1 - density, density]
        ).astype(np.uint8)
        self._generation = 0
    
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
            row = ''.join(['\u2588' if cell else ' ' for cell in self.grid[y]])
            rows.append(row)
        return '\n'.join(rows)
    
    # =========================================================================
    # Pattern Definitions - Cached for performance
    # =========================================================================
    
    @classmethod
    def block(cls) -> List[List[int]]:
        """Create a 2x2 Block pattern (still life)."""
        if 'block' not in cls._pattern_cache:
            cls._pattern_cache['block'] = [[1, 1], [1, 1]]
        return cls._pattern_cache['block']
    
    @classmethod
    def blinker(cls) -> List[List[int]]:
        """Create a 3x1 Blinker pattern (oscillator, period 2)."""
        if 'blinker' not in cls._pattern_cache:
            cls._pattern_cache['blinker'] = [[1, 1, 1]]
        return cls._pattern_cache['blinker']
    
    @classmethod
    def glider(cls) -> List[List[int]]:
        """Create a 3x3 Glider pattern (spaceship)."""
        if 'glider' not in cls._pattern_cache:
            cls._pattern_cache['glider'] = [
                [0, 1, 0],
                [0, 0, 1],
                [1, 1, 1]
            ]
        return cls._pattern_cache['glider']
    
    @classmethod
    def beacon(cls) -> List[List[int]]:
        """Create a 4x4 Beacon pattern (oscillator, period 2)."""
        if 'beacon' not in cls._pattern_cache:
            cls._pattern_cache['beacon'] = [
                [1, 1, 0, 0],
                [1, 1, 0, 0],
                [0, 0, 1, 1],
                [0, 0, 1, 1]
            ]
        return cls._pattern_cache['beacon']
    
    @classmethod
    def pulsar(cls) -> List[List[int]]:
        """Create a 13x13 Pulsar pattern (oscillator, period 3)."""
        if 'pulsar' not in cls._pattern_cache:
            quadrant = [
                [0, 0, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0]
            ]
            full_pattern = []
            for row in quadrant:
                full_row = row + [0] + row[::-1]
                full_pattern.append(full_row)
            middle_row = [0] * 13
            full_pattern = full_pattern + [middle_row] + full_pattern[::-1]
            cls._pattern_cache['pulsar'] = full_pattern
        return cls._pattern_cache['pulsar']
    
    @classmethod
    def lwss(cls) -> List[List[int]]:
        """Create a 5x4 Lightweight Spaceship (LWSS) pattern."""
        if 'lwss' not in cls._pattern_cache:
            cls._pattern_cache['lwss'] = [
                [0, 1, 0, 0, 1],
                [1, 0, 0, 0, 0],
                [1, 0, 0, 0, 1],
                [1, 1, 1, 1, 0]
            ]
        return cls._pattern_cache['lwss']
    
    @classmethod
    def toad(cls) -> List[List[int]]:
        """Create a 4x3 Toad pattern (oscillator, period 2)."""
        if 'toad' not in cls._pattern_cache:
            cls._pattern_cache['toad'] = [
                [0, 1, 1, 1],
                [1, 1, 1, 0]
            ]
        return cls._pattern_cache['toad']
    
    @classmethod
    def pentadecathlon(cls) -> List[List[int]]:
        """Create a 16x9 Pentadecathlon pattern (oscillator, period 15)."""
        if 'pentadecathlon' not in cls._pattern_cache:
            cls._pattern_cache['pentadecathlon'] = [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]
        return cls._pattern_cache['pentadecathlon']
    
    # =========================================================================
    # NEW PATTERNS - Added as improvements
    # =========================================================================
    
    @classmethod
    def gosper_glider_gun(cls) -> List[List[int]]:
        """Create the Gosper Glider Gun (36x9) - produces infinite gliders."""
        if 'gosper_glider_gun' not in cls._pattern_cache:
            cls._pattern_cache['gosper_glider_gun'] = [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]
        return cls._pattern_cache['gosper_glider_gun']
    
    @classmethod
    def r_pentomino(cls) -> List[List[int]]:
        """Create the R-pentomino (5x5) - famous methuselah with 2336 generation lifespan."""
        if 'r_pentomino' not in cls._pattern_cache:
            cls._pattern_cache['r_pentomino'] = [
                [0, 1, 1, 0, 0],
                [1, 1, 0, 0, 0],
                [0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0]
            ]
        return cls._pattern_cache['r_pentomino']
    
    @classmethod
    def diehard(cls) -> List[List[int]]:
        """Create Diehard pattern (7x3) - methuselah that dies after 130 generations."""
        if 'diehard' not in cls._pattern_cache:
            cls._pattern_cache['diehard'] = [
                [0, 0, 0, 0, 0, 0, 1],
                [1, 1, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 1, 1]
            ]
        return cls._pattern_cache['diehard']
    
    @classmethod
    def acorn(cls) -> List[List[int]]:
        """Create Acorn pattern (7x3) - methuselah that takes 5206 generations to stabilize."""
        if 'acorn' not in cls._pattern_cache:
            cls._pattern_cache['acorn'] = [
                [0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0],
                [1, 1, 0, 0, 1, 1, 1]
            ]
        return cls._pattern_cache['acorn']
    
    @classmethod
    def hwss(cls) -> List[List[int]]:
        """Create Heavy Weight Spaceship (7x4)."""
        if 'hwss' not in cls._pattern_cache:
            cls._pattern_cache['hwss'] = [
                [0, 0, 1, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 0]
            ]
        return cls._pattern_cache['hwss']
    
    @classmethod
    def eater(cls) -> List[List[int]]:
        """Create Eater pattern (5x4) - pattern that absorbs gliders."""
        if 'eater' not in cls._pattern_cache:
            cls._pattern_cache['eater'] = [
                [0, 1, 1, 0, 0],
                [1, 1, 0, 1, 0],
                [0, 0, 0, 1, 0],
                [0, 0, 0, 1, 1]
            ]
        return cls._pattern_cache['eater']
    
    @classmethod
    def infinite_growth(cls) -> List[List[int]]:
        """Create Infinite Growth pattern (9x5) - pattern that grows indefinitely."""
        if 'infinite_growth' not in cls._pattern_cache:
            cls._pattern_cache['infinite_growth'] = [
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 1, 1, 1, 0, 0, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]
        return cls._pattern_cache['infinite_growth']
    
    @classmethod
    def get_all_patterns(cls) -> Dict[str, Callable[[], List[List[int]]]]:
        """Get all available patterns as a dictionary."""
        return {
            'block': cls.block,
            'blinker': cls.blinker,
            'glider': cls.glider,
            'beacon': cls.beacon,
            'pulsar': cls.pulsar,
            'lwss': cls.lwss,
            'toad': cls.toad,
            'pentadecathlon': cls.pentadecathlon,
            # New patterns
            'gosper_glider_gun': cls.gosper_glider_gun,
            'r_pentomino': cls.r_pentomino,
            'diehard': cls.diehard,
            'acorn': cls.acorn,
            'hwss': cls.hwss,
            'eater': cls.eater,
            'infinite_growth': cls.infinite_growth,
        }


# Standalone function for backwards compatibility
def pentadecathlon() -> List[List[int]]:
    """Create a proper 16x9 Pentadecathlon pattern (oscillator, period 15)."""
    return GameOfLife.pentadecathlon()


import pygame
import sys
from typing import Tuple, Optional
import time


class ColorTheme:
    """Color theme for the Game of Life GUI."""
    
    def __init__(
        self, 
        name: str,
        background: Tuple[int, int, int],
        grid: Tuple[int, int, int],
        cell_alive: Tuple[int, int, int],
        cell_dead: Tuple[int, int, int],
        text: Tuple[int, int, int],
        highlight: Tuple[int, int, int]
    ) -> None:
        self.name = name
        self.BACKGROUND = background
        self.GRID_COLOR = grid
        self.CELL_ALIVE = cell_alive
        self.CELL_DEAD = cell_dead
        self.TEXT_COLOR = text
        self.HIGHLIGHT_COLOR = highlight


# Predefined themes
THEMES = {
    'dark': ColorTheme(
        'Dark',
        (20, 20, 30),
        (40, 40, 60),
        (100, 200, 100),
        (30, 30, 40),
        (220, 220, 220),
        (255, 255, 200)
    ),
    'matrix': ColorTheme(
        'Matrix',
        (0, 0, 0),
        (0, 20, 0),
        (0, 255, 0),
        (0, 10, 0),
        (0, 255, 0),
        (200, 255, 200)
    ),
    'classic': ColorTheme(
        'Classic',
        (255, 255, 255),
        (200, 200, 200),
        (0, 0, 0),
        (255, 255, 255),
        (0, 0, 0),
        (100, 100, 100)
    ),
    'ocean': ColorTheme(
        'Ocean',
        (10, 20, 40),
        (30, 50, 80),
        (100, 180, 220),
        (20, 40, 60),
        (200, 220, 240),
        (150, 200, 255)
    ),
    'sunset': ColorTheme(
        'Sunset',
        (30, 10, 20),
        (60, 30, 40),
        (255, 150, 100),
        (40, 20, 30),
        (255, 220, 200),
        (255, 200, 150)
    ),
}


class GameOfLifeGUI:
    """PyGame GUI for Conway's Game of Life."""
    
    def __init__(
        self, 
        width: int = 800, 
        height: int = 600, 
        cell_size: int = 15
    ) -> None:
        """
        Initialize the PyGame GUI.
        
        Args:
            width: Window width in pixels (default: 800)
            height: Window height in pixels (default: 600)
            cell_size: Size of each cell in pixels (default: 15)
        """
        pygame.init()
        
        self.width = width
        self.height = height
        self.cell_size = cell_size
        
        # Calculate grid dimensions based on cell size
        self.grid_width = width // cell_size
        self.grid_height = height // cell_size
        
        # Create the game instance with new features
        self.game = GameOfLife(
            self.grid_width, 
            self.grid_height,
            ruleset=Ruleset.CONWAY,
            wrapping=False
        )
        
        # Create the screen
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Conway's Game of Life")
        
        # Theme support
        self.current_theme = 'dark'
        self.theme = THEMES[self.current_theme]
        
        # Font
        self.font = pygame.font.SysFont('Arial', 20)
        self.small_font = pygame.font.SysFont('Arial', 16)
        
        # Game state
        self.running = False
        self.generation = 0
        self.speed = 10  # Updates per second
        self.last_update = 0
        self.dragging = False
        self.draw_mode = 1  # 1 for alive, 0 for dead
        
        # Pattern selection - now includes new patterns
        self.patterns = GameOfLife.get_all_patterns()
        self.current_pattern = 'glider'
        
        # Ruleset selection
        self.rulesets = {
            'conway': Ruleset.CONWAY,
            'highlife': Ruleset.HIGHLIFE,
            'seeds': Ruleset.SEEDS,
            'day_night': Ruleset.DAY_NIGHT,
            'life_no_death': Ruleset.LIFE_WITHOUT_DEATH,
        }
        self.current_ruleset = 'conway'
        
        # New: Step mode
        self.step_mode = False
        
        # New: Theme index for cycling
        self.theme_names = list(THEMES.keys())
    
    def _apply_colors(self) -> None:
        """Apply current theme colors to GUI."""
        colors = ['BACKGROUND', 'GRID_COLOR', 'CELL_ALIVE', 'CELL_DEAD', 
                  'TEXT_COLOR', 'HIGHLIGHT_COLOR']
        for color in colors:
            setattr(self, color, getattr(self.theme, color))
    
    def handle_events(self) -> bool:
        """Handle PyGame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                # Space: Play/Pause
                if event.key == pygame.K_SPACE:
                    self.running = not self.running
                
                # Enter: Step (when paused)
                elif event.key == pygame.K_RETURN:
                    if not self.running:
                        self.game.next_generation()
                        self.generation = self.game.generation
                
                # R: Reset (clear grid)
                elif event.key == pygame.K_r:
                    self.game.clear()
                    self.generation = 0
                
                # C: Clear grid
                elif event.key == pygame.K_c:
                    self.game.clear()
                    self.generation = 0
                
                # +/- or [/]: Adjust speed
                elif event.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_RIGHTBRACKET):
                    self.speed = min(60, self.speed + 2)
                elif event.key in (pygame.K_MINUS, pygame.K_LEFTBRACKET):
                    self.speed = max(1, self.speed - 2)
                
                # W: Toggle wrapping (toroidal mode)
                elif event.key == pygame.K_w:
                    self.game.wrapping = not self.game.wrapping
                
                # T: Cycle through themes
                elif event.key == pygame.K_t:
                    idx = (self.theme_names.index(self.current_theme) + 1) % len(self.theme_names)
                    self.current_theme = self.theme_names[idx]
                    self.theme = THEMES[self.current_theme]
                    self._apply_colors()
                
                # 1-9, 0: Select patterns
                pattern_keys = list(self.patterns.keys())
                key_map = {
                    pygame.K_1: 0, pygame.K_2: 1, pygame.K_3: 2, pygame.K_4: 3,
                    pygame.K_5: 4, pygame.K_6: 5, pygame.K_7: 6, pygame.K_8: 7,
                    pygame.K_9: 8, pygame.K_0: 9
                }
                if event.key in key_map and key_map[event.key] < len(pattern_keys):
                    self.current_pattern = pattern_keys[key_map[event.key]]
                
                # J/K: Cycle rulesets
                elif event.key == pygame.K_j:
                    ruleset_list = list(self.rulesets.keys())
                    idx = (ruleset_list.index(self.current_ruleset) + 1) % len(ruleset_list)
                    self.current_ruleset = ruleset_list[idx]
                    self.game.set_ruleset(self.rulesets[self.current_ruleset])
                elif event.key == pygame.K_k:
                    ruleset_list = list(self.rulesets.keys())
                    idx = (ruleset_list.index(self.current_ruleset) - 1) % len(ruleset_list)
                    self.current_ruleset = ruleset_list[idx]
                    self.game.set_ruleset(self.rulesets[self.current_ruleset])
                
                # D: Toggle draw mode (alive/dead)
                elif event.key == pygame.K_d:
                    self.draw_mode = 1 if self.draw_mode == 0 else 0
                
                # F: Fill random
                elif event.key == pygame.K_f:
                    self.game.randomize(0.3)
                    self.generation = 0
                
                # G: Toggle grid
                elif event.key == pygame.K_g:
                    self.show_grid = not self.show_grid if hasattr(self, 'show_grid') else False
                
                # ESC: Quit
                elif event.key == pygame.K_ESCAPE:
                    return False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.dragging = True
                    self.handle_click(event.pos)
                elif event.button == 3:  # Right click
                    # Place current pattern
                    x, y = self.screen_to_grid(event.pos)
                    pattern_func = self.patterns.get(self.current_pattern)
                    if pattern_func:
                        pattern = pattern_func()
                        self.game.add_pattern(pattern, x, y)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging = False
            
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging:
                    self.handle_click(event.pos)
        
        return True
    
    def handle_click(self, pos: Tuple[int, int]) -> None:
        """Handle mouse click at position."""
        x, y = self.screen_to_grid(pos)
        if 0 <= x < self.grid_width and 0 <= y < self.grid_height:
            if self.draw_mode == 1:
                self.game.set_cell(x, y, 1)
            else:
                self.game.set_cell(x, y, 0)
    
    def screen_to_grid(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        """Convert screen coordinates to grid coordinates."""
        x, y = pos
        grid_x = x // self.cell_size
        grid_y = y // self.cell_size
        return grid_x, grid_y
    
    def update(self) -> None:
        """Update game state if running."""
        if not self.running:
            return
        
        current_time = time.time()
        if current_time - self.last_update > 1.0 / self.speed:
            self.game.next_generation()
            self.generation = self.game.generation
            self.last_update = current_time
    
    def draw(self) -> None:
        """Draw everything to the screen."""
        # Clear screen
        self.screen.fill(self.BACKGROUND)
        
        # Draw grid lines
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(
                self.screen, self.GRID_COLOR,
                (x, 0), (x, self.height), 1
            )
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(
                self.screen, self.GRID_COLOR,
                (0, y), (self.width, y), 1
            )
        
        # Draw cells
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if self.game.get_cell(x, y) == 1:
                    rect = pygame.Rect(
                        x * self.cell_size + 1,
                        y * self.cell_size + 1,
                        self.cell_size - 2,
                        self.cell_size - 2
                    )
                    pygame.draw.rect(self.screen, self.CELL_ALIVE, rect)
                    pygame.draw.rect(self.screen, self.HIGHLIGHT_COLOR, rect, 1)
        
        # Draw UI text
        self.draw_ui()
        
        # Update display
        pygame.display.flip()
    
    def draw_ui(self) -> None:
        """Draw UI elements and text."""
        # Status
        status = "RUNNING" if self.running else "PAUSED"
        status_color = (100, 255, 100) if self.running else (255, 100, 100)
        
        # Calculate population
        population = int(np.sum(self.game.grid))
        
        ruleset_display = {
            'conway': 'Conway',
            'highlife': 'HighLife',
            'seeds': 'Seeds',
            'day_night': 'Day&Night',
            'life_no_death': 'NoDeath'
        }
        
        texts = [
            f"Generation: {self.generation}",
            f"Population: {population}",
            f"Status: {status}",
            f"Speed: {self.speed} FPS",
            f"Grid: {self.grid_width}x{self.grid_height}",
            f"Pattern: {self.current_pattern}",
            f"Ruleset: {ruleset_display.get(self.current_ruleset, self.current_ruleset)}",
            f"Wrapping: {'ON' if self.game.wrapping else 'OFF'}",
            f"Theme: {self.theme.name}",
            f"Draw: {'ALIVE' if self.draw_mode == 1 else 'DEAD'}"
        ]
        
        # Draw text background
        pygame.draw.rect(
            self.screen, (30, 30, 45, 230),
            (10, 10, 280, 300), border_radius=8
        )
        pygame.draw.rect(
            self.screen, (60, 60, 80),
            (10, 10, 280, 300), 2, border_radius=8
        )
        
        # Draw texts
        for i, text in enumerate(texts):
            color = status_color if i == 2 else self.TEXT_COLOR
            text_surface = self.font.render(text, True, color)
            self.screen.blit(text_surface, (20, 20 + i * 28))
        
        # Controls help
        controls = [
            "CONTROLS:",
            "SPACE: Play/Pause",
            "ENTER: Step (when paused)",
            "R: Reset grid",
            "C: Clear grid",
            "+/-: Adjust speed",
            "W: Toggle wrapping",
            "T: Cycle theme",
            "J/K: Cycle ruleset",
            "D: Toggle draw mode",
            "F: Fill random",
            "L-click: Draw cells",
            "R-click: Place pattern",
            "ESC: Quit"
        ]
        
        # Draw controls background
        pygame.draw.rect(
            self.screen, (30, 30, 45, 230),
            (self.width - 320, 10, 310, 420), border_radius=8
        )
        pygame.draw.rect(
            self.screen, (60, 60, 80),
            (self.width - 320, 10, 310, 420), 2, border_radius=8
        )
        
        # Draw controls
        for i, text in enumerate(controls):
            color = (255, 255, 200) if i == 0 else self.TEXT_COLOR
            font = self.font if i == 0 else self.small_font
            text_surface = font.render(text, True, color)
            self.screen.blit(text_surface, (self.width - 310, 20 + i * 28))
    
    def run(self) -> None:
        """Main game loop."""
        clock = pygame.time.Clock()
        
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            clock.tick(60)  # Cap at 60 FPS
        
        pygame.quit()


def gui_main() -> None:
    """Main function to run the GUI."""
    print("Starting Conway's Game of Life GUI...")
    print("Features: Multiple rulesets, patterns, themes, wrapping mode")
    print()
    print("Controls:")
    print("  SPACE: Play/Pause  |  ENTER: Step  |  R: Reset  |  C: Clear")
    print("  +/-: Speed  |  W: Wrapping  |  T: Theme  |  J/K: Rulesets")
    print("  1-0: Patterns  |  D: Draw mode  |  F: Random fill")
    print("  L-click: Draw  |  R-click: Place pattern  |  ESC: Quit")
    print()
    
    gui = GameOfLifeGUI(width=1000, height=700, cell_size=15)
    gui.run()


def demo() -> None:
    """Demonstrate the Game of Life with various patterns."""
    print("Conway's Game of Life Demo")
    print("=" * 50)
    
    # Create a game
    game = GameOfLife(40, 20)
    
    # Add different patterns
    print("\n1. Adding Block pattern (still life):")
    game.add_pattern(GameOfLife.block(), 2, 5)
    
    print("\n2. Adding R-pentomino (methuselah):")
    game.add_pattern(GameOfLife.r_pentomino(), 20, 8)
    
    print("\n3. Adding Glider pattern (spaceship):")
    game.add_pattern(GameOfLife.glider(), 30, 5)
    
    print("\n4. Adding Diehard (methuselah):")
    game.add_pattern(GameOfLife.diehard(), 10, 15)
    
    print("\n5. Adding Acorn (methuselah):")
    game.add_pattern(GameOfLife.acorn(), 25, 15)
    
    print("\nInitial state:")
    print(game)
    
    # Run a few generations
    print("\nRunning 10 generations...")
    for generation in range(1, 11):
        game.next_generation()
        print(f"\nGeneration {generation}:")
        print(game)
    
    # Demo alternative rulesets
    print("\n" + "=" * 50)
    print("Testing HighLife ruleset:")
    game_hl = GameOfLife(20, 10, ruleset=Ruleset.HIGHLIFE)
    game_hl.add_pattern(GameOfLife.glider(), 5, 3)
    print("\nHighLife Glider:")
    print(game_hl)
    game_hl.next_generation()
    print("\nAfter 1 generation:")
    print(game_hl)


def benchmark() -> None:
    """Run performance benchmark."""
    print("Performance Benchmark")
    print("=" * 50)
    
    sizes = [(50, 50), (100, 100), (200, 200), (500, 500)]
    iterations = 100
    
    for width, height in sizes:
        game = GameOfLife(width, height)
        game.randomize(0.3)
        
        # Benchmark vectorized method
        start = time.time()
        for _ in range(iterations):
            game.next_generation()
        elapsed = time.time() - start
        
        print(f"Grid {width}x{height}: {elapsed:.4f}s ({iterations} iterations)")
        print(f"  Avg: {elapsed/iterations*1000:.2f}ms per generation")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "--gui":
            gui_main()
        elif sys.argv[1] == "--benchmark":
            benchmark()
        else:
            demo()
    else:
        demo()