# Conway's Game of Life

A Python implementation of Conway's Game of Life, a cellular automaton devised by mathematician John Horton Conway.

![Game of Life Screenshot Placeholder](#screenshot-placeholder)

## Description

Conway's Game of Life is a zero-player game that evolves based on its initial state. It consists of a grid of cells that can be either alive or dead. The game progresses through generations, with each cell's state determined by its neighbors according to a simple set of rules.

### Conway's Rules
1. **Underpopulation**: Any live cell with fewer than two live neighbors dies
2. **Survival**: Any live cell with two or three live neighbors lives on to the next generation
3. **Overpopulation**: Any live cell with more than three live neighbors dies
4. **Reproduction**: Any dead cell with exactly three live neighbors becomes a live cell

## Features

- **Complete Game of Life implementation** with Conway's cellular automaton rules
- **Interactive grid management** with customizable width and height
- **Multiple initialization options**:
  - Clear grid
  - Random initialization with adjustable density
  - Pattern placement at specific coordinates
- **Built-in pattern library** including:
  - **Still lifes**: Block
  - **Oscillators**: Blinker (period 2), Beacon (period 2), Pulsar (period 3), Toad (period 2), Pentadecathlon (period 15)
  - **Spaceships**: Glider, Lightweight Spaceship (LWSS)
  - **Guns**: Gosper Glider Gun (produces gliders indefinitely)
  - **Methuselahs**: R-Pentomino (evolves for 1100+ generations)
- **Visual ASCII representation** using Unicode block characters
- **Save/Load grid states** to JSON files
- **Demo function** showcasing pattern interactions
- **Extensible architecture** for adding custom patterns
- **Pygame GUI** with interactive controls and visualization

## Installation

### Prerequisites
- Python 3.6 or higher
- NumPy library for efficient array operations
- Pygame library for graphical interface

### Install Dependencies
```bash
# Install required packages
pip install numpy pygame
```

### Clone the Repository
```bash
git clone https://github.com/wintermute-overcuriousity/game-of-life.git
cd game-of-life
```

## Usage

### Basic Usage

```python
from game_of_life import GameOfLife

# Create a 50x50 grid
game = GameOfLife(50, 50)

# Add a glider pattern at position (10, 10)
game.add_pattern(GameOfLife.glider(), 10, 10)

# Run 10 generations
for generation in range(10):
    game.next_generation()
    print(f"Generation {generation + 1}:")
    print(game)
```

### Running the Demo
```bash
python game_of_life.py
```

The demo will:
1. Display various patterns (Block, Blinker, Glider, Beacon, LWSS)
2. Show 10 generations of evolution
3. Clear the grid and demonstrate random initialization
4. Show 5 generations of random pattern evolution

### Running the GUI
```bash
python game_of_life.py --gui
```

The GUI provides:
- Interactive grid editing with mouse
- Real-time visualization
- Play/Pause controls
- Speed adjustment
- Pattern selection and placement
- Generation counter
- Save/Load grid states

### Available Patterns

The implementation includes the following static methods for pattern creation:

```python
# Still lifes
GameOfLife.block()      # 2x2 block (stable)

# Oscillators
GameOfLife.blinker()    # 3x1 oscillator (period 2)
GameOfLife.beacon()     # 4x4 oscillator (period 2)
GameOfLife.pulsar()     # 13x13 oscillator (period 3)
GameOfLife.toad()       # 4x3 oscillator (period 2)
GameOfLife.pentadecathlon()  # 16x9 oscillator (period 15)

# Spaceships
GameOfLife.glider()     # 3x3 glider (travels diagonally)
GameOfLife.lwss()       # 5x4 Lightweight Spaceship

# Guns
GameOfLife.gosper_glider_gun()  # 36x9 Gosper Glider Gun

# Methuselahs
GameOfLife.r_pentomino()  # 5x5 R-Pentomino (evolves 1100+ generations)
```

### Adding Custom Patterns

```python
# Define your own pattern as a 2D list
custom_pattern = [
    [1, 0, 1],
    [0, 1, 0],
    [1, 0, 1]
]

# Add it to the grid
game.add_pattern(custom_pattern, x=20, y=20)
```

### Grid Controls

```python
# Create game instance
game = GameOfLife(width=60, height=40)

# Set individual cells
game.set_cell(x=5, y=5, state=1)  # Make cell alive
game.set_cell(x=5, y=6, state=0)  # Make cell dead

# Get cell state
state = game.get_cell(x=5, y=5)  # Returns 1 (alive) or 0 (dead)

# Clear the entire grid
game.clear()

# Randomize with 25% density
game.randomize(density=0.25)

# Count neighbors of a cell
neighbors = game.count_neighbors(x=5, y=5)

# Advance to next generation
next_grid = game.next_generation()

# Save grid to file
game.save_to_file('my_grid.json')

# Load grid from file
game = GameOfLife.load_from_file('my_grid.json')
```

### GUI Controls

When running the GUI (`--gui` flag), you can use the following controls:

#### Keyboard Controls
- **SPACE**: Play/Pause simulation
- **R**: Reset grid (clear all cells)
- **C**: Clear grid
- **S**: Save grid to file
- **L**: Load grid from file
- **+/-**: Adjust simulation speed
- **1-9**: Select different patterns:
  - 1: Block (still life)
  - 2: Blinker (oscillator)
  - 3: Glider (spaceship)
  - 4: Beacon (oscillator)
  - 5: Pulsar (oscillator)
  - 6: Lightweight Spaceship (LWSS)
  - 7: Toad (oscillator)
  - 8: Pentadecathlon (oscillator)
  - 9: Gosper Glider Gun
- **D**: Toggle draw mode (alive/dead)
- **F**: Fill grid with random pattern
- **V**: Toggle between vectorized and iterative method
- **ESC**: Quit application

#### Mouse Controls
- **Left Click**: Draw cells (toggle based on draw mode)
- **Right Click**: Place selected pattern at cursor position
- **Click and Drag**: Continuous drawing

## Screenshot Placeholder

```
Generation 1:
████████     ████████
██     ██   ██     ██
██  ██  ██   ██  ██  ██
██     ██   ██     ██
████████     ████████

Generation 2:
   ██████        ██████
  ██    ██      ██    ██
  ██    ██      ██    ██
   ██████        ██████

Generation 3:
    ██          ██
   ██████      ██████
    ██          ██
```

*(Actual ASCII visualization will be displayed when running the program)*

## Project Structure

```
game-of-life/
├── game_of_life.py    # Main implementation with GUI
├── config.py          # Configuration settings
├── README.md          # This documentation
├── requirements.txt   # Python dependencies
└── .git/              # Git repository
```

## Dependencies

- **NumPy**: For efficient array operations and grid management
- **Pygame**: For graphical visualization (required for GUI mode)

## Running Tests

```bash
# Run the built-in demo
python game_of_life.py

# Run the GUI
python game_of_life.py --gui

# Run benchmark
python game_of_life.py --benchmark

# Test specific patterns
python -c "
from game_of_life import GameOfLife

# Test save/load
game = GameOfLife(20, 20)
game.add_pattern(GameOfLife.glider(), 5, 5)
game.save_to_file('test.json')

loaded = GameOfLife.load_from_file('test.json')
print('Save/Load works!')
print(loaded)
"

# Test new patterns
python -c "
from game_of_life import GameOfLife
game = GameOfLife(40, 20)
game.add_pattern(GameOfLife.gosper_glider_gun(), 1, 5)
print('Gosper Glider Gun:')
print(game)
"
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Acknowledgments

- John Horton Conway for creating the Game of Life
- The cellular automata community for pattern discovery
- NumPy developers for the excellent array library
- Pygame developers for the graphics library

## Future Enhancements

- [ ] Pattern library browser
- [ ] Export to image/video formats
- [ ] Web interface using Flask/Django
- [ ] Additional cellular automaton rulesets (e.g., HighLife, Day & Night)
- [ ] Zoom and pan in GUI
- [ ] Multiple rule presets