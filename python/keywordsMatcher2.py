import pandas as pd
import json
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import cross_val_score
from StringIO import StringIO

PATH = "../data/"
DATASET = "datasets/bbc.csv"
INPUT = "articles.json"
OUTPUT = "articlesWithPredefined.json"

with open(DATASET, "r") as file:
    df = pd.read_csv(StringIO(file))
df['category_id'] = df['category'].factorize()[0]
category_id_df = df[['category', 'category_id'
                     ]].drop_duplicates().sort_values('category_id')
category_to_id = dict(category_id_df.values)
id_to_category = dict(category_id_df[['category_id', 'category']].values)

with open(INPUT, "r") as file:
    articles = json.load(file)

tfidf = TfidfVectorizer(
    sublinear_tf=True,
    min_df=5,
    norm='l2',
    encoding='latin-1',
    ngram_range=(1, 2),
    stop_words='english')

features = tfidf.fit_transform(df.text).toarray()
labels = df.category_id

model = LogisticRegression(random_state=0)

model.fit(features, labels)

text_features = tfidf.transform([x['text'] for x in articles])
predictions = model.predict(text_features)

for article, prediction in zip(articles, predictions):
    article['category'] = id_to_category[prediction]

with open(OUTPUT, "w") as file:
    json.dump(articles, file)
