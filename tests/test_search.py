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
