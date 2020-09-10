#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
import re
import sys
import requests
from bs4 import BeautifulSoup as bs
import urllib
import argparse
import ssl
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


ssl._create_default_https_context = ssl._create_unverified_context
requests.packages.urllib3.disable_warnings()

parser = argparse.ArgumentParser()
parser.add_argument('-w', '--word')
parser.add_argument('-m', '--maxFound', type=int, default=100)
args = parser.parse_args()

URL_ROOT = 'https://www.lists.rdg.ac.uk/archives/met-jobs/'

soup = bs(requests.get(URL_ROOT, verify=False).text, "lxml")

wordsRange = 50

# for each month page of ads


class Search:
    def __init__(self, args):
        self.countFound = 0
        self.countAds = 0
        self.listMonthsOcc = []
        self.args = args
        self._loop()

    def _loop(self):
        for monthLink in soup.findAll('a'):

            monthHref = monthLink.get('href')

            if monthHref and 'date' in monthHref:

                monthUrl = URL_ROOT + monthHref
                print(monthUrl)
                year, month = [int(a)
                               for a in monthUrl.split('/')[-2].split('-')]
                print(year, month)
                sys.exit()
                monthSoup = bs(requests.get(
                    monthUrl, verify=False).text, "lxml")

                # for each link in a month page
                for adLink in monthSoup.findAll('a'):

                    adHref = adLink.get('href')

                    if adHref and 'msg' in adHref:

                        self.countAds += 1
                        if not args.word:
                            self.listMonthsOcc.append(yearMonth)
                            if self.countAds > self.args.maxFound:
                                return
                            else:
                                continue
                        adUrl = monthUrl.replace('date.html', adHref)

                        try:
                            data = urllib.request.urlopen(
                                adUrl).read().decode('utf-8')
                        except urllib.error.HTTPError:
                            print('HTTP error when reading. Continue')
                            continue

                        if args.word:
                            match = re.search(
                                self.args.word, data, re.IGNORECASE)

                            if match:
                                # get sentence around self.args.word
                                word = match.group(0)
                                index = data.index(word)
                                sentence = data[index -
                                                wordsRange: index+wordsRange]

                                # make sure it's not title of next or previous ad
                                if '[Met-jobs]' not in sentence:
                                    print(adUrl)
                                    print(sentence + '\n')
                                    print(data)
                                    self.countFound += 1
                                    self.listMonthsOcc.append(yearMonth)

                                if self.countAds % 50 == 0:
                                    print(self.countAds)
                                if self.countFound > self.args.maxFound:
                                    print(self.countFound/self.countAds)
                                    return


s = Search(args)
dd = Counter(s.listMonthsOcc)

years_fmt = mdates.DateFormatter('%Y-%m')
years = mdates.YearLocator()
fig, ax = plt.subplots()


xLabels = []
for k in dd.keys():
    year, month = [int(a) for a in k.split('-')]
    xLabels.append(datetime(year, month, 1))

ax.scatter(xLabels, dd.values())  # , width=5)
#  print(xLabels)
#  ax.set_xticklabels(xLabels)
ax.xaxis.set_major_locator(years)
ax.xaxis.set_major_formatter(years_fmt)
ax.grid()

plt.savefig('histOut.pdf')
plt.show()
