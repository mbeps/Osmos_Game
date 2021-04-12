# Osmos Game
## Introduction 
The game developed is called Osmos. The objective of this game is for the player to survive and kill all the enemies before the timer runs out. The bigger balls will engulf the smaller balls. This means that enemies can merge and become larger, the player will have to kill all the enemies before they merge otherwise the enemies will be too large for the player to kill. The timer is set by the player which defines how much time the player has to kill the enemies. The player is controlled using the arrow keys. All the balls in the game bounce on walls of they collide. 

## Rules
- Control the player with the arrow keys.
- Bigger balls kill the smaller ball.
- Player wins when all the enemies are dead.
- Player loses if the it gets killed or the timer runs out (if set).
- Balls (enemies, player) bounce if there is a collision with the wall.

## Features
- Power ups increase player speed for limited time.
- Time limit (can be unlimited).
- Gravity between objects. 
- Display scores.
- Mass is ejected from player when moving using arrow keys. 
- Enemy is split after a set time to make the game play more fair. 

## Controls
- **Left arrow (←)** - player moves left.
- **Right arrow (→)** - player moves right.
- **Up arrow (↑)** - player moves up.
- **Down arrow (↓)** - player moves down.
- **E** - exit game.

## Installation

SimpleGUI requires Python 3 to be installed. Game developed using Python 3.9. 

**Installing SimpleGUI for Windows**

```sh
pip install SimpleGUICS2Pygame
```

**Installing SimpleGUI for Unix (Linux / macOS)**

```sh
python3 -m pip install SimpleGUICS2Pygame
```

## Running
Run the `main.py` using Python 3. Make sure that you are in the directory where the game is stored. 

**Windows**
```sh
python main.py 
```


**Unix (macOS / Linux)**
```sh
python3 main.py 
```

## License
MIT
