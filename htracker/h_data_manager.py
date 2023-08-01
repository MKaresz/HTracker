#  iu International University of Applied Science
#  name: Karoly Molnar
#  matriculation: 92113786
#  date: 2023
#

"""
HDataManager class to handle database functionalities:
load, save and convert from and to json format

"""
import json
import os
from datetime import datetime

from htracker import FILE_PATH
from htracker import HErrorCode
from htracker.h_data import Habit


class HDataManager:
    """ Habit data manager class.

    Responsible to handle data loading, saving and convert it back and
    forth to json.

    """

    @staticmethod
    def delete_database() -> HErrorCode:
        """Deleting the database

        Database can be corrupted returns True if file was deleted

        :return: HErrorCode

        """
        # file can be read-only
        try:
            print(FILE_PATH)
            os.remove(FILE_PATH)
            return HErrorCode.SUCCESS
        except OSError:
            return HErrorCode.FILE_WRITE

    @staticmethod
    def load_database(path: str = FILE_PATH) \
            -> (HErrorCode, dict[Habit]):
        """Loads habits database from disk

        loads the existing database from disk, if no database exists
        will return an empty dictionary

        :param path: load database path
        :type path: str

        :return HErrorCode, dict[Habit] :
                            HErrorCode Enum, user-friendly
                            error codes defined in __init__,
                            dictionary {name(str):Habit} storing name
                            and habit class objects pairs

       """
        # make an empty dict to give it back if no db exists
        new_habits = {}
        try:
            with open(path, "r") as \
                    read_file:
                try:
                    habits_json = json.load(read_file)
                    for json_habit_key in habits_json:
                        new_habits[json_habit_key] = \
                            HDataManager._json_to_habit(
                                habits_json[json_habit_key]
                            )
                except json.decoder.JSONDecodeError:
                    return HErrorCode.JSON_ERROR, new_habits
            return HErrorCode.SUCCESS, new_habits
        except FileNotFoundError:
            return HErrorCode.FILE_READ, new_habits
        except OSError:
            raise RuntimeError(
                "Unable to handle error, program will terminate."
            )

    @staticmethod
    def save_database(habits: dict[Habit]) -> HErrorCode:
        """Saves a habit dictionary to the disk

        :param habits: storing name and habit pairs
        :type habits: dictionary of {name(str):Habit} pairs

        :return: HErrorCode

        """
        try:
            json_data = {}
            for habit_key in habits:
                json_data[habit_key] = HDataManager. \
                    _habit_to_json(habits[habit_key])
            with open(FILE_PATH, "w") as write_file:
                json.dump(json_data, indent=4, fp=write_file)
            return HErrorCode.SUCCESS
        except OSError:
            return HErrorCode.FILE_WRITE

    @staticmethod
    def _habit_to_json(habit: Habit) -> dict:
        """Convert Habit to json data

        :param habit: Habit

        :return: dictionary of {name(str):Habit} pairs

        """
        return {
            "name": habit.name,
            "starting_date": str(habit.starting_date),
            "periodicity": habit.periodicity,
            "events": [str(event) for event in habit.check_offs],
            "streak": habit.streak,
            "on_track": habit.on_track,
            "struggle": habit.struggle
        }

    @staticmethod
    def _json_to_habit(json_data) -> Habit:
        """Convert json data to Habit obj

        :param json_data: json data of one Habit

        :return: Habit

        """
        habit = Habit()
        habit.name = json_data["name"]
        habit.starting_date = datetime.strptime(
            json_data["starting_date"], '%Y-%m-%d').date()
        habit.periodicity = json_data["periodicity"]
        habit.check_offs = [datetime.strptime(event, '%Y-%m-%d').date()
                            for event in json_data["events"]]
        habit.streak = json_data["streak"]
        habit.on_track = json_data["on_track"]
        habit.struggle = json_data["struggle"]
        return habit
