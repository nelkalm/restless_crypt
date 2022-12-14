# restless_crypt
An implementation of a dungeon crawler game using the Pygame module.

## Description
Welcome to Restless Crypt, a game where the main character, a Fire Fairy, must escape a 4-level restless dungeon with enemies. The Fairy must fight a boss at the last level to escape the dungeon.

This project is a fleshed-out version of a simple shell-based game introduced in my first CS courses. Originally, the project scope did not involve Pygame; it was just a command-line user interaction with one main character and two enemies to demonstrate my understanding of object-oriented programming concepts. I took this project a step further by creating more enemies and items, including level files, implementing a GUI with event-based user-interaction, including sound and sound effects. 

![Restless Crypt Game Overview](https://github.com/nelkalm/restless_crypt/blob/main/restless-crypt-gif/game-overview_AdobeExpress.gif)

## Development
The diagram below shows the overall development structure to implement this game.

![File and object structure for implementing Restless Crypt](https://github.com/nelkalm/restless_crypt/blob/main/restless-crypt-diagram.png?raw=true)

The main.py Python file takes in level data as csv files, and use them to construct the game screen using Pygame and the different main game objects: World, Weapon, Item, Button, and ScreenFade. All main game objects are drawn on the screen.

The World object is initialized and then used to create Character objects: the main player, enemies, and the boss enemy. Each of these Characters can use objects initialized by the Weapon class. The Bossball object is used exclusively by the boss enemy; all its functionalities are inherited by the Weapon class. 

## Gameplay and Screenshots

Fire fairy magic balls at enemies:

<img src="https://github.com/nelkalm/restless_crypt/blob/main/restless-crypt-gif/hitting-enemies_AdobeExpress.gif" width="450" />

Accumulate score by collecting coins:

<img src="https://github.com/nelkalm/restless_crypt/blob/main/restless-crypt-gif/accummulate-coins_AdobeExpress.gif" width="450" />

Game over when player's health reaches 0:

<img src="https://github.com/nelkalm/restless_crypt/blob/main/restless-crypt-gif/game-over_AdobeExpress.gif" width="450" />

## Playing the game
To play the game, you have to execute the 'main.py' file with python. The command to do this will be like:

    $ python3 path_to/main.py
    $ python path_to/main.py

Depending on the version of python that you have installed. Try python3 first, and if the command is not recognized, try with python

You'll also need the pygame package: You can install it through pip with the command:

    $ pip3 install pygame
    $ pip install pygame

Depending on the version of pip that you have installed. Try pip3 first, and if the command is not recognized, try with pip.

