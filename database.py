"""Tools to build database for search engine."""
import sys
from urllib.parse import urljoin
from requests import get
import requests
from bs4 import BeautifulSoup as bs
import ssl
import csv

ssl._create_default_https_context = ssl._create_unverified_context
requests.packages.urllib3.disable_warnings()

URL_ROOT = 'https://www.lists.rdg.ac.uk/archives/met-jobs/'

soup = bs(get(URL_ROOT, verify=False).text, "lxml")


class Database:
    def __init__(self, years, months, path_csv, n_lines_max=int(1E6)):

        self.years = years
        self.months = months
        self.path_csv = path_csv
        self.n_lines_max = n_lines_max
        self._init_csv()
        self._loop()

    def _init_csv(self):

        with open(self.path_csv, "w") as f:
            pass

    def _loop(self):

        for month_link in soup.findAll('a'):
            month_href = month_link.get('href')

            if month_href and 'date' in month_href:

                month_url = urljoin(URL_ROOT, month_href)
                monthSoup = bs(get(month_url, verify=False).text,
                               "lxml")

                # for each link in a month page
                for ad_link in monthSoup.findAll('a'):

                    ad_href = ad_link.get('href')

                    if ad_href and 'msg' in ad_href:

                        ad_url = month_url.replace('date.html', ad_href)

                        ad_soup = bs(get(
                            ad_url, verify=False).text, "lxml")

                        title = ad_soup.find('h1').get_text()

                        date = [a.get_text() for a in ad_soup.select(
                            'tr td') if a.get_text().count(':') == 2][0]

                        print(title, date, ad_url)
                        with open(self.path_csv, 'a') as newFile:
                            new = csv.writer(newFile)
                            new.writerow([title, date, ad_url])

                        with open(self.path_csv) as f:
                            n_lines = sum(1 for line in f)
                            if n_lines == self.n_lines_max:
                                sys.exit()
