# void_reckoning
## year 11 computer science semester 1 game - space shooter

## deliverable 4 documentation
### prerequisites
- sys
- pygame
- random
- math
- time
- enum
- python version 3.10.7
### functional requirements
- player combat system
    - the player can currently shoot laser bullets. When the bullets hit asteroids and enemies, the bullet would deal damage to the object that got hit
    - there is also a "bomb" that the player can place once every minute. A circle would expane and everything that touches it would directly die.
- Progressively harder gameplay
    - The longer the player stays in the game alive, the more enemies and asteroids would spawn. the enemies would also travel and attack faster.
- Physics based movement system
    - The player and other objects in the game moves with a system where they each have their own vectors, and would each travel in their own direction and speed

### Non functional requirements
- Smooth perfomance
    - the game is currently able to run at around 60 fps most of the time.
- Sound and visuals
    - each object has their own sprites. I also implemented music and sound effects.

### Test cases
- basic movement test
    1. Going into the game, press the start button.
    2. pressing w would make the player should go up, d goes right, s goes down, a goes left.
    3. press c to change the camera mode
    4. there should be a smooth transition where the caemra turns until the player faces toward the top of the screen
    5. pressing a should make the player turn left, d turns right
- firing
    1. make the camera mode "fixed"
    2. press e (the firing key), the laser should shoot out of the tip of the player spaceship, and in the direction of where the player is facing
    3. make the camera mode "rotated"
    4. press e again, the laser should shoot up (where the player should also face)
- drawing
    1. playing the game normally, there should not be any fickering or blinking objects
    2. the transition between the 2 camera modes should be smooth and should exit as soon as the required movements are finished.










### Encounted problems
![image of laser stuck ot the player](docs\debugging\problems_encountered\laser_stuck.png)

This happened when i changed from using rectangles to using sprites.
It happened because of how i implemented the movement system, where there was a variable for x and y, but also a *Rect* object. updating the x and y variable does not actually change the x and y value inside the *Rect* object, and therefore the laser bullets would get stuck on top of the player

![hit box test](docs\debugging\problems_encountered\hitbox_test.png)

another probelm I encountered is rectangles being incorrectly initialised, and therefore objects would not behave correctly. During testing, I would draw out the rectangles used for collision detectiosn to check if they are done correctly.

# usage guide
run ```src/main.py``` to run the game

press the "start" button to start the game.

use wasd to move around, space to brake/slow down, e to fire laser bullet and c to change camera mode.

your goal is to kill as many alien enemies as possible. There are 2 types:

![bumper](assets\images\bumper.png) bumpers, which would move directly towards the player. Can be pushed away with asteroids. The player would lose health if a bumper touches the player's spaceship

![turret](assets\images\turret.png) turrets, which stays at a single place and would shoot the player with small, green bullets ![turret bullets](assets\images\turret_bullet.png).
