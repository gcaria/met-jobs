"""Tools to query database."""
import os
from functools import cached_property

import pandas as pd
from dateutil import parser
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

dirname = os.path.dirname(__file__)
PATH_DEFAULT = f"{dirname}/database.csv"


class Search:
    """Perform search and prepare dataframe results for display, using
    provided input.
    """

    def __init__(
        self, query, path_db=None, start=None, end=None, by="best", n_results=10
    ):

        self.query = query
        self.path_db = path_db if path_db else PATH_DEFAULT
        self.start, self.end = self._format_times(start, end)
        self.by = by
        self.n_results = n_results

        if not os.path.exists(self.path_db):
            raise FileNotFoundError(f"Database not found at: {self.path_db}")

        if self.start and self.end and self.start > self.end:
            raise ValueError("Start date can not be after end date!")

    def _format_times(self, start, end):

        if start is not None:
            start = parser.parse(start)
        if end is not None:
            end = parser.parse(end)
        return start, end

    def _sel_time_interval(self, df, t_start, t_end):

        if t_start:
            df = df[df.date >= t_start]
        if t_end:
            df = df[df.date <= t_end]
        return df

    @cached_property
    def df(self):

        df = pd.read_csv(self.path_db, parse_dates=["date"], infer_datetime_format=True)
        # For non-standard datetime parsing, must use pd.to_datetime after pd.read_csv
        df["date"] = pd.to_datetime(df["date"], utc=True)
        # Remove information about timezone, since we do not need
        # to know time with this level of precision
        df["date"] = df["date"].dt.tz_convert(None)
        df = self._sel_time_interval(df, self.start, self.end)

        if self.by == "best":
            df = df.reset_index(drop=True)
        elif self.by in ["newest", "oldest"]:
            df = df[df["title"].str.contains(self.query, case=False)]
            is_ascending = self.by == "oldest"
            df.sort_values(
                inplace=True, by="date", ascending=is_ascending, ignore_index=True
            )
        else:
            raise ValueError(
                'Invalid "by" argument, choose between {best, newest, oldest}'
            )
        return df

    @property
    def first_results(self):
        """Indexes of dataframe rows to be displayed as search results"""

        if self.by == "best":
            # Get the "term frequency–inverse document frequency" statistics
            # i.e weights the word counts by how many titles contain that word
            vectorizer = TfidfVectorizer()
            X = vectorizer.fit_transform(self.df["title"])
            query_vec = vectorizer.transform([self.query])

            results = cosine_similarity(X, query_vec).reshape((-1,))
            return results.argsort()[-self.n_results :][::-1]
        else:
            n_results = min(self.n_results, len(self.df))
            return range(n_results)
