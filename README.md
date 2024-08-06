# Pac-Man Game with A* Pathfinding ᗧ···ᗣ···ᗣ··

This is a Python implementation of the classic Pac-Man game, featuring A* and Dijkstra's pathfinding algorithms for ghost movement. The game is built using the Pygame library and demonstrates basic game development concepts and graph traversal/pathfinding techniques.

This project was created as a fun way to compare Dijkstra's Algorithm with the A* Algorithm for UC Berkeley's Extension "Data Structures and Algorithms" COMPSCI X404.1 course.

## Features ✨

- 🕹️ Classic Pac-Man gameplay
- 🤖 A* and Dijkstra's pathfinding algorithms for ghost movement
- 🔄 Ability to switch between A* and Dijkstra's algorithms during gameplay
- 🗺️ Customizable maze layout
- 🏆 Score tracking
- 🚀 Game over screen with restart option

<img width="593" alt="Pacman Screenshot" src="https://github.com/user-attachments/assets/7dff17e6-2e86-44f3-ac75-35aee51ecccd">

## Requirements 🛠️

- 🐍 Python 3.12
- 🎮 Pygame library

## Installation 💻

1. Ensure you have Python 3.12 installed on your system.
2. Install the Pygame library by running:
   ```
   pip install pygame
   ```
3. Download the `main.py` file to your local machine.

## How to Play 👾

1. Run the game by executing the following command in your terminal:
   ```
   python main.py
   ```
2. Use the arrow keys to move Pac-Man:
   - ⬆️ Up Arrow: Move Up
   - ⬇️ Down Arrow: Move Down
   - ⬅️ Left Arrow: Move Left
   - ➡️ Right Arrow: Move Right
3. Eat all the dots while avoiding the ghosts.
4. Press 'A' to switch to A* pathfinding algorithm.
5. Press 'D' to switch to Dijkstra's pathfinding algorithm.

## Game Controls 🕹️

- ⬆️⬇️⬅️➡️ Arrow Keys: Move Pac-Man
- 🅰️ 'A' Key: Switch to A* pathfinding algorithm
- 🅳 'D' Key: Switch to Dijkstra's pathfinding algorithm
- 🔄 'R' Key: Restart the game (on game over screen)
- ❌ 'Q' Key: Quit the game (on game over screen)

## Customization 🛠️

You can customize the game by modifying the following variables in the `main.py` file:

- `MAZE`: Change the layout of the maze
- `CELL_SIZE`: Adjust the size of each cell in the maze
- `PACMAN_START`: Set Pac-Man's starting position
- `GHOST_STARTS`: Set the starting positions of the ghosts

## Code Structure 📂

- `PacmanGame` class: Main game logic
- `draw_grid`: Renders the maze
- `draw_entities`: Renders Pac-Man and ghosts
- `move_pacman`: Handles Pac-Man movement
- `move_ghosts`: Manages ghost movement using pathfinding
- `a_star` and `dijkstra`: Implement pathfinding algorithms
- `game_over_screen`: Displays the game over screen
- `run`: Main game loop

## Contributing 🤝

Feel free to fork this project and submit pull requests with improvements or bug fixes. Some areas for potential enhancement include:

- 🔊 Adding sound effects and music
- 🏙️ Implementing multiple levels
- 🏅 Creating a high-score system
- 💥 Adding power-ups and different ghost behaviors
- 🐛 Fixing side scroll pass on the edges

## License 📜

This project is open source and available under the [MIT License](https://opensource.org/licenses/MIT).

## Acknowledgements 🙏

This game was created as a learning project and draws inspiration from the classic Pac-Man arcade game by Namco.

Enjoy playing! 🎉👾
