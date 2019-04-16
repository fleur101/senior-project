# Requirements
# pip install numpy
# pip install scipy
# pip install spacy
# python -m spacy download en_core_web_lg

import nltk
import json
import spacy
import joblib
from scipy import spatial 
import numpy as np
nlp = spacy.load("en_core_web_lg")

import tensorflow as tf
import tensorflow_hub as hub
module_url = "https://tfhub.dev/google/universal-sentence-encoder/2"
embed = hub.Module(module_url)
def getFeatures(arrayOfTexts):
  with tf.Session() as session:
    session.run([tf.global_variables_initializer(), tf.tables_initializer()])
    features = session.run(embed(arrayOfTexts))
  return features


# The path to the folder with data
PATH = "../data/"

# file named USER_INPUT_FN contains a JSON array of strings
# format: [string]
USER_INPUT_FN = PATH + "userCategories.json"

# file named PREDEFINED_CATEGORIES_FN contains JSON array of categories.
# format: [{ id: string, featureWords: [string] }]
PREDEFINED_CATEGORIES_FN = PATH + "predefinedCategories.json"

# file named ARTICLES_FN contains a JSON array of all articles.
# format: [{ title: string, text: string, url: string, source_url: string, predefinedCategory: string }]
ARTICLES_FN = PATH + "articlesWithWikipediaPredefined.json"

# file named CLUSTERING_MODEL_FN contains a joblib model of clustering algorithm.
MODEL_FN = PATH + "model_clustering.joblib"

# file named OUTPUT_FN will be created, containing an array of article group
# format: [{ title: string, url: string, source_url: string, predefinedCategory: string, category: string }]
OUTPUT_FN = PATH + "categorizedArticles.json"


# This model makes a
def model2_match_user_input(userInputFilename, articlesFilename,
                            predefinedCategoriesFilename, outputFilename, modelFilename):
    # Open files
    with open(userInputFilename) as f:
        userCats = json.load(f)
    with open(articlesFilename) as f:
        artilces = json.load(f)
    with open(predefinedCategoriesFilename) as f:
        definedCats = json.load(f)
    with open(modelFilename) as f:
        model = joblib.load(f)

    # map user input to clusters
    userVecs = [getFeatures(x) for x in userCats]
    userToPredefined = [model.predict(x) for x in userVecs]
    
    for article in articles:
        # compute distance to each user
        distances = [spatial.distance.cosine(model.cluster_centers_[article['predefinedCategory']], model.cluster_centers_[x]) for x in userToPredefined]
        distances = sorted(enumerate(distances), lambda x: x[1])
        article['category'] = userCats[distances[0][0]]
        article['distances'] = distances 

    with open(PATH + OUTPUT_FN, 'w') as file:
        file.write(json.dumps(result))


if __name__ == "__main__":
    model2_match_user_input(USER_INPUT_FN, ARTICLES_FN,
                            PREDEFINED_CATEGORIES_FN, OUTPUT_FN, MODEL_FN)
