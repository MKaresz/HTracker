#  iu International University of Applied Science
#  name: Karoly Molnar
#  matriculation: 92113786
#  date: 2023
#

"""
HTracker main logic to handle other components

"""
from datetime import date, timedelta

from htracker import HDisplayCategory, HErrorCode
from htracker.__init__ import FILE_PATH
from htracker.h_data import Habit
from htracker.h_data_manager import HDataManager
from htracker.h_display import HDisplay


class HTracker:

    def __init__(self):
        pass

    def load_habits_database(self, path: str = FILE_PATH) -> \
            (HErrorCode, dict[Habit]):
        """Loads habits from database

        :return dict[Habit]: dictionary of {name(str):Habit} pairs

        """
        return HDataManager.load_database(path)

    def delete_habit_database(self) -> HErrorCode:
        """ Deletes the database

        I can occur it gets corrupted

        :return: HErrorCode

        """
        return HDataManager.delete_database()

    def import_database(self, path: str) -> HErrorCode:
        error_code, habits = self.load_habits_database(path)
        if error_code == HErrorCode.SUCCESS:
            return HDataManager.save_database(habits)

    def check_habit_name_exists(self, name) -> HErrorCode:
        """Checks if the input habit name exists in the database

        :param name: name of habit
        :type name: str

        :return: HErrorCode

        """
        error_code, loaded_habits = HDataManager.load_database()
        if error_code == HErrorCode.SUCCESS:
            if name in loaded_habits:
                return HErrorCode.NAME_EXISTS
            else:
                return HErrorCode.NAME_ERROR
        else:
            return error_code

    def add_habit_to_database(self, habit: Habit) -> HErrorCode:
        """Adds a new habit to the database

        :param habit: Habit to be added
        :type habit: Habit

        :return: HErrorCode

        """
        error_code, habits = HDataManager.load_database()
        if (error_code == HErrorCode.SUCCESS) or \
                (error_code == HErrorCode.FILE_READ):
            habits[habit.name] = habit
            return HDataManager.save_database(habits)
        else:
            return error_code

    def remove_habit_from_database(self, name: str) -> HErrorCode:
        """Removes a habit from database

        :param name: name of the habit to be removed
        :type name: str

        :return HErrorCode:

        """
        error_code, habits = self.load_habits_database()
        if error_code == HErrorCode.SUCCESS:
            habits.pop(name)
            HDataManager.save_database(habits)
        return error_code

    def check_off(self, name: str, in_date: date) -> HErrorCode:
        """Adds a check-off date to a habit

        :param name: habit name
        :type name: str
        :param in_date: date of check-off
        :type in_date: date

        :return: HErrorCode

        """
        error_code, habits = self.load_habits_database()
        if error_code == HErrorCode.SUCCESS:
            # not expecting KeyError as it was checked in h_cli
            habit = habits[name]
            name_error = self._check_off_date_valid(
                habit,
                in_date
            )
            if name_error != HErrorCode.SUCCESS:
                return name_error
            habit.check_offs.append(in_date)
            # for querying is better to have this list shorted
            # longest_streak, current_streak
            habit.check_offs.sort()
            # store longest streak in db for display
            streaks = \
                self._count_streaks(habit)
            habit.streak = streaks[0]
            # give user feedback on current streaks
            HDisplay.print_streak(streaks[1])
            habit.on_track = \
                self._calc_on_track(habit)
            # store breaks in db for display
            habit.struggle = self._count_struggle(
                habit,
                habit.starting_date
            )
            return HDataManager.save_database(habits)
        else:
            return error_code

    def analyse_streak(self, name) -> HErrorCode:
        """calculates the streak of habit with a given name or all
        habits

        :param name: name of habit
        :type name: str

        :return: HErrorCode

        """
        error_code, habits = self.load_habits_database()
        if error_code == HErrorCode.SUCCESS:
            if name:
                filtered_habits = [habits[name]]
                HDisplay.display_habits(
                    HDisplayCategory.STREAK,
                    filtered_habits
                )
            else:
                shorted_habits = sorted(
                    habits.items(),
                    key=lambda item: item[1].streak,
                    reverse=True
                )
                HDisplay.display_habits(
                    HDisplayCategory.STREAK,
                    [habit[1] for habit in shorted_habits]
                )
            return HErrorCode.SUCCESS
        else:
            return error_code

    def analyse_periodicity(self, period) -> HErrorCode:
        """Makes a list of all habits with the given periodicity

        :param period: number of days for periodicity
        :type period: int

        :return: HErrorCode

        """
        error_code, habits = self.load_habits_database()
        if error_code == HErrorCode.SUCCESS:
            filtered_habits = []
            for habit in habits:
                if habits[habit].periodicity == period:
                    filtered_habits.append(habits[habit])
            HDisplay.display_habits(
                HDisplayCategory.PERIODICITY,
                filtered_habits
            )
        return error_code

    def analyse_on_track(self, sort: str) -> HErrorCode:
        """Makes a list of all habits based on order of on-track

        :param sort: ascending or descending order
        :type sort: str

        :return: HErrorCode

        """
        error_code, habits = self.load_habits_database()

        if error_code == HErrorCode.SUCCESS:
            if sort == "a":
                shorted_habits = sorted(
                    habits.items(),
                    key=lambda item: item[1].on_track,
                    reverse=False
                )
                HDisplay.display_habits(
                    HDisplayCategory.STREAK,
                    [habit[1] for habit in shorted_habits]
                )
            elif sort == "d":
                shorted_habits = sorted(
                    habits.items(),
                    key=lambda item: item[1].on_track,
                    reverse=True
                )
                HDisplay.display_habits(
                    HDisplayCategory.STREAK,
                    [habit[1] for habit in shorted_habits]
                )
            return HErrorCode.SUCCESS
        else:
            return error_code

    def analyse_struggle(self, in_date: date) -> HErrorCode:
        """Makes an ordered list from the habits based on struggle value
        the start time range is given by the user and capped today.

        :param in_date: filter start date to today
        :type in_date: date

        :return: HErrorCode

        """

        error_code, habits = self.load_habits_database()
        for habit in habits:
            breaks_db = self._count_struggle(habits[habit], in_date)
            breaks_time = self._count_missing_check_offs(habits[habit],
                                                         in_date)
            habits[habit].struggle = (breaks_db + breaks_time)
        shorted_habits = sorted(
            habits.items(),
            key=lambda item: item[1].struggle,
            reverse=True
        )
        HDisplay.display_habits(
            HDisplayCategory.STRUGGLE,
            [habit[1] for habit in shorted_habits]
        )
        return HErrorCode.SUCCESS

    def list_all_habits(self) -> HErrorCode:
        error_code, habits = self.load_habits_database()
        if error_code == HErrorCode.SUCCESS:
            if habits:
                HDisplay.display_habits(
                    HDisplayCategory.ALL,
                    list(habits.values())
                )
        return error_code

    def list_all_check_off(self, name: str) -> HErrorCode:
        """

        :param name:
        :return:
        """
        name_error_code = self.check_habit_name_exists(name)
        if name_error_code == HErrorCode.NAME_EXISTS:
            error_code, habits = self.load_habits_database()
            if error_code == HErrorCode.SUCCESS:
                HDisplay.print_check_offs(HDisplayCategory.CHECK_OFFS,
                                          habits[name]
                                          )
            else:
                return error_code
        return HErrorCode.SUCCESS

    def _check_off_date_valid(
            self,
            habit: Habit,
            check_off_date: date
    ) -> HErrorCode:
        """Utility method to check if the given date is valid:
            - not set before starting date
            - not a duplicated check-off date

        :param habit: habit object storing attributes of a habit
        :type habit: habit
        :param check_off_date: date the habit is checked-off
        :type check_off_date: date

        :return: HErrorCode

        """
        # one can't check-off a date before starting the habit
        if habit.starting_date > check_off_date:
            return HErrorCode.START_DATE_ERROR
        # from design, we don't allow duplicated entry
        if check_off_date in habit.check_offs:
            return HErrorCode.SAME_DATE_ERROR
        # no way to put future dated in as input
        if date.today() < check_off_date:
            return HErrorCode.FUTURE_DATE_ERROR
        return HErrorCode.SUCCESS

    def _count_struggle(self, habit: Habit, in_date: date) -> int:
        """Count the streak breaks in the habit check-off date list
        starting from in_date

        :param habit: habit object storing attributes of a habit
        :type habit: habit
        :param in_date: a habit entry
        :type in_date: date

        :return: int

        """
        periodicity: int = habit.periodicity
        habit_break = 0
        # as we shift the idx by +1 we need to have one less idx
        for idx in range(len(habit.check_offs) - 1):
            if habit.check_offs[idx] < in_date:
                continue
            # need to compare the previous and the current idx date
            if (
                    habit.check_offs[idx + 1] - habit.check_offs[idx]
            ).days != periodicity:
                habit_break += 1
        return habit_break

    def _count_missing_check_offs(self, habit: Habit,
                                  in_date: date) -> int:
        """Count missing check-offs from the last check-off to in_date

        :param habit: habit object storing attributes of a habit
        :type habit: habit
        :param in_date: a habit entry
        :type in_date: date

        :return: int

        """
        delta_periodicity = timedelta(days=int(habit.periodicity))
        habit_break = 0
        last_date = habit.check_offs[-1]
        # step forward with the periodicity till today
        while last_date < date.today():
            last_date += delta_periodicity
            if last_date < in_date:
                continue
            # if no check-off for today we will have breaks = 1
            # let's count for every skipped period
            habit_break += 1
        return habit_break

    def _count_streaks(self, habit: Habit) -> int():
        """Count the longest and the actual streaks for a habit
         using the check-off date list

        :param habit: habit object storing attributes of a habit
        :type habit: habit

        :return: int(longest_streak, current_streak)

        """
        periodicity: int = habit.periodicity
        longest_streak = 0
        current_streak = 0
        for idx in range(len(habit.check_offs) - 1):
            if (
                    habit.check_offs[idx + 1] - habit.check_offs[idx]
            ).days == periodicity:
                current_streak += 1
            else:
                current_streak = 0
            if current_streak > longest_streak:
                longest_streak = current_streak
        return longest_streak, current_streak

    def _calc_on_track(self, habit: Habit) -> float:
        """Calculate the on-track percentage value

        :param habit: habit object storing attributes of a habit
        :type habit: habit

        :return: float in range of 0.0 - 1.0

        """
        # need to reduce the check-offs by 1 to exclude the start date
        # of the habit we can't count streak on just one date
        # we have to add the missing check-off till today
        return habit.streak / (
                len(habit.check_offs)
                - 1
                + self._count_missing_check_offs(
                                habit,
                                habit.starting_date
                                )
                            )
