# -*- coding: utf-8 -*-
"""
Install the following libraries
# !pip install sematch
# !pip install nltk
!pip install numpy
!pip install scipy
!pip install spacy
!python -m spacy download en_core_web_lg
"""
# import nltk
import json
import spacy
# nltk.download('wordnet')
# nltk.download('wordnet_ic')
# from sematch import semantic
# from sematch.semantic.similarity import WordNetSimilarity

nlp = spacy.load("en_core_web_lg")

PATH = "../data/"
ARTICLES = PATH + "articlesWithKeywords.json"
DATABASE = PATH + "predefinedCategories.json"
OUTPUT = PATH + "articlesWithPredefined.json"

# wns = WordNetSimilarity()

with open(DATABASE) as f:
    predefinedCategories = json.load(f)

with open(ARTICLES) as f:
    articles = json.load(f)


def similarityScoreSpacy(a, b):
    return nlp(a).similarity(nlp(b)) * 100


# def similarityScoreWN(a, b):
#     return wns.word_similarity(a, b, 'wpath')


# function calculates the similarity score between two strings
def similarityScore(a, b):
    return similarityScoreSpacy(a, b)


# function calculates the similarity score between two arrays
def similarityScoreBetweenArrays(x, y):
    sim = 0
    for a in x:
        for b in y:
            sim += similarityScore(a, b)
    return sim / (len(x) * len(y))


def model1_match_keywords():
    for article in articles:
        score = [
            similarityScoreBetweenArrays(article['keywords'],
                                         x['featureWords'])
            for x in predefinedCategories
        ]
        article['predefinedCategory'] = predefinedCategories[score.index(
            max(score))]
    with open(OUTPUT, "w") as file:
        file.write(articles)


if __name__ == "__main__":
    model1_match_keywords()
