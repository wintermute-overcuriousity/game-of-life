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



import pygame
import sys
from typing import Tuple, Optional
import time


class GameOfLifeGUI:
    """
    PyGame GUI for Conway's Game of Life.
    """
    
    def __init__(self, width: int = 800, height: int = 600, cell_size: int = 15):
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
        
        # Create the game instance
        self.game = GameOfLife(self.grid_width, self.grid_height)
        
        # Create the screen
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Conway's Game of Life")
        
        # Colors
        self.BACKGROUND = (20, 20, 30)
        self.GRID_COLOR = (40, 40, 60)
        self.CELL_ALIVE = (100, 200, 100)
        self.CELL_DEAD = (30, 30, 40)
        self.TEXT_COLOR = (220, 220, 220)
        self.HIGHLIGHT_COLOR = (255, 255, 200)
        
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
        
        # Pattern selection
        self.patterns = {
            'block': GameOfLife.block,
            'blinker': GameOfLife.blinker,
            'glider': GameOfLife.glider,
            'beacon': GameOfLife.beacon,
            'pulsar': GameOfLife.pulsar,
            'lwss': GameOfLife.lwss,
            'toad': GameOfLife.toad
        }
        self.current_pattern = 'glider'
    
    def handle_events(self):
        """Handle PyGame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                # Space: Play/Pause
                if event.key == pygame.K_SPACE:
                    self.running = not self.running
                
                # R: Reset (clear grid)
                elif event.key == pygame.K_r:
                    self.game.clear()
                    self.generation = 0
                
                # C: Clear grid
                elif event.key == pygame.K_c:
                    self.game.clear()
                    self.generation = 0
                
                # +/-: Adjust speed
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    self.speed = min(60, self.speed + 2)
                elif event.key == pygame.K_MINUS:
                    self.speed = max(1, self.speed - 2)
                
                # 1-7: Select patterns
                elif event.key == pygame.K_1:
                    self.current_pattern = 'block'
                elif event.key == pygame.K_2:
                    self.current_pattern = 'blinker'
                elif event.key == pygame.K_3:
                    self.current_pattern = 'glider'
                elif event.key == pygame.K_4:
                    self.current_pattern = 'beacon'
                elif event.key == pygame.K_5:
                    self.current_pattern = 'pulsar'
                elif event.key == pygame.K_6:
                    self.current_pattern = 'lwss'
                elif event.key == pygame.K_7:
                    self.current_pattern = 'toad'
                
                # D: Toggle draw mode (alive/dead)
                elif event.key == pygame.K_d:
                    self.draw_mode = 1 if self.draw_mode == 0 else 0
                
                # F: Fill random
                elif event.key == pygame.K_f:
                    self.game.randomize(0.3)
                    self.generation = 0
                
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
                        self.game.add_pattern(pattern_func(), x, y)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left click
                    self.dragging = False
            
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging:
                    self.handle_click(event.pos)
        
        return True
    
    def handle_click(self, pos):
        """Handle mouse click at position."""
        x, y = self.screen_to_grid(pos)
        if 0 <= x < self.grid_width and 0 <= y < self.grid_height:
            current_state = self.game.get_cell(x, y)
            # Toggle or set based on draw mode
            if self.draw_mode == 1:
                self.game.set_cell(x, y, 1)
            else:
                self.game.set_cell(x, y, 0)
    
    def screen_to_grid(self, pos):
        """Convert screen coordinates to grid coordinates."""
        x, y = pos
        grid_x = x // self.cell_size
        grid_y = y // self.cell_size
        return grid_x, grid_y
    
    def update(self):
        """Update game state if running."""
        if not self.running:
            return
        
        current_time = time.time()
        if current_time - self.last_update > 1.0 / self.speed:
            self.game.next_generation()
            self.generation += 1
            self.last_update = current_time
    
    def draw(self):
        """Draw everything to the screen."""
        # Clear screen
        self.screen.fill(self.BACKGROUND)
        
        # Draw grid lines
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, self.GRID_COLOR, 
                           (x, 0), (x, self.height), 1)
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, self.GRID_COLOR,
                           (0, y), (self.width, y), 1)
        
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
    
    def draw_ui(self):
        """Draw UI elements and text."""
        # Status text
        status = "RUNNING" if self.running else "PAUSED"
        status_color = (100, 255, 100) if self.running else (255, 100, 100)
        
        texts = [
            f"Generation: {self.generation}",
            f"Status: {status}",
            f"Speed: {self.speed} FPS",
            f"Grid: {self.grid_width}x{self.grid_height}",
            f"Pattern: {self.current_pattern}",
            f"Draw mode: {'ALIVE' if self.draw_mode == 1 else 'DEAD'}"
        ]
        
        # Draw text background
        pygame.draw.rect(self.screen, (30, 30, 45, 200), 
                        (10, 10, 300, 180), border_radius=8)
        pygame.draw.rect(self.screen, (60, 60, 80), 
                        (10, 10, 300, 180), 2, border_radius=8)
        
        # Draw texts
        for i, text in enumerate(texts):
            color = status_color if i == 1 else self.TEXT_COLOR
            text_surface = self.font.render(text, True, color)
            self.screen.blit(text_surface, (20, 20 + i * 30))
        
        # Draw controls help
        controls = [
            "CONTROLS:",
            "SPACE: Play/Pause",
            "R: Reset grid",
            "C: Clear grid",
            "+/-: Adjust speed",
            "1-7: Select pattern",
            "D: Toggle draw mode",
            "F: Fill random",
            "L-click: Draw cells",
            "R-click: Place pattern",
            "ESC: Quit"
        ]
        
        # Draw controls background
        pygame.draw.rect(self.screen, (30, 30, 45, 200),
                        (self.width - 310, 10, 300, 340), border_radius=8)
        pygame.draw.rect(self.screen, (60, 60, 80),
                        (self.width - 310, 10, 300, 340), 2, border_radius=8)
        
        # Draw controls text
        for i, text in enumerate(controls):
            color = (255, 255, 200) if i == 0 else self.TEXT_COLOR
            font = self.font if i == 0 else self.small_font
            text_surface = font.render(text, True, color)
            self.screen.blit(text_surface, (self.width - 300, 20 + i * 28))
    
    def run(self):
        """Main game loop."""
        clock = pygame.time.Clock()
        
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            clock.tick(60)  # Cap at 60 FPS
        
        pygame.quit()


def gui_main():
    """Main function to run the GUI."""
    print("Starting Conway's Game of Life GUI...")
    print("Controls:")
    print("  SPACE: Play/Pause")
    print("  R: Reset grid")
    print("  C: Clear grid")
    print("  +/-: Adjust speed")
    print("  1-7: Select patterns")
    print("  D: Toggle draw mode (alive/dead)")
    print("  F: Fill random")
    print("  L-click: Draw cells")
    print("  R-click: Place pattern")
    print("  ESC: Quit")
    print()
    
    # Create and run the GUI
    gui = GameOfLifeGUI(width=1000, height=700, cell_size=18)
    gui.run()


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
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--gui":
        gui_main()
    else:
        demo()