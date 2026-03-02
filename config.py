# Configuration file for Conway's Game of Life
# This file contains default settings that can be customized

# Grid settings
DEFAULT_WIDTH = 50
DEFAULT_HEIGHT = 50

# GUI settings
GUI_WIDTH = 1000
GUI_HEIGHT = 700
GUI_CELL_SIZE = 18

# Colors (RGB format)
COLORS = {
    'background': (20, 20, 30),
    'grid': (40, 40, 60),
    'cell_alive': (100, 200, 100),
    'cell_dead': (30, 30, 40),
    'text': (220, 220, 220),
    'highlight': (255, 255, 200),
    'status_running': (100, 255, 100),
    'status_paused': (255, 100, 100),
}

# Simulation settings
DEFAULT_DENSITY = 0.3  # Default probability of cell being alive in random mode
DEFAULT_SPEED = 10  # Updates per second in GUI
MAX_SPEED = 60
MIN_SPEED = 1

# Algorithm settings
USE_VECTORIZED_BY_DEFAULT = True  # Use faster NumPy vectorization by default

# Pattern library - now includes more patterns
BUILTIN_PATTERNS = [
    'block',
    'blinker',
    'glider',
    'beacon',
    'pulsar',
    'lwss',
    'toad',
    'pentadecathlon',
    'gosper_glider_gun',
    'r_pentomino',
]

# Keyboard mapping for pattern selection
PATTERN_KEYS = {
    '1': 'block',
    '2': 'blinker',
    '3': 'glider',
    '4': 'beacon',
    '5': 'pulsar',
    '6': 'lwss',
    '7': 'toad',
    '8': 'pentadecathlon',
    '9': 'gosper_glider_gun',
}

# File save/load settings
SAVE_FILE_PATH = 'game_of_life_save.json'