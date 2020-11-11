import argparse
import sys
from datetime import datetime

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from style import printc

parser = argparse.ArgumentParser(description='Search in the met-jobs ads.')
parser.add_argument('query', metavar='QUERY', type=str,
                    help='String for search query')
parser.add_argument('-d', '--database', default='data/database.csv', type=str,
                    help='Database for search query')
parser.add_argument('-n', '--n_results', default=10, type=int,
                    help='Number of results displayed')
parser.add_argument('-s', '--start', type=str,
                    help='Start date for search (format : DD-MM-YYYY)')
parser.add_argument('-e', '--end', type=str,
                    help='End date for search (format : DD-MM-YYYY)')
args = parser.parse_args()


def format_times(args):

    start, end = None, None
    if args.start:
        start = datetime.strptime(args.start, '%d-%m-%Y')
    if args.end:
        end = datetime.strptime(args.end, '%d-%m-%Y')
    return start, end


def sel_time(df, t_start, t_end):

    if t_start:
        df = df[df.date >= t_start]
    if t_end:
        df = df[df.date <= t_end]
    return df


df = pd.read_csv(args.database, parse_dates=['date'])

start, end = format_times(args)

if start and end and start > end:
    sys.exit('Start date can not be after end date !')

df = sel_time(df, start, end)

df.reset_index(inplace=True, drop=True)
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['title'])
query_vec = vectorizer.transform([args.query])
results = cosine_similarity(X, query_vec).reshape((-1,))
last_results = results.argsort()[-args.n_results:][::-1]

for i_count, i_df in enumerate(last_results):

    print('-'*70)
    i_title = df.loc[i_df, 'title']
    i_date = df.loc[i_df, 'date'].strftime('%d %m %Y')
    i_url = df.loc[i_df, 'url']
    printc(f'{i_count+1}) {i_title} - {i_date}', 'blue')
    print(f'{i_url}')
