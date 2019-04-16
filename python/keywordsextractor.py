# -*- coding: utf-8 -*-
"""
python 2

Install the following libraries
pip install summa
pip install rake-nltk
pip install pandas
"""
from summa import keywords
from rake_nltk import Rake
import json
import pandas as pd
import time

PATH = "../data/"
INPUT = PATH + "articles.json"
OUTPUT = PATH + "articlesWithKeywords.json"
r = Rake()


def extractKeywordsSumma(text):
    keywords.keywords(text).split()


def extractKeywordsRake(text):
    r.extract_keywords_from_text(text)
    return r.get_ranked_phrases()


def extractKeywordsFrom(text):
    return extractKeywordsSumma(text)


def loadArticles(input_filename):
    with open(input_filename, "r") as file:
        articles = json.load(file)
    return articles


def extractKeywords(articles, output_filename):
    i = 0
    avg_keywords = 0
    for article in articles:
        text = article['text']
        text = text.encode('ascii', 'ignore').decode('ascii')
        words = extractKeywordsFrom(article)
        avg_keywords += len(words)
        article['keywords'] = words
        i += 1
    with open(output_filename, "w") as file:
        file.write(articles)

    print('Extracted keywords from {} articles'.format(i))
    avg_keywords /= i
    print('Average number of keywords: {}'.format(avg_keywords))


if __name__ == "__main__":
    start = time.time()
    articles = loadArticles(INPUT)
    extractKeywords(articles, OUTPUT)
    end = time.time()
    print('It took {} seconds'.format(end - start))
