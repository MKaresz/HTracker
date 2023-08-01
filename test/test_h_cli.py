#  iu International University of Applied Science
#  name: Karoly Molnar
#  matriculation: 92113786
#  date: 2023
#

import pytest

from htracker import HErrorCode
from htracker.h_cli import main_menu
from htracker import __app_name__, __version__


def test_about(get_runner):
    result = get_runner.invoke(main_menu, ["about"])
    expected = f"The {__app_name__}, version:{__version__}"
    assert result.output.rstrip() == expected

def test_help(get_runner):
    result = get_runner.invoke(main_menu, ["--help"])
    expected = f"Usage:"
    assert expected in result.output

def test_remove_habit(get_runner):
    # create a habit
    result = get_runner.invoke(main_menu, ["add-habit", "-n", "test_habit", "-p", "3", "-d", "1970-03-04"])
    expected = HErrorCode.SUCCESS.value
    created = result.output.rstrip() == expected

    # delete the habit
    result = get_runner.invoke(main_menu, [
        "remove-habit",
        "-n",
        "test_habit",
        "-c"
        "Y"
    ]
                               )
    deleted = HErrorCode.SUCCESS.value in result.output
    assert all((created, deleted))

@pytest.mark.parametrize("name, period, starting_date",
                         [("habit1", "1", "1970-03-04"),
                          ("habit2", "2", "1971-03-04"),
                          ("habit3", "3", "1972-03-04")])
def test_add_habit(get_runner, name, period, starting_date):
    result = get_runner.invoke(main_menu, [
        "add-habit",
        "-n",
        name,
        "-p",
        period,
        "-d",
        starting_date
    ]
                               )
    assert HErrorCode.SUCCESS.value in result.output


def test_delete_db_aborted(get_runner):
    result = get_runner.invoke(main_menu, ["remove-all-habits", "-c", "n"])
    assert result.exit_code == 0
    assert HErrorCode.ABORTED.value in result.output


def test_delete_all_habits(get_runner, restore_testdatabase):
    result = get_runner.invoke(main_menu, ["remove-all-habits", "-c", "y"])
    assert result.exit_code == 0
    assert HErrorCode.SUCCESS.value in result.output

def test_check_off(get_runner):
    result = get_runner.invoke(main_menu, ["add-habit", "-n", "jogging", "-p", "7", "-d", "2023-07-01"])
    result = get_runner.invoke(main_menu, ["check-off", "-n", "jogging", "-d", "2023-07-08"])
    assert result.exit_code == 0
    assert HErrorCode.SUCCESS.value in result.output

def test_analyse_streak(get_runner):
    result = get_runner.invoke(main_menu, ["analyse", "streak", "-n", "AA Meeting"])
    assert result.exit_code == 0
    assert HErrorCode.SUCCESS.value in result.output

def test_analyse_struggle(get_runner):
    result = get_runner.invoke(main_menu, ["analyse", "struggle", "-d", "2023-01-08"])
    assert result.exit_code == 0
    assert HErrorCode.SUCCESS.value in result.output

def test_analyse_periodicity(get_runner):
    result = get_runner.invoke(main_menu, ["analyse", "periodicity", "-p", "1"])
    assert result.exit_code == 0
    assert HErrorCode.SUCCESS.value in result.output


def test_analyse_ontrack(get_runner):
    result = get_runner.invoke(main_menu, ["analyse", "on-track", "-s", "A"])
    assert result.exit_code == 0
    assert HErrorCode.SUCCESS.value in result.output

def test_list_habitsk(get_runner):
    result = get_runner.invoke(main_menu, ["list-habits"])
    assert result.exit_code == 0
    assert HErrorCode.SUCCESS.value in result.output

def test_list_check_offs(get_runner):
    result = get_runner.invoke(main_menu, ["list-check-offs", "-n", "AA Meeting"])
    assert result.exit_code == 0
    assert HErrorCode.SUCCESS.value in result.output

def test_habit_exists(get_runner):
    _ = get_runner.invoke(main_menu, ["add-habit", "-n", "repeathabit", "-p", "3", "-d", "1980-03-04"])
    result = get_runner.invoke(main_menu, ["add-habit", "-n", "repeathabit", "-p", "3", "-d", "1980-03-04"])
    assert result.exit_code == 0
    assert HErrorCode.NAME_EXISTS.value in result.output