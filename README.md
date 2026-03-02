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
  - **Oscillators**: Blinker (period 2), Beacon (period 2), Pulsar (period 3), Toad (period 2)
  - **Spaceships**: Glider, Lightweight Spaceship (LWSS)
  - **Complex oscillators**: Pentadecathlon (period 15)
- **Visual ASCII representation** using Unicode block characters
- **Demo function** showcasing pattern interactions
- **Extensible architecture** for adding custom patterns

## Installation

### Prerequisites
- Python 3.6 or higher
- NumPy library for efficient array operations

### Install Dependencies
```bash
# Install required packages
pip install numpy pygame
```

### Clone the Repository
```bash
git clone https://github.com/yourusername/game-of-life.git
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

# Spaceships
GameOfLife.glider()     # 3x3 glider (travels diagonally)
GameOfLife.lwss()       # 5x4 Lightweight Spaceship

# Complex patterns
GameOfLife.pentadecathlon()  # 16x9 oscillator (period 15)
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
```

## Screenshot Placeholder

```
Generation 1:
███████   ███████
█     █   █     █
█  █  █   █  █  █
█     █   █     █
███████   ███████

Generation 2:
   ███        ███
  █   █      █   █
  █   █      █   █
   ███        ███

Generation 3:
    █          █
   ███        ███
    █          █
```

*(Actual ASCII visualization will be displayed when running the program)*

## Project Structure

```
game-of-life/
├── game_of_life.py    # Main implementation
├── README.md          # This documentation
└── .git/              # Git repository
```

## Dependencies

- **NumPy**: For efficient array operations and grid management
- **Pygame**: For graphical visualization (optional, for future GUI implementation)

## Running Tests

```bash
# Run the built-in demo
python game_of_life.py

# Test specific patterns
python -c "
from game_of_life import GameOfLife
game = GameOfLife(20, 20)
game.add_pattern(GameOfLife.glider(), 5, 5)
print('Glider added successfully')
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

## Future Enhancements

- [ ] Pygame-based graphical interface
- [ ] Interactive grid editing
- [ ] Pattern library browser
- [ ] Speed controls for generation progression
- [ ] Save/Load grid states
- [ ] Export to image/video formats
- [ ] Web interface using Flask/Django
- [ ] Performance optimizations for larger grids
- [ ] Additional cellular automaton rulesets