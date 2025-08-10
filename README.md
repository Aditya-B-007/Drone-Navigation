# Drone-Navigation
This project simulates an autonomous drone navigating a 2D grid environment using A* pathfinding.
The drone dynamically scans its surroundings, updates its knowledge of the environment, and replans routes when obstacles appear or are detected.
Features

    A* pathfinding algorithm for optimal route planning.

    Dynamic replanning when obstacles are detected or appear.

    Fog of war visualization to simulate limited sensor visibility.

    Sensor-based mapping of unknown terrain.

    Obstacle generation with adjustable density.

    Real-time simulation using Pygame.

Project Structure

.
├── main.py              # Entry point for running the simulation
├── drone.py             # Drone class with movement, sensing, and path replanning
├── pathfinding_logic.py # A* pathfinding algorithm implementation

File Overview

    main.py – Initializes the simulation, sets up the environment, generates obstacles, and runs the game loop.

    drone.py – Implements the drone's movement, sensing, and path validation.

    pathfinding_logic.py – Contains a simple A* search algorithm for finding optimal paths.

Requirements

    Python 3.8+

    Pygame

Install dependencies:

pip install pygame

Usage

Run the simulation:

python main.py

Controls

    Close the simulation window to stop the program.

    Obstacles regenerate every 10 seconds to simulate a changing environment.

Configuration

You can tweak parameters inside main.py:

    TILE_SIZE – Size of each grid cell (default: 16).

    OBSTACLE_DENSITY – Probability of an obstacle spawning in a cell (default: 0.09).

    Start_pos & End_pos – Coordinates for the start and end positions.

    CHANGE_EVENT timer – Frequency of world state changes.

How It Works

    Environment Setup
    The grid world is initialized with randomly generated obstacles. The drone starts at a defined position and aims to reach the target.

    Sensor Scanning
    The drone has a circular sensor radius and updates its known map (known_grid) as it moves.

    Pathfinding
    The A* algorithm (pathfinding_logic.py) is used to plan an optimal route from the current position to the goal based on the known map.

    Dynamic Replanning
    If the current path becomes blocked, the drone recalculates a new route.

    Visualization

        Obstacles: Red

        Path: Light blue outlines

        Unexplored areas: Covered in fog

Example Output

When running, you'll see:

    The drone moving step-by-step toward the goal.

    Fog clearing as the drone scans its surroundings.

    The path updating when obstacles appear.

License

This project is released under the MIT License.
