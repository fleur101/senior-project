# Requirements
# pip install numpy
# pip install scipy
# pip install spacy
# python -m spacy download en_core_web_lg

import nltk
import json
import spacy
nlp = spacy.load("en_core_web_lg")

# The path to the folder with data
PATH = "../data/"

# file named USER_INPUT_FN contains a JSON array of strings
# format: [string]
USER_INPUT_FN = "userCategories.json"

# file named PREDEFINED_CATEGORIES_FN contains JSON array of categories.
# format: [{ id: string, featureWords: [string] }]
PREDEFINED_CATEGORIES_FN = "predefinedCategories.json"

# file named ARTICLES_FN contains a JSON array of all articles.
# format: [{ title: string, text: string, url: string, source_url: string, predefinedCategory: string }]
ARTICLES_FN = "articlesWithCnnPredefined.json"

# file named OUTPUT_FN will be created, containing an array of article group
# format: [{ title: string, url: string, source_url: string, predefinedCategory: string, category: string }]
OUTPUT_FN = "categorizedArticles.json"


# function calculates the similarity score between two strings
def similarityScore(a, b):
    return nlp(a).similarity(nlp(b)) * 100


# function calculates the similarity score between two arrays
def similarityScoreBetweenArrays(x, y):
    sim = 0
    for a in x:
        for b in y:
            sim += similarityScore(a, b)
    return sim / (len(x) * len(y))


# function returns feature words for user definded categories
def featureWords(category):
    return [category]


# This model makes a
def model2_match_user_input(userInputFilename, articlesFilename,
                            predefinedCategoriesFilename, outputFilename):
    # Open files
    with open(PATH + userInputFilename) as f:
        userCats = json.load(f)
    with open(PATH + articlesFilename) as f:
        artilces = json.load(f)
    with open(PATH + predefinedCategoriesFilename) as f:
        definedCats = json.load(f)
    # Assign each article
    mapDefinedToUser = {}
    for definedCat in definedCats:
        simScores = []
        # calculate similarity with each predefined category
        for userCat in userCats:
            simScores.append(
                similarityScoreBetweenArrays(
                    featureWords(userCat), definedCat['featureWords']))
        # score = max(simScores)
        # userCatIndex = simScores.index(score)
        # userCat = userCats[userCatIndex]
        # mapDefinedToUser[definedCat["id"]] = {
        #     "category": userCat,
        #     "score": score
        # }
        sortedScores = sorted(simScores, reverse=True)
        mapDefinedToUser[definedCat["id"]] = []
        for i in range(3):
            score = sortedScores[i]
            userCatIndex = simScores.index(score)
            userCat = userCats[userCatIndex]
            mapDefinedToUser[definedCat["id"]].append({
                "category": userCat,
                "score": score
            })
    result = [[] for i in range(len(userCats) + 1)]
    for article in artilces:
        del article['text']
        if article['definedCategory'] in mapDefinedToUser:
            article['category'] = mapDefinedToUser[article['definedCategory']][
                0]['category']
            article['top3'] = mapDefinedToUser[article['definedCategory']]
            result[userCats.index(article['category'])].append(article)
        else:
            article['category'] = None
            result[len(userCats)].append(article)

    with open(PATH + OUTPUT_FN, 'w') as file:
        file.write(json.dumps(result))


if __name__ == "__main__":
    model2_match_user_input(USER_INPUT_FN, ARTICLES_FN,
                            PREDEFINED_CATEGORIES_FN, OUTPUT_FN)
