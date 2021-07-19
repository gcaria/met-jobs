"""Tools to query database."""
import os
from datetime import datetime, timezone
from functools import cached_property

import pandas as pd
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
        self.df = None

        if self.start and self.end and self.start > self.end:
            raise ValueError("Start date can not be after end date!")

    def _format_times(self, start, end):

        if start is not None:
            start = datetime.strptime(start, "%d-%m-%Y").replace(tzinfo=timezone.utc)
        if end is not None:
            end = datetime.strptime(end, "%d-%m-%Y").replace(tzinfo=timezone.utc)
        return start, end

    def _sel_time_interval(self, df, t_start, t_end):

        if t_start:
            df = df[df.date >= t_start]
        if t_end:
            df = df[df.date <= t_end]
        return df

    @cached_property
    def _df(self):
        df = pd.read_csv(self.path_db, parse_dates=["date"])
        return self._sel_time_interval(df, self.start, self.end)

    @property
    def first_results(self):
        """Indexes of dataframe rows to be displayed as search results"""

        if self.by == "best":
            self.df = self._df.reset_index(drop=True)
            # Get the "term frequency–inverse document frequency" statistics
            # i.e weights the word counts by how many titles contain that word
            vectorizer = TfidfVectorizer()
            X = vectorizer.fit_transform(self.df["title"])
            query_vec = vectorizer.transform([self.query])

            results = cosine_similarity(X, query_vec).reshape((-1,))
            return results.argsort()[-self.n_results :][::-1]

        elif self.by in ["newest", "oldest"]:
            self.df = self._df[self._df["title"].str.contains(self.query, case=False)]
            is_ascending = self.by == "oldest"
            self.df = self.df.sort_values(
                by="date", ascending=is_ascending, ignore_index=True
            )
            n_results = min(self.n_results, len(self.df))
            return range(n_results)
        else:
            raise ValueError(
                'Invalid "by" argument, choose between {best, newest, oldest}'
            )
