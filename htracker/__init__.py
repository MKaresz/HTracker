#  iu International University of Applied Science
#  name: Karoly Molnar
#  matriculation: 92113786
#  date: 2023.
#

"""Habit tracking CLI module

The module is able to store a habits, and save it to Json file.
Every habit can have a name, starting date a periodicity stored in
number of days, stores the check-off events in a date list, and
calculates a steak period from the events dates. Limitation is that you
can't have two habits with the same name, as the habits are identified
by their name.

Options:
  --help  :Show this message and exit.

Commands:
  about         :Prints application name and version number to the user.
  add-habit     :Add a new function to the habit list
  analyze       :Analyze habits sub-menu (with the following commands)
      periodicity   :Print habits by periodicity
      streak        :Print habit(s) by streak
  check-off     :Check-off a habit.
  list-habits   :Print all habits in database to the user.
  remove-habit  :Remove a habit from the habits list.

"""
import os
from enum import Enum
from pathlib import Path

# define module variables
__app_name__: str = "habit tracking app"
__version__: str = "0.1.0"

# we need a filepath to a folder what the user can write
FILE_PATH = Path.home().joinpath(
    "." + Path.home().stem + "_htracker.json"
)

# the path to the test data. We copy over the data upon user request
TEST_FILE_PATH = os.path.join(
    os.getcwd(),
    "AppData",
    "h_tracker_test_data.json"
)


# define custom error code categories
class HErrorCode(Enum):
    SUCCESS = "Operation successful."
    ABORTED = "Operation aborted."
    FILE_READ = "No existing database found."
    FILE_WRITE = "Database cannot be written."
    JSON_ERROR = "Database is corrupted."
    NAME_ERROR = "Habit name is not found in database."
    NAME_EXISTS = "Habit already exists in database."
    RUNTIME = "Fatal error program exits."
    START_DATE_ERROR = "Input date is earlier than check-off date."
    SAME_DATE_ERROR = "Input date was already checked-off."
    FUTURE_DATE_ERROR = "Input date is in the future."


# define display categories for console output
class HDisplayCategory(Enum):
    ALL = "Listing all habits:"
    PERIODICITY = "Habits listed by periodicity:"
    STREAK = "Habits listed by longest streak:"
    CHECK_OFFS = "Listing all check-off for habit:"
    STRUGGLE = "Habits listed by most breaks:"
