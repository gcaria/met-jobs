import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-q', '--query', required=True)
args = parser.parse_args()

df = pd.read_csv('database.csv')
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['title'])
query_vec = vectorizer.transform([args.query])
results = cosine_similarity(X,query_vec).reshape((-1,))


for i_count, i_df in enumerate(results.argsort()[-10:][::-1]):
    print(i_count+1, df.loc[i_df,'title'])
    print(df.loc[i_df,'url'])
