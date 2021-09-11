import os
import subprocess

import numpy as np
import pytest

from met_jobs.search import Search


def test_length():

    search = Search("foo", n_results=5)
    assert len(search.first_results) == 5


def test_wrong_db_path():

    with pytest.raises(FileNotFoundError):
        Search("foo", path_db="not_a_path.csv")


def test_interval_dates():

    # only pass start date
    search = Search("foo", start="2015-01-01")
    assert min(search.df["date"] >= np.datetime64("2015-01-01"))

    # only pass end date
    search = Search("foo", end="2015-01-01")
    assert max(search.df["date"] <= np.datetime64("2015-01-01"))

    # pass both dates with wrong values
    with pytest.raises(ValueError, match=r".* can not be after .*"):
        Search("foo", start="2019-01-01", end="2015-01-01")

    # pass both dates with correct values
    search = Search("foo", end="2019-01-01", start="2015-01-01")
    assert min(search.df["date"] >= np.datetime64("2015-01-01"))
    assert max(search.df["date"] <= np.datetime64("2019-01-01"))


def test_by_argument():

    with pytest.raises(ValueError, match=r".* argument, choose .*"):
        Search("foo", by="funniest").df

    search = Search("foo", by="newest")
    assert search.df["date"].is_monotonic_decreasing
    assert search.df["title"].str.contains("foo", case=False).all()

    search = Search("foo", by="oldest")
    assert search.df["date"].is_monotonic_increasing
    assert search.df["title"].str.contains("foo", case=False).all()


@pytest.fixture
def rootdir():
    return os.path.dirname(os.path.abspath(__file__))


@pytest.mark.xfail
def test_script_execution(rootdir):
    path_db = os.path.join(rootdir, "test_create.csv")
    process = subprocess.run(["search_met", "foo", "-d", path_db], capture_output=True)
    expected = (
        "1)   Postdoctoral fellow position at Hanyang University - updates             "
        "   - 31-05-2020\nhttps://www.lists.rdg.ac.uk/archives/met-jobs/2020-05/msg00069.html\n\n\n2)"  # noqa: E501
        "   Postdoctoral Fellow in Atmosphere, Oceanography or Climate science - Rom..."
        " - 14-05-2020\nhttps://www.lists.rdg.ac.uk/archives/met-jobs/2020-05/msg00025.html\n\n\n3)"  # noqa: E501
        "   DTN- Meteorologist vacancy                                                 "
        " - 11-05-2020\nhttps://www.lists.rdg.ac.uk/archives/met-jobs/2020-05/msg00017.html\n\n\n4)"  # noqa: E501
        "   Assistant Professor climate change, flood/drought-risk, data-driven methods"
        " - 12-05-2020\nhttps://www.lists.rdg.ac.uk/archives/met-jobs/2020-05/msg00020.html\n\n\n5)"  # noqa: E501
        "   Post-doc position on Forecasting of Water Variables                        "
        " - 12-05-2020\nhttps://www.lists.rdg.ac.uk/archives/met-jobs/2020-05/msg00021.html\n\n\n6)"  # noqa: E501
        "   DWD: Mitarbeiter/in (m/w/d) im Sachgebiet Entwicklung meteorologischer D..."
        " - 13-05-2020\nhttps://www.lists.rdg.ac.uk/archives/met-jobs/2020-05/msg00022.html\n\n\n7)"  # noqa: E501
        "   Ph.D. student position on machine learning in meteorology at the Univers..."
        " - 14-05-2020\nhttps://www.lists.rdg.ac.uk/archives/met-jobs/2020-05/msg00023.html\n\n\n8)"  # noqa: E501
        "   Technisch-wissenschaftliche/r MA/in: Wissenschaftliches Rechnen/HPC        "
        " - 14-05-2020\nhttps://www.lists.rdg.ac.uk/archives/met-jobs/2020-05/msg00024.html\n\n\n9)"  # noqa: E501
        "   FW: RP3                                                                    "
        " - 14-05-2020\nhttps://www.lists.rdg.ac.uk/archives/met-jobs/2020-05/msg00029.html\n\n\n10)"  # noqa: E501
        '  Ph-D thesis in France "Modelling studeies of the chlorine atmospheric ch...'
        " - 11-05-2020\nhttps://www.lists.rdg.ac.uk/archives/met-jobs/2020-05/msg00019.html\n"  # noqa: E501
    )
    actual = process.stdout.decode()
    result = actual == expected
    print("\n" + actual)
    assert result
