import pytest
from pathlib import Path
from click.testing import CliRunner
from htracker.h_cli import main_menu
from htracker.__init__ import FILE_PATH, TEST_FILE_PATH


@pytest.fixture(scope="session")
def get_runner():
    runner = CliRunner()   
    return runner

@pytest.fixture(scope="session", autouse=True)
def prepare_testrun():
    # save the datafile of the app and load testdata
    temp_path =  Path.home().joinpath(
        "." + Path.home().stem + "_htracker.json"
        )
    if FILE_PATH.exists():
        with open(FILE_PATH, "r") as source, open(temp_path, "w") as target:
            target.write(source.read())

    with open(TEST_FILE_PATH, "r") as source, open(FILE_PATH, "w") as target:
        target.write(source.read())

    yield

    with open(temp_path, "r") as source, open(FILE_PATH, "w") as target:
        target.write(source.read())


@pytest.fixture
def restore_testdatabase():
    yield
    with open(TEST_FILE_PATH, "r") as source, open(FILE_PATH, "w") as target:
        target.write(source.read())
    
        
        

