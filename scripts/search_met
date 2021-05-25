import argparse
import sys
from datetime import datetime, timezone

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from style import printc

parser = argparse.ArgumentParser(description='Search in the met-jobs ads.')
parser.add_argument('query', metavar='QUERY', type=str,
                    help='String for search query')
parser.add_argument('-d', '--database', default='data/database.csv', type=str,
                    help='Path of database used for search query')
parser.add_argument('-n', '--n_results', default=10, type=int,
                    help='Number of results displayed')
parser.add_argument('-s', '--start', type=str,
                    help='Start date for search (format : DD-MM-YYYY)')
parser.add_argument('-e', '--end', type=str,
                    help='End date for search (format : DD-MM-YYYY)')
parser.add_argument('--by', type=str, default='best',
                    choices=['best', 'newest', 'oldest'],
                    help='Criterium for order of results')
args = parser.parse_args()


def format_times(args):

    start, end = None, None
    if args.start:
        start = datetime.strptime(
            args.start, '%d-%m-%Y').replace(tzinfo=timezone.utc)
    if args.end:
        end = datetime.strptime(
            args.end, '%d-%m-%Y').replace(tzinfo=timezone.utc)
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
    sys.exit('Start date can not be after end date!')

df = sel_time(df, start, end)

if args.by == 'best':
    df.reset_index(inplace=True, drop=True)
    # Get the "term frequency–inverse document frequency" statistics
    # i.e weights the word counts by how many titles contain that word
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df['title'])
    query_vec = vectorizer.transform([args.query])

    results = cosine_similarity(X, query_vec).reshape((-1,))
    first_results = results.argsort()[-args.n_results:][::-1]

elif args.by in ['newest', 'oldest']:
    df = df[df['title'].str.contains(args.query, case=False)]
    is_ascending = bool(args.by == 'oldest')
    df.sort_values(by='date', inplace=True,
                   ascending=is_ascending, ignore_index=True)
    n_results = min(args.n_results, len(df))
    first_results = range(n_results)

for i_count, i_df in enumerate(first_results):

    print('-'*70)
    i_title = df.loc[i_df, 'title']
    i_date = df.loc[i_df, 'date'].strftime('%d-%m-%Y')
    i_url = df.loc[i_df, 'url']
    printc(f'{i_count+1}) {i_title} - {i_date}', 'blue')
    print(f'{i_url}')
