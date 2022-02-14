Recruitment Pipeline
==========================================================

Welcome to my game of boggle. This is a REST api endpoint only game.

## Installation instructions

You need to have [Python](https://www.python.org/downloads/) to run this programme.
This project was created with Python 3.8.12 but any version above 3.7 and below 3.9
should work fine.

In the terminal, execute:

    $ python -m venv venv
    $ venv\Scripts\activate
    $ pip install -r requirements.txt
    $ python manage.py makemigrations
    $ python manage.py migrate
    $ python manage.py runserver 127.0.0.1:9001

Now the game is running on port 9001.
Note: you may have to replace "python" with "py" if you encounter any problems running the python scripts.


To run tests, execute:

    $ python manage.py test

## API Endpoints
CREATING A GAME
```
POST /games
```
- Parameters:
  + `duration` (required): the time (in seconds) that specifies the duration of
    the game
  + `random` (required): if `true`, then the game will be generated with random
    board.  Otherwise, it will be generated based on input.
  + `board` (optional): if `random` is not true, this will be used as the board
    for new game. If this is not present, new game will get the default board
    from `game\test_board.txt`
    
The logic for this api endpoint can be found in ```CreateGameView``` under ```game\views.py```.

PLAYING A GAME
```
PUT /games/:id
```
- Parameters:
  + `id` (required): The ID of the game
  + `token` (required): The token for authenticating the game
  + `word` (required): The word that can be used to play the game
  
The logic for this api endpoint can be found in ```PlayGameView``` under ```game\views.py```.

RETRIEVING A GAME INFO
```
GET /games/:id
```

- Parameters:
  + `id` (required): The ID of the game
  
The logic for this api endpoint can be found in ```PlayGameView``` under ```game\views.py```.

## Code Logic

- Database models

The logic for database models can be found under ```game\models.py```

There are three database models used for this game: ```Game```, ```Attempt``` and ```Board```.
Whenever a user creates a new game, he would necessarily need to provide board characters 
(for the board layout). Therefore a ```Board``` database entry would be created. As different users
may provide the same board layout, or not at all (default board used), the same board can be reused
for subsequent games. ```Board``` has also been kept separate from ```Game``` to allow memoization of
any words found for that ```Board```, and the expensive word finding engine need not be used as often.
```BoardData``` class is also used to sanitise any board layout string to ensure that they are in the
correct format, and they meet the requirements of a ```Board```(ascii letters + *)


For each game created, the board and duration would be saved in ```Game```. The current time would also be saved 
as start_time. For each game to be considered a valid game (non-expired), the current time will be subtracted against
start_time and compared with the duration.

Any proper valid moves made by a user will be saved as an ```Attempt``` entry. Any subsequent moves will
always check all current ```Game``` associated ```Attempt``` entries to ensure that no repeat words can be
submitted again. Each ```Attempt``` entry also holds the score of each move and thus the total score for
each game can be obtained by summing all current ```Game``` associated ```Attempt``` entries' score. Upon
deletion of any ```Game```, all associated ```Attempt``` entries will also be deleted. ```Attempt``` has 
been kept separate from ```Game``` to allow easy analysis of words and scores for each type of board.

- Word Finding Engine

The word finding engine resides under ```game\models.py``` under method ```Board.is_word_available```. 
Everytime a word is provided by user, it is checked under the memoized words in the ```Board```, if
it is not, then proceed to check against the list of words provided, if it is a valid word, then proceed to
use the expensive method ```Board.is_char_sequence_available```. 

```Board.is_char_sequence_available``` creates a dictionary with each char and the coordinate they belong to. 
Then create another dictionary ```move_num_w_positions```  with the move number as the keys. For example, if "HOPE" is given, then a dictionary 
(hash-map) of {0:[], 1:[], 2:[], 3: []} is created. Check the position on 1 character, and place all available positions
into key 0 of move_num_w_positions. Check the next character and check whether this character is adjacent to any of the 
last position in key 0. If there is any such character, append both positions in order into key 1. Repeat until all
the characters in the word have been accounted for. If there is a sequence once the final character is reached, this
sequence of character is found on the board! 