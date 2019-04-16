# -*- coding: utf-8 -*-
"""
python 3
## Newspaper3k newspaper articles extraction

### Steps to reproduce:
- Install Anaconda Navigator 1.8.7  
- Create an environment called 'newspaper3k'  
- Install nb_conda for Jupyter notebook  
- Install newspaper3k with `pip install newspaper3k` 
- Download necessary corpora for NLP by running this script https://raw.githubusercontent.com/codelucas/newspaper/master/download_corpora.py
- Run this document
"""
import re
import newspaper
import time
import json
import copy

PATH = "../data/"
DUMPFILE = PATH + "articles.json"
LOGFILE = PATH + "logs/articleExtractor" + time.time() + ".log"
# Default number of articles to extract from each paper
NUM_OF_ARTICLES = 20
# Newspapers for extraction
newspaperURLs = [
    "http://www.nydailynews.com/",
    #     "https://www.huffingtonpost.com/", multilingual
    #     "https://www.voanews.com/",
    "http://www.latimes.com/",
    "https://nypost.com/",
    #     "http://www.dailymail.co.uk", bad formatting
    #     "https://www.thetimes.co.uk/", paid
    "http://www.chicagotribune.com/",
    "https://timesofindia.indiatimes.com/",
    "http://www.chinadaily.com.cn/",
    "https://cnn.com/",
    "https://www.nytimes.com/",
    "https://www.wsj.com/",
    "https://www.nbcnews.com/",
    "https://www.foxnews.com/",
    "https://www.washingtonpost.com/",
    "https://www.theguardian.com/",
    "https://www.bbc.com/",
    "https://www.usatoday.com/",
    "https://abcnews.go.com/"
]
LOG = ""


def logprint(text):
    print(text)
    global LOG
    LOG += text + "\n"


def build(newspaperURL):
    logprint(
        "Fetching articles from {} ...\nThis might take some time...".format(
            newspaperURL))
    start = time.time()
    config = newspaper.Config()
    config.MIN_WORD_COUNT = 700
    config.MIN_SENT_COUNT = 40
    paper = newspaper.build(
        url=newspaperURL,
        config=config,
        memoize_articles=False,
        fetch_images=False,
    )
    end = time.time()
    logprint("Done. Fethching took {} seconds.".format(end - start))
    return paper


def extractArticles(paper, number):
    logprint("Starting article extraction...")
    start = time.time()
    i = 0
    extractedArticles = []
    for article in paper.articles:

        try:
            article.download()
            article.parse()
            l = len(article.text.split(' '))
            if l < 300:
                print("{}".format(l), end=" "),
                raise Exception
            article.nlp()
            extractedArticles.append(article)
            if i == number:
                i -= 1
                break
            i += 1
            logprint("Extracting article #{} from {}...".format(
                i + 1, paper.brand))
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            pass
            #logprint("Error occured while extracting article #{}".format(i+1))

    end = time.time()
    logprint(
        "Finished article extraction! Extracted {} articles".format(i + 1))
    logprint("Time took: {} seconds".format(end - start))

    return extractedArticles


def dumpArticles(articles, filename):
    _id = 0
    for i in range(len(articles)):
        articles[i] = {
            "id": _id,
            "text": articles[i].text,
            "title": articles[i].title,
            "source_url": articles[i].source_url,
            "url": articles[i].url,
            "keywords": articles[i].keywords,
            "meta_keywords": articles[i].meta_keywords,
            "authors": articles[i].authors,
        }
        _id += 1
    r = json.dumps(articles)
    with open(filename, "w") as file:
        file.write(r)


def loadArticles(filename):
    with open(filename, "r") as file:
        articles = json.load(file)
    return articles


def getArticles():
    start = time.time()
    articles = []
    for newspaperURL in newspaperURLs:
        paper = build(newspaperURL)
        logprint("Number of articles: {}".format(len(paper.articles)))
        articles += extractArticles(paper, NUM_OF_ARTICLES)
    end = time.time()
    logprint("DONE. Total time: {} seconds".format(end - start))
    return articles


def save(articles):
    dumpArticles(articles, DUMPFILE)
    logprint("Results are dumped to {}".format(DUMPFILE))
    with open(LOGFILE, "w") as f:
        f.write(LOG)
    print("Logs are saved in artcleExtractorLogs.txt")


# config
# extractor
# source_url
# url
# title
# top_img
# top_image
# meta_img
# imgs
# images
# movies
# text
# keywords
# meta_keywords
# tags
# authors
# publish_date
# summary
# html
# article_html
# is_parsed
# download_state
# download_exception_msg
# meta_description
# meta_lang
# meta_favicon
# meta_data
# canonical_link
# top_node
# clean_top_node
# doc
# clean_doc
# additional_data
# link_hash
