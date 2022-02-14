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


## Deployment

The repository is forked into a private repository and the deployment is done on Azure Cloud using the App Service using 
the App Service's CI/CD pipeline. 