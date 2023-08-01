# Htracker

HTracker is a Habit Tracker App. It's a stand-alone Back-End console application that helps the user to track and maintain good habits. Whether the user wants to workout, meditate, or learn a language, this application is there to help. It helps the user to stay on track and stay motivated. In this application, the user can create multiple habits and track their progress with a simple and intuitive command line interface. Habit Tracker App also analyzes the user's performance and shows their achieved streaks, breaks, and on-track value. With this Habit Tracker App, you can turn your aspirations into actions!

## Project Description
The Habit Tracker App is a stand-alone Back-End console application.  

A list of libraries used within the project:
* [Click](https://click.palletsprojects.com/en/8.1.x/): Version 8.1
* [pytest](https://docs.pytest.org/en/7.4.x/): Version 7.4.0


## Requirements

This module requires the followings:
* pytest 7.4
* click 8.1
* python 3.7+

## Installation
To install the htracker package from github, first clone the repository.

```git clone https://github.com/MKaresz/HTracker.git```

Then just run from that directory:

```pip install .```


All the required libraries will be installed.

## Usage
The user can use the console interface to interact with the application and perform various operations.

e.g.:
```"python -m htracker --help" -> to get the help text```

Every command has ```--help``` argument to display the available information on that command

e.g.: ```"python -m htracker add-habit --help"```


Or you can use the interactive CLI to enter the needed data into the application after running a command.

e.g.: ```"python -m htracker add-habit"```


### Available commands
```
├── htracker
    ├── about              -> Prints out the app name and version number
    ├── add-habit          -> Adds a new habit to your habit database.
    ├── add-random-habits  -> Adds random habits to your database.
    ├── analyse            -> Opens the analyse sub-menu.
        ├── on-track       -> List habits sorted by on-track in ascending or descending order
        ├── periodicity    -> List habits of a certain periodicity
        ├── streak         -> List all habits sorted by the longest streak
        ├── struggle       -> Returns the habit with the most break in its streak
    ├── check-off          -> Adds a new check-off date to one of your habits.
    ├── list-check-offs    -> Lists all the check off date for a habit.
    ├── list-habits        -> Lists all of your habits in database.
    ├── remove-all-habits  -> Deletes all of your habits.
    ├── remove-habit       -> Removes a habit from your habit database.
```

### Display help
***
Launch the program from the terminal.

```python -m htracker```

or

```python -m htracker --help```

### About the program
***
Get name and version of the application:

```python -m htracker about```  
       

### Add habit
***
Start the interactive 'add habit' process:

```python -m htracker add-habit```        

Or add habit with its features as options in one command line using -n name, -p periodicity, -d starting date.

```python -m htracker add-habit -n [name] -p [periodicity] -d [yyyy-mm-dd]```


### Remove a habit
***
Remove a habit in the guided remove habit process starting it with the remove-habit command:

```python -m htracker remove-habit```

Or remove a certain habit using the remove-habit command and the confirmation option -n name, -c confirmation ("Y" or "N").

```python -m htracker remove-habit -n jogging -c Y```


### Remove all habits
***
Use the 'remove-all-habits' command and in the next step confirm your choice:

```python -m htracker remove-all-habits```


Or remove all habits using the 'remove-all-habits' command and the confirmation option -c confirmation ("Y" or "N").

```python -m htracker remove-all-habits -c Y```


### Check off
***
Mark a habit completed for a period with the “check-off” command. Give the name and the date of completion in the next steps.

```python -m htracker check-off```


Mark a habit completed for a period with the “check-off” command by giving a -n name, -d date the date of completion.

```python -m htracker check-off -n [name] -d [yyyy-mm-dd]```

### List check offs

To list all of the check-offs for one habit use the “list-check-off“ command with the -n name argument.

```python -m htracker check-off```


### List habits
***
To get an overview of all of your habits we can use the "list-habits" command.

```python -m htracker list-habits```

### Analyse habits
***
In order to list the habits by categories, open the submenu with the “analyse“ command
and choose from the categories: periodicity, streak, struggle, or on-track.

To analyse periodicity 1 [num of days] habits use: -p 1

```pyhon -m htracker analyse periodicity -p 1```

To get all the habits ordered by "on-track": -s A or D for ascending or descending list.

```python -m htracker analyse on-track -s A```

To get habits sorted by the length of their streaks, use after analyse the "streak" command. Or if the name argument left empty it will list all of the habits. n- name.

```python -m htracker analyse streak -n```

To get the habit you struggled the most, use the 'struggle' command and give a date from you like to start the filter till today use -d and date with the following format [YYYY-MM-DD].

```python -m htracker analyse struggle -d 2023-01-01```

### Load test habits
***
To try out the application we can load in predefined habits, with the "load-test-habits" command and use -c confirmation ("Y" or "N"). Be careful as the new habits will overwrite any existing habits.

```python -m htracker analyse load-test-habits -c Y```


***
### Thank you!
Thank you for taking the time to try out my habit tracker application. I'm glad if you enjoyed using it and I hope it helps you achieve your goals.

I would love to hear your feedback on how I can improve the app and make it more useful. Please feel free to share your suggestions with me.