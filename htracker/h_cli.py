#  iu International University of Applied Science
#  name: Karoly Molnar
#  matriculation: 92113786
#  date: 2023
#

"""
Handle user command line input

"""

from datetime import datetime, date

import click

from htracker import HErrorCode, TEST_FILE_PATH
from htracker import __app_name__, __version__
from htracker.h_data import Habit
from htracker.h_tracker import HTracker

# the component that handles the habit tracking logic
h_tracker = HTracker()


@click.group(help="""-- Welcome to the habit tracker app! -- \n
"Excellence, is not an act, but a habit." ~ Aristotle """)
def main_menu() -> None:
    """Main menu start

     dummy method for click group

     """
    pass


# @click.command(name="info: get about notes")
@main_menu.command(help="-> Prints out the app name and version number")
def about() -> None:
    """Prints the application name and version number to the user.

    """
    click.secho(
        f"The {__app_name__}, version:{__version__}", fg="yellow",
        bold="true"
    )


@main_menu.command(help="-> Adds a new habit to your habit database.")
@click.option(
    "-n", "--name",
    type=str,
    prompt="Habit name",
    help="Enter the name of the habit",
    default="My habit"
)
@click.option(
    "-p", "--period",
    type=int,
    prompt="Enter the period for the habit in days",
    help="Enter 1 for daily, or 7 for weekly periodicity.",
    default=1
)
@click.option(
    "-d", "--start_date",
    type=str,
    prompt="Enter starting date (YYYY-MM-DD) or hit Enter for today",
    help="Enter the starting date of your habit.",
    default=str(date.today())
)
def add_habit(name: str, period: int, start_date: str) -> None:
    """Adds a new habit to the habits database

    :param name: Name of habit
    :type name: str

    :param period: Habit periodicity in days
    :type period: int

    :param start_date: Start day of user habit
    :type start_date: date

    """
    # duplicated names need to be checked
    name_error_code = h_tracker.check_habit_name_exists(name)
    if (name_error_code == HErrorCode.NAME_ERROR) or \
            (name_error_code == HErrorCode.FILE_READ):
        # handle not correct date input format
        try:
            # create a new habit from the input
            new_habit = Habit(
                name,
                datetime.strptime(start_date, '%Y-%m-%d').date(),
                period,
                # we assume the start date is the first check-off date
                [datetime.strptime(start_date, '%Y-%m-%d').date()]
            )
            file_error_code = h_tracker.add_habit_to_database(new_habit)
            # different color based on error category
            fg_color = "green" if \
                file_error_code == HErrorCode.SUCCESS else "red"
            click.secho(file_error_code.value, fg=fg_color)
        except ValueError:
            click.secho(f"Wrong input format. "
                        + HErrorCode.RUNTIME.value,
                        fg="red")
            # fix: currently not known how to call back the date input
            # again, so exit
            ctx = click.Context(main_menu)
            click.Context.exit(ctx)
    else:
        click.secho(name_error_code.value, fg="red")


@main_menu.command(help="-> Removes a habit from your habit database.")
@click.option(
    "-n", "--name",
    type=str,
    prompt="Habit name",
    help="Enter the name of the habit"
)
@click.option(
    "-c", "--confirm",
    type=click.Choice(["Y", "N"], case_sensitive=False),
    prompt=click.style(
        "Are you sure you want to delete your habit",
        fg="red"
    ),
    help="Confirm that you want to delete your habit data"
)
def remove_habit(name, confirm) -> None:
    """Removes a habit from the habits database by name.

    :param name: the habit name to be deleted from habits database
    :type name: str
    :param confirm: user confirmation
    :type confirm: str

   """
    # input is set to non-case-sensitive
    if confirm.lower() == "n":
        click.secho(HErrorCode.ABORTED.value, fg="red")
        return
    # check if the habit really exists in db
    name_error_code = h_tracker.check_habit_name_exists(name)
    if name_error_code == HErrorCode.NAME_EXISTS:
        file_error_code = h_tracker.remove_habit_from_database(name)
        # different color based on error category
        fg_color = "green" if file_error_code == HErrorCode.SUCCESS \
            else "red"
        click.secho(file_error_code.value, fg=fg_color)
    else:
        click.secho(HErrorCode.NAME_ERROR.value, fg="red")


@main_menu.command(
    help="-> Adds a new check-off date to one of your habits."
)
@click.option(
    "-n", "--name",
    type=str,
    prompt="Habit name",
    help="Enter the name of the habit"
)
@click.option(
    "-d", "--check_date",
    type=str,
    prompt="Enter starting date (YYYY-MM-DD) or hit Enter for today",
    help="Enter the starting date (YYYY-MM-DD) of your habit:",
    default=str(date.today())
)
def check_off(name, check_date) -> None:
    """Checks-off an event for a habit.

    :param name: Habit name to be checked-off
    :type name: str
    :param check_date: Date of check-off
    :type check_date: str

    """
    # check if the habit really exists in db
    name_error_code = h_tracker.check_habit_name_exists(name)
    if name_error_code == HErrorCode.NAME_EXISTS:
        # handle not correct date input format
        try:
            error_code = h_tracker.check_off(
                name,
                datetime.strptime(check_date, '%Y-%m-%d').date()
            )
            # different color based on error category
            fg_color = "green" if error_code == HErrorCode.SUCCESS \
                else "red"
            click.secho(error_code.value, fg=fg_color)
        except ValueError:
            click.secho(f"Wrong date format. "
                        + HErrorCode.RUNTIME.value,
                        fg="red")
            # fix: currently not known how to call back the date input
            # again, so exit
            ctx = click.Context(main_menu)
            click.Context.exit(ctx)
    else:
        click.secho(name_error_code.value, fg="red")


# todo move to h_tracker
@main_menu.command(help="-> Lists all of your habits in database.")
def list_habits() -> None:
    """Prints to console all habits in database to the user.

    """
    error_code = h_tracker.list_all_habits()
    fg_color = "green" if error_code == HErrorCode.SUCCESS else "red"
    click.secho(error_code.value, fg=fg_color)


# todo move to h_tracker
@main_menu.command(help="-> Lists all the check off date for a habit.")
@click.option(
    "-n", "--name",
    type=str,
    prompt="Habit name",
    help="Enter the name of the habit"
)
def list_check_offs(name: str) -> None:
    """Prints to console all check-off dates of a given habit.

    :param name: name of the habit to print the check-off list
    :type name: str

    """
    error_code = h_tracker.list_all_check_off(name)
    # different color based on error category
    if error_code == HErrorCode.SUCCESS:
        fg_color = "green"
    else:
        fg_color = "red"
    click.secho(error_code.value, fg=fg_color)


@main_menu.command(help="-> Deletes all of your habits.")
@click.option(
    "-c", "--confirm",
    type=click.Choice(["Y", "N"], case_sensitive=False),
    prompt=click.style(
        "Are you sure you want to delete all of your habits",
        fg="red"
    ),
    help="Confirm that you want to delete all of your habits"
)
def remove_all_habits(confirm) -> None:
    """Deletes the database. Can be useful if the file gets corrupted

    :param confirm: user confirmation
    :type confirm: str

   """
    # give the possibility to use lower case letter as well
    if confirm.lower() == "n":
        click.secho(HErrorCode.ABORTED.value, fg="red")
        return
    error_code = h_tracker.delete_habit_database()
    # different color based on error category
    fg_color = "green" if error_code == HErrorCode.SUCCESS else "red"
    click.secho(error_code.value, fg=fg_color)


@main_menu.group(help="-> Opens the analyse sub-menu.")
def analyse() -> None:
    """Analyse habits sub-menu

     dummy method for click sub-menu

     """
    pass


@analyse.command(
    help="-> Prints habits based on the entered longest streak."
)
@click.option(
    "-n", "--name",
    type=str,
    prompt="Name habit for longest streak, "
           "or hit Enter for all habits streak",
    help="Display longest streak of habit(s).",
    default=""
)
def streak(name: str) -> None:
    """Prints to the console the given habit's longest streak,
    or if no name is given than all habit's longest streaks.

    :param name: Habit name to be checked-off
    :type name: str

    """
    name_error_code = h_tracker.check_habit_name_exists(name)
    if name_error_code == HErrorCode.NAME_EXISTS or name == "":
        error_code = h_tracker.analyse_streak(name)
        # different color based on error category
        fg_color = "green" if error_code == HErrorCode.SUCCESS \
            else "red"
        click.secho(error_code.value, fg=fg_color)
    else:
        click.secho(name_error_code.value, fg="red")


@analyse.command(
    help="-> Prints habits based on the entered periodicity."
)
@click.option(
    "-p", "--period",
    type=int,
    prompt="Give periodicity to filter your habits",
    default=1
)
def periodicity(period: int) -> None:
    """Prints habits filtered by periodicity

    :param period: period of habit to show
    :type period: int

    """
    error_code = h_tracker.analyse_periodicity(period)
    # different color based on error category
    fg_color = "green" if error_code == HErrorCode.SUCCESS else "red"
    click.secho(error_code.value, fg=fg_color)


@analyse.command(
    help="-> A percent value based on how good the habit is on-track."
)
@click.option(
    "-s", "--sort",
    type=click.Choice(['A', 'D'], case_sensitive=False),
    prompt=click.style(
        "Ascending or descending order",
        fg="red"
    ),
    help="Display habits based on on-track.",
    default='A'
)
def on_track(sort: str) -> None:
    """Calculates an on-track value based on streaks and breaks.
    The order of habits can be changes to show the most success or
    least success habit first

    :param sort: ascending or descending order
    :type sort: str

    """
    error_code = h_tracker.analyse_on_track(sort.lower())
    # different color based on error category
    fg_color = "green" if error_code == HErrorCode.SUCCESS else "red"
    click.secho(error_code.value, fg=fg_color)


@analyse.command(
    help="-> Analyse struggle by habits between today and a given date."
)
@click.option(
    "-d", "--in_date",
    type=str,
    prompt="Enter starting date (YYYY-MM-DD) or hit Enter for today",
    help="Analyse struggle by habits between today and a given date.",
    default=str(date.today())
)
def struggle(in_date: str) -> None:
    """Analyse struggle by habits between today and a given date

    It calculates the breaks and the missed check-offs till today.
    if today has not check-off it will count as break

    :param in_date: date in past
    :type in_date: date

    """
    # handle not correct date input format
    try:
        # need to convert the str to date format for easy compare
        past_date = datetime.strptime(in_date, '%Y-%m-%d').date()
        # util function to calc breaks and missing check-off
        error_code = h_tracker.analyse_struggle(past_date)
        # different color based on error category
        if error_code == HErrorCode.SUCCESS:
            fg_color = "green"
        else:
            fg_color = "red"
        click.secho(error_code.value, fg=fg_color)
    except ValueError:
        click.secho(f"Wrong date format. "
                    + HErrorCode.RUNTIME.value,
                    fg="red")
        # fix: currently not known how to call back the date input again
        # so exit
        ctx = click.Context(analyse)
        click.Context.exit(ctx)


@main_menu.command(
    help="-> Overwrites your habits with pre-defined test habits."
)
@click.option(
    "-c", "--confirm",
    type=click.Choice(["Y", "N"], case_sensitive=False),
    prompt=click.style(
        "Do you want replace your habits with predefined test habits?",
        fg="red"
    ),
    help="Confirm that you want to overwrite your habit data!"
)
def load_test_habits(
        confirm: str
) -> None:
    """Replaces your database with predefined habits for testing

    :param confirm: user confirmation
    :type confirm: str

    """
    # input is set to non-case-sensitive
    if confirm.lower() == "n":
        click.secho(HErrorCode.ABORTED.value, fg="red")
        return
    error_code = h_tracker.import_database(TEST_FILE_PATH)
    # different color based on error category
    fg_color = "green" if error_code == HErrorCode.SUCCESS else "red"
    click.secho(error_code.value, fg=fg_color)
