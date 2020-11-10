import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import argparse
from style import printc

parser = argparse.ArgumentParser(description='Search in the met-jobs ads.')
parser.add_argument('query', metavar='QUERY', type=str,
                    help='String for search query')
parser.add_argument('-d', '--database', default='data/database.csv',
                    help='Database for search query')
parser.add_argument('-n', '--n_results', default=10, type=int,
                    help='Number of results displayed')
args = parser.parse_args()

df = pd.read_csv(args.database)

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['title'])
query_vec = vectorizer.transform([args.query])
results = cosine_similarity(X, query_vec).reshape((-1,))

for i_count, i_df in enumerate(results.argsort()[-args.n_results:][::-1]):

    print('-'*70)
    i_title = df.loc[i_df, 'title']
    i_date = df.loc[i_df, 'date']
    i_url = df.loc[i_df, 'url']
    printc(f'{i_count+1}) {i_title} - {i_date}', 'blue')
    print(f'{i_url}')
