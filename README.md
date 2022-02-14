Recruitment Pipeline
==========================================================

Welcome to my interpretation of a recruitment pipeline web application.

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

## Starting up

Before you begin, execute:

    $ python initial_script.py

This will set up some initial data in your local database.

To login as a user, choose either one of the following:
  - Username: user1, password: password12345
  - Username: user2, password: password12345

To login as a recruiter, choose either one of the following:
  - Username: recruiter1, password: password12345
  - Username: recruiter2, password: password12345


## Pipeline Logic

The logic for the recruitment pipeline is mainly controlled by three database models: ```Application```, ```Task``` and ```Job```

All ```Application``` instances would necessarily reference a ```Job``` instance. When a job seeker applies for a job,
an ```Application``` entry is created, along with one ```Task```. A new ```Task``` entry is always created whenever
a new ```Application``` entry is created, or the stage of an ```Application``` entry is altered. This will ensure that
the recruiter will keep track of what he needs to do before proceeding to move the application to the next stage. Also,
upon applying for a new job, the ```Application``` entry will not have any recruiter tagged to it, but will be flagged out
on the dashboard for all recruiters to take over the case as soon as possible.

Whenever a recruiter wants to move the application to the next stage, he will be forced to complete all existing tasks,
before the application stage can be changed. This is controlled both in the frontend and backend. As mentioned in the
previous paragraph, whenever a recruiter moves the application to the next stage, a new ```Task``` entry will be automatically
created. The Tasks and next_stage for application stages are found as class variables in ```Application```. No more tasks
and further action by recruiter will be required when the application stage moves to either REJECTED or HIRED.


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