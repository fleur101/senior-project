# Requirements
# pip install numpy
# pip install scipy
# pip install tensorflow

# import nltk
import json
# import spacy
import joblib
from scipy import spatial 
import numpy as np
from operator import itemgetter
import sklearn
# nlp = spacy.load("en_core_web_lg")

import time
totalS = time.time()

start = time.time()
print("Embed load")
import tensorflow as tf
import tensorflow_hub as hub
module_url = "https://tfhub.dev/google/universal-sentence-encoder/2"
embed = hub.Module(module_url)
def getFeatures(arrayOfTexts):
  with tf.Session() as session:
    session.run([tf.global_variables_initializer(), tf.tables_initializer()])
    features = session.run(embed(arrayOfTexts))
  return features
end = time.time()
print(f"Time: {end - start}")

# The path to the folder with data
PATH = "../data2.0/"

# file named USER_INPUT_FN contains a JSON array of strings
# format: [string]
USER_INPUT_FN = PATH + "userCategories.json"

# file named PREDEFINED_CATEGORIES_FN contains JSON array of categories.
# format: [{ id: string, featureWords: [string] }]
# UPDATE!!! Since we use clustering now, it will be just range(0, N)
# PREDEFINED_CATEGORIES_FN = PATH + "predefinedCategories.json"

# file named ARTICLES_FN contains a JSON array of all articles.
# format: [{ title: string, text: string, url: string, source_url: string, predefinedCategory: string }]
ARTICLES_FN = PATH + "articlesWithWikipediaPredefined.json"
# ARTICLES_FN = PATH + "mock_data.json"

# file named CLUSTERING_MODEL_FN contains a joblib model of clustering algorithm.
MODEL_FN = PATH + "model_clustering.joblib"

# file named OUTPUT_FN will be created, containing an array of article group
# format: 
# [
    # [{ 
        # selectedCategory: string,
        # percentageScores: string,
        # title: string,
        # url?: string,
        # source_url?: string,
    # }]
# ]
OUTPUT_FN = PATH + "categorizedArticles.json"

def escape(s):
    return s.translate(str.maketrans({"'":  r"\'", '"': r'\"'}))

# This model makes a
def model2_match_user_input(userInputFilename, articlesFilename,
                         outputFilename, modelFilename):
                         
    start = time.time()
    print("Read files")
    # Open files
    with open(userInputFilename) as f:
        userCats = json.load(f)
    with open(articlesFilename) as f:
        articles = json.load(f)
    # with open(predefinedCategoriesFilename) as f:
    #     definedCats = json.load(f)
    model = joblib.load(modelFilename)
    end = time.time()
    print(f"Time: {end - start}")


    
    start = time.time()
    print("Features generation")
    # map user input to clusters
    userVecs = getFeatures(userCats)
    end = time.time()
    print(f"Time: {end - start}")
    start = time.time()
    print("Features prediction")
    userToPredefined = model.predict(userVecs)
    end = time.time()
    print(f"Time: {end - start}")
    
    start = time.time()
    print("distance calculation")
    result = [[] for _ in range(len(userCats))]
    for article in articles:
        # compute distance to each user
        distances = [np.int(100*(1-spatial.distance.cosine(model.cluster_centers_[article['predefinedCategory']], x))) for x in userVecs]
        selectedCategory = np.argmax(distances)
        article['selectedCategory'] = np.int(selectedCategory)
        article['percentageScores'] = distances
        if 'title' not in article:
            article['title'] = article['text'][:100]+"..."
        del article['text']
        del article['keywords']
        del article['meta_keywords']
        del article['authors']
        for i in article:
            if type(article[i]) == str:
                article[i] = escape(article[i])
        result[selectedCategory].append(article)

    with open(PATH + OUTPUT_FN, 'w') as file:
        file.write(json.dumps(result))
    # hit = 0
    # miss = 0
    # for ind, x in enumerate(result):
    #     for y in x:
    #         if userCats.index(y['original_category']) == ind:
    #             hit += 1
    #         else:
    #             miss +=1
    end = time.time()
    print(f"Time: {end - start}")
    print("result: ")
    # print(f"hits: {hit}")
    # print(f"miss: {miss}")
    # print(f"score: {hit/(hit+miss)}")


if __name__ == "__main__":
    print("Started matching")
    model2_match_user_input(USER_INPUT_FN, ARTICLES_FN,
                            OUTPUT_FN, MODEL_FN)

totalF = time.time()
print(f"Total time: {totalF-totalS}")