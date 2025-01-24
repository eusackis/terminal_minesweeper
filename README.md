# Terminal minesweeper

## Project description
This is pretty straight-forward. It is a minesweeper game I made which you can play in a CLI. Or at least should be.
This was part of the codecademy 'Computer Science' course as a first portfolio project - creating a game to play in the terminal.
Some of the suggested options were tic-tac-toe, "Who Wants To Be a Millionaire?", Tarot cards, but I went with Minesweeper, because
it seemed like the most interesting option and probably the most challenging out of all of them. 

The courses is based on learning the concepts of CS with Python, so the whole game is written in Python.

Two things were specifically challenging:
  1) the initial foundational loop of reading the surrounding tiles (due to a misunderstanding of how to implement try/except and invalid iterable values), which is the underlying logic for several functions in this game
  2) the mass uncovering function when you open a blank tile

This does have some unicode characters, because I wanted to add some more easily visually discernable symbols, but this might be causing some issues for the CLI if it is not set-up properly.
Will need to look if I can mitigate it in the code itself or just provide the initial option to opt out of the unicode in favor of simpler characters.

## How to play the game
Nothing fancy - just have Python 3.10 installed (might be sufficient to just have any Python 3 version).
Open up a terminal and run:

`python path/to/file/game.py`
