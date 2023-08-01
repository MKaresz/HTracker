"""

_check_off_date_valid
_count_struggle
_count_missing_check_offs
_count_streaks
_calc_on_track

"""
import pytest
from htracker.h_tracker import HTracker
from htracker.h_data_manager import HDataManager
from datetime import date
from htracker import HErrorCode


@pytest.fixture
def htracker_obj():
    return HTracker()

@pytest.fixture
def habit():
    test_habit = HDataManager._json_to_habit(
        {
        "name": "AA Meeting",
        "starting_date": "2023-01-01",
        "periodicity": 7,
        "events": [
            "2023-01-01",
            "2023-01-08",
            "2023-01-15",
            "2023-01-22",
            "2023-01-29",
            "2023-05-05",
            "2023-05-12"
        ],
        "streak": 4,
        "on_track": 0.6666666666666666,
        "struggle": 1
    }
    )
    return test_habit

def test_check_off_date_valid_start(htracker_obj, habit):
    invalid_checkoff = date.fromisoformat('2019-12-04')
    error_code = htracker_obj._check_off_date_valid(habit, invalid_checkoff)
    assert error_code.value == HErrorCode.START_DATE_ERROR.value

def test_check_off_date_valid_duplicated(htracker_obj, habit):
    invalid_checkoff = date.fromisoformat("2023-05-12")
    error_code = htracker_obj._check_off_date_valid(habit, invalid_checkoff)
    assert error_code.value == HErrorCode.SAME_DATE_ERROR.value

def test_check_off_date_valid_future(htracker_obj, habit):
    invalid_checkoff = date.fromisoformat("2024-05-12")
    error_code = htracker_obj._check_off_date_valid(habit, invalid_checkoff)
    assert error_code.value == HErrorCode.FUTURE_DATE_ERROR.value
