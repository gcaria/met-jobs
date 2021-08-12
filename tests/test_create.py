import os
import subprocess

import pytest


@pytest.fixture
def rootdir():
    return os.path.dirname(os.path.abspath(__file__))


def is_same_csv(actual, expected):

    with open(actual, "r") as t1, open(expected, "r") as t2:
        fileone = t1.readlines()
        filetwo = t2.readlines()

    for line in filetwo:
        if line not in fileone:
            return False
    return True


def test_database(rootdir):

    path_expected = os.path.join(rootdir, "test_create.csv")
    path_actual = os.path.join(rootdir, "test_create_tmp.csv")

    process = subprocess.run(
        ["create_db", path_actual, "--start", "2020-05", "--end", "2020-05"]
    )

    assert process.returncode == 0
    assert is_same_csv(path_actual, path_expected)

    os.remove(path_actual)

    process = subprocess.run(
        ["create_db", path_actual, "--start", "2020-04", "--end", "2020-04"]
    )

    assert process.returncode == 0
    assert not is_same_csv(path_actual, path_expected)

    os.remove(path_actual)
