"""Tools to build database for search engine."""
from urllib.parse import urljoin
from requests import get
import requests
from bs4 import BeautifulSoup as bs
import ssl
import pandas as pd

ssl._create_default_https_context = ssl._create_unverified_context
requests.packages.urllib3.disable_warnings()

URL_ROOT = 'https://www.lists.rdg.ac.uk/archives/met-jobs/'

soup = bs(get(URL_ROOT, verify=False).text, "lxml")


class Database:
    def __init__(self, n_lines_max=int(1E6)):

        self.titles = []
        self.dates = []
        self.urls = []
        self.n_lines_max = n_lines_max
        self._loop()

    def _loop(self):

        for month_link in soup.findAll('a'):
            month_href = month_link.get('href')

            if month_href and 'date' in month_href:

                month_url = urljoin(URL_ROOT, month_href)
                monthSoup = bs(get(month_url, verify=False).text,
                               "lxml")

                # for each link in a month page
                for ad_link in monthSoup.findAll('a'):

                    title, date, ad_url = extract_ad(ad_link, month_url)
                    if title:
                        self._append(title, date, ad_url)

                    if len(self.titles) == self.n_lines_max:
                        break
                if len(self.titles) == self.n_lines_max:
                    break

    def _append(self, title, date, url):
        """Append found ad information to output lists that will build
        dataframe.
        """

        print(title, date, url)
        self.titles.append(title)
        self.dates.append(date)
        self.urls.append(url)
        print(len(self.titles))

    @property
    def df(self):
        return pd.DataFrame(list(zip(self.titles, self.dates, self.urls)),
                            columns=['title', 'date', 'url'])

    def to_csv(self, path):
        self.df.to_csv(path)


def extract_ad(ad_link, month_url):
    """Get ad information from ad link."""

    title, date, ad_url = None, None, None

    ad_href = ad_link.get('href')

    if ad_href and 'msg' in ad_href:

        ad_url = month_url.replace('date.html', ad_href)

        ad_soup = bs(get(
            ad_url, verify=False).text, "lxml")

        title = ad_soup.find('h1').get_text()

        split_str = '[Met-jobs] '
        if  split_str in title:
            title = title.split(split_str)[1]

        dates = [a.get_text() for a in ad_soup.select(
            'tr td') if a.get_text().count(':') == 2]

        if dates:
            date = dates[0]

    return title, date, ad_url
