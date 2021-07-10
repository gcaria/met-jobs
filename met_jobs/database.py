"""Tools to build database for search engine."""
import ssl
from urllib.parse import urljoin

import dateutil.parser as dparser
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from requests import get

ssl._create_default_https_context = ssl._create_unverified_context
requests.packages.urllib3.disable_warnings()

URL_ROOT = "https://www.lists.rdg.ac.uk/archives/met-jobs/"

soup = bs(get(URL_ROOT, verify=False).text, "lxml")


class Database:
    def __init__(self, n_lines_max=None, verbose=False):

        self.titles = []
        self.dates = []
        self.urls = []
        self.n_lines_max = n_lines_max
        self.verbose = verbose
        self._loop()

    def _loop(self):

        for month_link in soup.findAll("a"):
            month_href = month_link.get("href")

            if month_href and "date" in month_href:

                month_url = urljoin(URL_ROOT, month_href)
                month_soup = bs(get(month_url, verify=False).text, "lxml")

                # Loop on all the links in a month page
                for ad_link in month_soup.findAll("a"):

                    title, date, ad_url = extract_ad(ad_link, month_url)
                    if title:
                        self._append(title, date, ad_url)

                    if self._is_max_len:
                        break
                if self._is_max_len:
                    break

    @property
    def _is_max_len(self):
        return self.n_lines_max and len(self.titles) == self.n_lines_max

    def _append(self, title, date, url):
        """Append found ad information to output lists that will build
        dataframe.
        """

        self.titles.append(title)
        self.dates.append(date)
        self.urls.append(url)
        if self.verbose:
            print(f"{len(self.titles)} -- {title} -- {date} -- {url}")

    @property
    def df(self):
        return pd.DataFrame(
            list(zip(self.titles, self.dates, self.urls)),
            columns=["title", "date", "url"],
        )

    def to_csv(self, path):
        self.df.to_csv(path)


def extract_ad(ad_link, month_url):
    """Get job ad information from job ad link."""

    title, date, ad_url = None, None, None

    ad_href = ad_link.get("href")

    if ad_href and "msg" in ad_href:

        ad_url = month_url.replace("date.html", ad_href)

        ad_soup = bs(get(ad_url, verify=False).text, "lxml")

        title = ad_soup.find("h1").get_text()

        split_str = "[Met-jobs] "
        if split_str in title:
            title = title.split(split_str)[1]

        dates = [
            a.get_text()
            for a in ad_soup.select("tr td")
            if a.get_text().count(":") == 2
        ]

        if dates:
            date = dparser.parse(dates[0])

    return title, date, ad_url
