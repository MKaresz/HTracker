#  iu International University of Applied Science
#  name: Karoly Molnar
#  matriculation: 92113786
#  date: 2023
#

"""
Module entry point to calls click decorated function

"""

from htracker import h_cli


def main() -> None:
    """Calls click decorated function.

    Click is a third party lib. from https://click.palletsprojects.com

    """
    h_cli.main_menu()


if __name__ == '__main__':
    main()
