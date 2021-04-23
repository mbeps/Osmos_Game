# **Osmos Game**
- [**Osmos Game**](#osmos-game)
	- [Introduction](#introduction)
	- [Technology](#technology)
	- [Rules](#rules)
	- [Features](#features)
	- [Controls](#controls)
	- [Demo Videos](#demo-videos)
	- [Installation](#installation)
	- [Running](#running)
- [**Documentation**](#documentation)
	- [Game Plan](#game-plan)
	- [Structure](#structure)
	- [Modules & Classes](#modules--classes)
	- [License](#license)

## Introduction 
The game is called Osmos. The main objective is for the player to kill and engulf all the enemies. All the balls bounce against walls upon collisions. There is also gravity acting upon entities; mass objects and other enemies are attracted to each other but not the player. Since mass objects do not merge, they are never bigger than the enemies which means that they are always attracted to the enemies. Gravity acts on the bigger enemies too but the force is much weaker. 

The bigger ball engulfs the smaller balls. Gravity makes it easier to engulf entities. If the player is larger than the enemy, then then the enemy is engulfed and killed. However, if the enemy is larger, then the player is killed, and the game is over. When player moves close to an enemy, it will eject mass into the enemy to move away from it, this will attract the enemy towards the player and increases its size. Because enemies can engulf each other and merge into a massive enemy, it makes it hard for the player to win which means that a timer has been implemented to split the enemies into smaller ones, this gives a chance for the player to win. Mass objects which are ejected by the player are also engulfed. Once a ball engulfs another, the size increases. 

For the player to move via the controls, mass is lost. This mass is ejected in the opposite direction to simulate Newton’s Laws. As mentioned before, this is then engulfed by others. 

At a set time, power ups will be spawned at a random place in the canvas. These power ups increase the speed of the player for a limited time. In the future, more types of power ups can be added. 

A timer can be set which defines the time limit by which time the player must win. If the timer runs out before the player has killed all the enemies, then the game is over. 

## Technology
The game is made a using the SimpleGUI module developed by CodeSkulptor3 for Python (version 3). Instructions are included bellow. Using this module, simple GUI applications can be built. A vector module has been used to handle all the vector calculations.

**Resources:**
- [CodeSkulptor3 Installation](#installation)
- [CodeSkulptor3 Documentation](https://py3.codeskulptor.org/docs.html)

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

## Demo Videos
**Winning**

https://user-images.githubusercontent.com/58662575/115227623-99f96200-a108-11eb-8bc5-45f0315c8dd3.mp4

- Player wins when there are no more enemies in the game. 
- Number of kills displayed in game. 

**Losing**

https://user-images.githubusercontent.com/58662575/115227647-a382ca00-a108-11eb-9f7a-34d79fd44100.mp4

- When player is dead because it was killed by an enemy. 
- Timer has ran out.

**Power Ups**

https://user-images.githubusercontent.com/58662575/115227682-aed5f580-a108-11eb-9678-e0bab53afdf0.mp4

- If the player peeks up a power up, it will get faster temporarily.
- Power ups spawn in random places in the canvas at certain times. 

**Split**

https://user-images.githubusercontent.com/58662575/115227701-b6959a00-a108-11eb-958f-77df52cde2bb.mp4

- At certain times, a random enemy will be split. 
  - Two smaller enemies will be created to give the player a chance to kill. 
- Only split when the enemy is large. 

**Timer**

https://user-images.githubusercontent.com/58662575/115227721-bf866b80-a108-11eb-9ccb-32559336015a.mp4

- When the timer is set, there is a time limit by which the player must win. 
- If the timer is not set, then the game place is unlimited (until enemies are dead or player is dead). 
- Timer is a countdown displayed in the game. 

**Gravity**

https://user-images.githubusercontent.com/58662575/115227259-25bebe80-a108-11eb-812b-b5790ae7701a.mp4

- Enemies and mass (ejected by player) are attracted to each other. 
- Bigger ball object has a larger pull on the smaller object. 
- Smaller ball object attracts the larger ball but the force is only a fraction of the attraction of the larger ball on the smaller. 
- Mass objects cannot merge (engulf each other) which means that they always have a set size which is smaller than the any enemy. 
  - Mass always strongly attracted to enemies. 
  - Multiple mass objects in one place (when ejected from same spot by player) have enough force to significantly move large enemy object. 
- Player does not attract any ball objects. 

## Installation

SimpleGUI requires Python 3 to be installed. Game developed using Python 3.9. 

**Installing SimpleGUI for Windows**

```sh
pip install SimpleGUICS2Pygame
```

**Installing SimpleGUI for Unix (Linux / macOS)**

```sh
pip3 install SimpleGUICS2Pygame
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

# **Documentation**
This section explains how the game fundamentally works. 

## Game Plan
This section explains the simple core mechanics of the game. 
**Game Over**

![image](https://user-images.githubusercontent.com/58662575/115228484-bf3aa000-a109-11eb-96bf-db435ad997d8.png)
- Player will engulf other balls (mass or enemies) to increase size.
- Mass will be lost to move - Mass will push in opposite direction.
- Enemies can engulf mass - If player is engulfed then the game is over.

**Bouncing**

![image](https://user-images.githubusercontent.com/58662575/115228817-248e9100-a10a-11eb-90af-9be342f0869a.png)
- All ball types of balls:
- 	Player
-	Enemy
-	Particles
-	Inheritance
-	All balls can inherit bounce, ingulf, etc methods

**Engulfing**

![image](https://user-images.githubusercontent.com/58662575/115228951-4ee04e80-a10a-11eb-9297-d4316aab0e53.png)
- If ball1 > ball2:
-	Ball1 engulfs ball2.
-	Else If ball2 > ball1:
-	Ball2 engulfs ball1.
Logic
- If ball1 > ball2
-	Ball1 gets mass from ball.
-	Ball2 is removed.

**Moving**

![image](https://user-images.githubusercontent.com/58662575/115229070-7afbcf80-a10a-11eb-8d2e-10e66f2c5abe.png)
- Newtons third means that the smaller mass will push the player.
- Mass will be faster than the player as player will be bigger.
- Both mass and player will have equal momentum
- Enemies do not lose mass but slit after some time

## Structure
This section shows the core structure of the game. It demonstrates how components link to each other. 

![Game Structure](https://user-images.githubusercontent.com/77356762/115402790-a69eb880-a1e3-11eb-9607-1d5dbeeee3b2.png)


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
