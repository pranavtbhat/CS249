import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

data = pd.read_csv('vertex_data.tsv', delimiter="\t")
data = data.where((pd.notnull(data)), "")

vect = TfidfVectorizer(min_df=1)
tfidf = vect.fit_transform(data.job_title)

pairwise_similarity = (tfidf * tfidf.T).A
