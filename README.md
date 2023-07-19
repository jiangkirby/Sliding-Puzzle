# Puzzle Slider Game

Puzzle Slider Game is a combination puzzle game where players must slide pieces to establish a specific end result that matches a solution. It's a digital version of the popular "15-puzzle" or "15-slide" game, but with added functionalities and options.

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Setup](#setup)
- [Usage](#usage)
- [Additional Notes](#additional-notes)
- [Testing](#testing)
- [Contributing](#contributing)

## Description

This project is a Python implementation of the Puzzle Slider Game. The game allows players to slide tiles vertically or horizontally to solve the puzzle. It includes a splash screen, customizable number of moves, "Reset" and "Load" options, and the ability to quit the game.

## Features

- Splash Screen: The game displays a splash screen for a few seconds before starting.
- Player Name Input: Players can enter their names through a pop-up window.
- Customizable Moves: Players can select the number of moves allowed to solve the puzzle.
- Move Count Display: The game keeps track of the number of moves completed by the player.
- Win/Lose Conditions: If the player solves the puzzle within the allowed moves, they win; otherwise, they lose.
- Reset Function: Players can use the "Reset" button to see the completed puzzle.
- Load Puzzle: Users can load different puzzles from the file system.
- Error Handling: The program handles missing or malformed puzzle files and logs errors to "error_log.txt".
- Quit Button: Players can exit the game anytime using the "Quit" button.

## Setup

1. Clone the repository to your local machine.
2. Install Python (version 3.x) if you haven't already.
3. Navigate to the project directory.

## Usage

1. Run the `puzzle_game.py` file to start the game.
2. The splash screen will be displayed for a few seconds, then a pop-up window will ask for the player's name.
3. Select the number of moves allowed and start the puzzle.
4. Click on a tile adjacent to the blank space to move it. The number of moves will be displayed in the status area.
5. If the puzzle is solved within the allowed moves, a victory message will be shown.
6. Players can click "Reset" to see the completed puzzle or "Load" to load a different puzzle.
7. The "Quit" button can be used to exit the game.

## Additional Notes

- Around 50% of puzzles with tiles in randomly generated order are solvable. The project includes a function that checks whether or not the current tile order is solvable. To view the solvability status, check the console print.

- The project includes code that guarantees the puzzle provided to the player is solvable.

- The program logs errors to the "error_log.txt" file.

## Testing

The project includes a set of PyUnit tests to ensure its functionality. To run the tests, use the following command:

```bash
python -m unittest discover -p 'unittest*.py'
```

## Contributing

If you find any issues with the project or have suggestions for improvements, please feel free to contribute or open an issue.