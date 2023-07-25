# Ultimate Tic-Tac-Toe
## Setup
Set up the virtual environment by running the following in the working directory:

`python -m venv venv`

`pip install -r requirements.txt`

From there you can run `python match.py -q` to run a match with the sample engines in the command line.
If you want to view it through the web ui, run the following in separate terminals within the same environment:
```
set FLASK_APP=flask_app
flask run
```
```
python match.py
```
_(Yes this could have been in a windowed UI but I made this in 2 days I'm taking the easy route)_

## Making your own engine
Every engine should inherit the BaseEngine class from `engines\engine_base.py`. Really the only reason for this is to enforce that the `best_move()` method exists, and for type annotations. Your engine should also include a `name` variable for the engine's name, and a `player` variable for yours. These are purely used for display purposes.

The `best_move(...)` method returns a tuple containing the move and a dictionary for metadata. The metadata is completely optional and if you want, you can simply pass `{}`. I _might_ do something cool with an `'evaluation'` key in the dict- to take advantage of this please pass a float or int in that specific field, if you want to use that.

## Rules
**Game Rules:**
- Win is 1 point to winner, Draw is 0.5 points to both sides
- Games are run in pairs with both players switching sides between each game.
- Games are run in batches of 5 game pairs. 
- - If there is a >=2 point difference after the first 5 game pairs, the player with more points is declared the winner. 
- - Otherwise the threshold is reduced to 1 and 5 more pairs are run. 
- - If there is still no conclusive winner, the time is reduced to 25% (22.5s) per turn. 
- - If there is still no decisive winner, the match is considered a draw.
- Players have a hard limit of 100s per move- if the player takes longer that's considered a forfeit.
- There is a soft limit of 90s per move. Going above this limit grants the time exceeded to the opponent, multiplied by 1.5. (e.g. If one player exceeds the limit by 1s, the opponent is granted 1.5s of extra thinking time)
- If a player errors out of the game, that's also considered a forfeit (as long as the error is from their code)

**Code Rules:**
- You're free to optimize but keep it within python- don't start writing external libraries and running them from python (this includes cython)
- If you want to use a specific package, it needs to be put in the discord channel so others that didn't know abt it can use it. If you ask someone else to post for you that's fine as long as it's clear it relates to this
- Don't do too much chicanery- exploiting bugs is fine to an extent but if it's game-breaking pls don't
- - If there's a bug that allows you to lag out or interfere with the opponent that's completely off limits- keep your code contained
- Don't touch/interfere with the actual game code
- You're allowed to have separate engines for X (first move) and O (not first move) if you want to
- You can define an \_\_init__ with any parameters you like, which can be set at the start of the match. It's reccomended to include a random seed parameter if you use one- the game number will be passed to it to ensure predictability and variance between games.


**List of ext. packages in use**
- [Bitvector](https://pypi.org/project/BitVector/)
