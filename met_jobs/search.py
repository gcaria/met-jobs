"""Tools to query database."""
from datetime import datetime, timezone

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from functools import cached_property


class Search:
    def __init__(
        self, query, path_db=None, start=None, end=None, by="best", n_results=10
    ):
        self.query = query
        self.path_db = path_db
        self.start, self.end = self._format_times(start, end)
        self.by = by
        self.n_results = n_results

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
    def df(self):
        df = pd.read_csv(self.path_db, parse_dates=["date"])
        return self._sel_time_interval(df, self.start, self.end)

    @property
    def first_results(self):
        if self.by == "best":
            self.df.reset_index(inplace=True, drop=True)
            # Get the "term frequency–inverse document frequency" statistics
            # i.e weights the word counts by how many titles contain that word
            vectorizer = TfidfVectorizer()
            X = vectorizer.fit_transform(self.df["title"])
            query_vec = vectorizer.transform([self.query])

            results = cosine_similarity(X, query_vec).reshape((-1,))
            return results.argsort()[-self.n_results :][::-1]

        elif self.by in ["newest", "oldest"]:
            self.df = self.df[self.df["title"].str.contains(self.query, case=False)]
            is_ascending = bool(self.by == "oldest")
            self.df.sort_values(
                by="date", inplace=True, ascending=is_ascending, ignore_index=True
            )
            n_results = min(args.n_results, len(self.df))
            return range(n_results)
        else:
            raise ValueError('Invalid "by" argument')
