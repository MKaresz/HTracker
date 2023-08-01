#  iu International University of Applied Science
#  name: Karoly Molnar
#  matriculation: 92113786
#  date: 2023
#

"""
HDisplay class to handle print out data to console

"""

import click

from htracker import HDisplayCategory
from htracker.h_data import Habit


class HDisplay:

    @staticmethod
    def display_habits(category: HDisplayCategory,
                       habits: list[Habit]
                       ) -> None:
        """Prints report to the console

        :param category: category enum class
        :type category: HDisplayCategory
        :param habits: ordered list of habit
        :type habits: list[Habits]

        """
        if len(habits) == 0:
            click.secho("No habits matching the criteria.", fg="yellow",
                        bold="true")
            return
        # print habit header first to display category, then data rows
        HDisplay.print_header(category)
        for habit in habits:
            HDisplay.print_habit_row(habit)

    @staticmethod
    def print_check_offs(category: HDisplayCategory,
                         habit: Habit) -> None:
        """Prints check-offs to the console of one Habit

        check-offs are a list in the habit list and do not fit into the
        normal habit display so separate display is needed.

        :param category: category enum class
        :type category: HDisplayCategory
        :param habit: contains the check-off list
        :type habit: Habit

        """
        # show the user the check-offs are from which habit
        cell_check_offs = "{:^18}"
        click.secho(category.value + " " + habit.name, fg="yellow",
                    bold="true")
        click.secho(
            cell_check_offs.format("Check-offs:") + "|",
            fg="white",
            bold="true"
        )
        click.secho(19 * "=", fg="blue", bold="true")
        # we like to print the check-offs in a column
        for check_off_date in habit.check_offs:
            cell_date = "{:^18}"
            click.secho(
                cell_date.format(str(check_off_date)) + "|",
                fg="white"
            )

    @staticmethod
    def print_streak(streak: int) -> None:
        """Prints the streaks after a check-off

        A short message to the user to let know his current streak right
        away when he enters a new check-off date.

        :param streak: the number of streak for a current habit
        :type streak: int

        """
        if streak > 0:
            click.secho(
                f"You are in a streak! {streak} times in a row!",
                fg="green",
                bold="true"
            )
        else:
            click.secho("Currently you are not in a streak. "
                        "But don't give up!",
                        fg="yellow",
                        bold="true")

    @staticmethod
    def print_header(category: HDisplayCategory) -> None:
        """Prints the header for Habit lists

        :param category: category for different prints
        :type category: HDisplayCategory

        """
        cell_name = "{:^50}"
        cell_date = "{:^18}"
        cell_periodicity = "{:^14}"
        cell_check_offs = "{:^13}"
        cell_streaks = "{:^12}"
        cell_struggle = "{:^11}"
        cell_on_track = "{:^13}"
        click.secho(category.value, fg="yellow", bold="true")
        click.secho(
            cell_name.format("Habit name:") + "|"
            + cell_date.format("Starting date:") + "|"
            + cell_periodicity.format("Periodicity:") + "|"
            + cell_check_offs.format("Check-offs:") + "|"
            + cell_streaks.format("Streaks:") + "|"
            + cell_struggle.format("Breaks:") + "|"
            + cell_on_track.format("On-track:") + "|",
            fg="white",
            bold="true"
        )
        click.secho(138 * "=", fg="blue", bold="true")

    @staticmethod
    def print_habit_row(
            habit: Habit
            ) -> None:
        """Prints a habit data in a row aligned like to the header

        :param habit: one habit to print
        :type habit: Habit

        """
        cell_name = "{:^50}"
        cell_date = "{:^18}"
        cell_periodicity = "{:^14}"
        cell_check_offs = "{:^13}"
        cell_streaks = "{:^12}"
        cell_struggle = "{:^11}"
        cell_on_track = "{:^13}"
        click.secho(
            cell_name.format(habit.name) + "|"
            + cell_date.format(str(habit.starting_date)) + "|"
            + cell_periodicity.format(str(habit.periodicity)) + "|"
            + cell_check_offs.format(len(habit.check_offs)) + "|"
            + cell_streaks.format(str(habit.streak)) + "|"
            + cell_struggle.format(str(habit.struggle)) + "|"
            + cell_on_track.format(str(int(habit.on_track * 100))
                                   + "%") + "|",
            fg="white"
        )
