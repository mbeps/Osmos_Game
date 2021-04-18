# Osmos Game
- [Osmos Game](#osmos-game)
	- [Introduction](#introduction)
	- [Technology](#technology)
	- [Rules](#rules)
	- [Features](#features)
	- [Controls](#controls)
	- [Installation](#installation)
	- [Running](#running)
	- [Modules & Classes](#modules--classes)
	- [License](#license)

## Introduction 
The game is called Osmos. The main objective is for the player to kill and engulf all the enemies. All the balls bounce against walls upon collisions. There is also gravity acting upon entities; mass objects and other enemies are attracted to each other but not the player. Since mass objects do not merge, they are never bigger than the enemies which means that they are always attracted to the enemies. Gravity acts on the bigger enemies too but the force is much weaker. 

The bigger ball engulfs the smaller balls. Gravity makes it easier to engulf entities. If the player is larger than the enemy, then then the enemy is engulfed and killed. However, if the enemy is larger, then the player is killed, and the game is over. Because enemies can engulf each other and merge into a massive enemy, it makes it hard for the player to win which means that a timer has been implemented to split the enemies into smaller ones, this gives a chance for the player to win. Mass objects which are ejected by the player are also engulfed. Once a ball engulfs another, the size increases. 

For the player to move via the controls, mass is lost. This mass is ejected in the opposite direction to simulate Newton’s Laws. As mentioned before, this is then engulfed by others. 

At a set time, power ups will be spawned at a random place in the canvas. These power ups increase the speed of the player for a limited time. In the future, more types of power ups can be added. 

A timer can be set which defines the time limit by which time the player must win. If the timer runs out before the player has killed all the enemies, then the game is over. 

## Technology
The game is made a using the SimpleGUI module developed by CodeSkulptor3 for Python (version 3). Instructions are included bellow. Using this module, simple GUI applications can be built. A vector module has been used to handle all the vector calculations.

**Resources:**
- [CodeSkulptor3 Installation](#installation)
- [CodeSkulptor3 Documentation](#installation)

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

## Modules & Classes
**Entities:**
- *Ball* - the super class for enemies, player, mass, and power ups which defines the basic functionalities of a ball such as bouncing. 
- *Enemy* - sub-class of Ball which defines how an enemy should function. 
- *Mass* - sub-class of Ball which defines how mass should behave. Mass is normally ejected from the player when controlling it. 
- *Player* - sub-class of balls controlled by the user to kill all the enemies and win. 
- *Power_Ups* - sub-class of ball which is spawned in random places and does not move. Gives a temporary power up to the player. 

**Game_Control:**
- *Interactions* - this module manages all the interactions between objects and the the game environment.
- *Keyboard* - handles and keeps track of the key presses which can then be used to execute certain operations depending on the keys that were pressed. 
- *Vector* - manages all the vector calculations. 

**Maps:**
- *Line* - these are the walls around the canvas which represent the boundary of the game. Ball objects bounce upon collision. 

## License
MIT
