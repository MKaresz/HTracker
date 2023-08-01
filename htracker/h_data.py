#  iu International University of Applied Science
#  name: Karoly Molnar
#  matriculation: 92113786
#  date: 2023
#

"""
Habit class to store one habit and relevant information

"""

from datetime import date
from typing import List


class Habit:
    def __init__(
            self,
            name="name",
            starting_date=date.today(),
            periodicity=1,
            check_offs=None,
            streak=0,
            on_track=1.0,
            struggle=0
    ):
        """Storing a habit data

        :param name: habit's name
        :type name: str
        :param starting_date: date the habit was entered into database
        :type starting_date: date
        :param periodicity: the reoccurring period in days
        :type periodicity: int
        :param check_offs: a list of dates for check-off events
        :type check_offs: list of dates
        :param streak: longest calculated streak
        :type streak: int
        :param struggle: no. of breaks from beginning of habit
        :type struggle: int
        """
        self.name = name
        self.starting_date = starting_date
        self.periodicity = periodicity
        self.check_offs: List[date] = check_offs if check_offs else []
        self.streak = streak
        self.on_track = on_track
        self.struggle = struggle
