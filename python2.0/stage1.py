#pip install -q tensorflow-hub


import numpy as np
import requests
import json
import time
import collections
from sklearn.cluster import KMeans
import tensorflow as tf
import tensorflow_hub as hub
from scipy.spatial.distance import pdist , squareform
from scipy.cluster.hierarchy import fcluster , linkage , dendrogram
import joblib
import sys, os
module_url = "https://tfhub.dev/google/universal-sentence-encoder/2"
embed = hub.Module(module_url)
# Number of articles to read
N = 100000

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

PATH = "../data2.0"

wikiDatasetPath = PATH + "documents_utf8_filtered_20pageviews.csv"
CLUSTERING_MODEL = PATH + "model_clustering.joblib"
CLASSIFIER_MODEL = PATH + "model_classifier.joblib"
WIKI_CATEGORIES = PATH + "wikipedia_categories" 
# Dataset with raw categories
# workFolder = path+folder_name+"/"
# catVecsPath = workFolder + "cats_vecs.csv"

# categoryFile = path+"cleaned-dataset-5-{}.json".format(N)
# !mkdir -p '{workFolder}'


# sys.path.append(os.path.abspath('/content/drive/Team Drives/Senior Project Team Drive/All/'))


class WikipediaDatabase:
    # Template of wikipedia url which will get the category
    WIKIPEDIA_URL_TEMPLATE = "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=categories&redirects=1&pageids={0}"

    def __init__(self, N, dataset_path):
        self.N = N
        self.dataset_path = dataset_path

    # Read articles from file
    # returns vector of ids as strings
    def getIds(self):
        print("Reading ids of the articles...", sep="")
        start = time.perf_counter()
        self.ids = []
        with open(self.dataset_path, encoding="utf8") as f:
            # Only first N artilces
            for n in np.arange(self.N):
            self.ids.append(f.readline().split(',', 1)[0].split("-")[-1])
        end = time.perf_counter()
        print(f" Done. Took {end-start} seconds")

    # Extract categories from the Wikipedia
    # Returns dataset [{pid, title, categories}]
    def extractMetadata(self):
        print("Fetching categories of the articles from Wikipedia...", sep=" ")
        start = time.perf_counter()
        self.categories = []
        # self.titles = []
        self.valid_size = 0
        for pid in ids:
            # Put page id into the template
            # Fetch categories
            r = requests.get(WIKIPEDIA_URL_TEMPLATE.format(pid))
            # Get query results
            query = r.json()["query"]

            # If there where redirect, means article does not exist anymore
            if "redirects" in query:
                self.categories.append(None)
                continue

            # under pages key, I assume there is only one subkey with page id
            key, value = query["pages"].popitem()

            # if there is no categories, skip
            if "categories" not in value:
                self.categories.append(None)
                continue
            self.valid_size += 1
            self.categories.append([x["title"] for x in value["categories"]])
            # self.titles.append(value["title"])
        end = time.perf_counter()
        print(f"Done. Valid articles count: {self.valid_size}; Time took {end-start} seconds")

    def loadCategories(self, outputFilename):
        self.categories = np.loadtxt(outputFilename)
        
    def saveCategories(self, outputFilename):
        np.savetxt(outputFilename, self.categories)

    def cleanCategories():
        wikiPrefixes = ("All Wikipedia articles",\
                        "All articles",\
                        "Articles",\
                        "BLP articles",\
                        "CS1 ",\
                        "Cleanup tagged",\
                        "Commons category",\
                        "EngvarB",\
                        "Pages",\
                        "Use ",\
                        "Wikipedia",
                        "Coordinates on Wikidata")
        for i in range(N):
            if self.categories[i]!=None:
                self.categories[i] = [x[9:] for x in self.categories[i] if not x[9:].startswith(wikiPrefixes)]
                self.categories[i] = [x for x in self.categories[i] if re.search(r"articles|\d\d\d\d|[Ww]iki|Century", x) == None]

    def generateDataset(self):
        self.getIds()
        self.extractMetadata()
        self.cleanCategories()

    def assignClusters(self, model, words):
        self.singleCluster = []
        self.multiCluster = []
        for cats in self.categories:
            if cats == None:
                clusters.append(None)
                continue
            freqs = collections.Counter([model.labels_[words.index(j)] for j in cats]).most_common()
            self.singleCluster.append(freqs[0][0].item())
            self.multiCluster.append([x[0].item() for x in freqs if x[1] == freqs[0][1]])
    
    def extractTexts(self):
        self.texts = []
        self.labels = []
        with open(self.dataset_path, encoding="utf8") as f: 
            # Only first N articles
            for n in np.arange(N):
                # read only first 5000 characters
                text = f.readline().split(',',1)[1][:5000])
                if self.singleCluster[n] == '':
                    continue
                self.texts.append(text)
                self.labels.append(int(self.singleCluster[n]))


    def getDataframeForClassifier(self):
        self.extractTexts()
        return pd.DataFrame(list(zip(self.texts, self.labels)), columns=['text', 'category'])

class ClusteringProcessor:
    def getFeatures(arrayOfTexts):
        with tf.Session() as session:
            session.run([tf.global_variables_initializer(), tf.tables_initializer()])
            features = session.run(embed(arrayOfTexts))
        return features


    def setClusterSize(self, N):
        self.N = N
    def setData(self, WikiData):
        self.WikiData = WikiData
        print(f"[Clustering] Converting words to vectors")
        self.words = np.unique([y for x in self.WikiData.categories if x != None for y in x]).tolist()
        self.vecs = self.getFeatures(words)

    def train(self):
        print(f"[Clustering] Training model with {self.N} clusters")
        self.model = KMeans(self.N, n_jobs = 4)
        self.model.fit(self.vecs)

    def loadModel(self, filename):
        self.model = joblib.load(filename)
        print(f"[Clustering] Model loaded from {filename}")

    def saveModel(self, filename):
        joblib.dump(self.model, filename)
        print(f"[Clustering] Model saved to {filename}")


class ClassifierProcessor:
    def __init__(self, WikiData):
        self.WikiData = WikiData

    def preprocessData():
        wiki_df = self.WikiData.getDataframeForClassifier()
        r = wiki_df.groupby('category').category.count()
        r.sort_values(ascending=False)
        freqs = collections.Counter(labels).most_common()
        minA = 50
        maxA = 200
        #Choose articles that have categories that appear not less than 20 times in total
        lnorm_cat_freqs = [x for x in freqs if x[1]>=minA]
        lnorm_cats = [x[0] for x in lnorm_cat_freqs]
        lnorm_wiki_df = wiki_df.loc[wiki_df['category'].isin(lnorm_cats)]
        # print(lnorm_wiki_df)
        print(f"Number of distinct categories that occur more or equal to {minA} times in the dataset = {len(lnorm_cats)}")
        print(f"Size of the corresponding dataset = {len(lnorm_wiki_df)}")

        #Choose articles that have categories that appear less than 100 times in total
        hnorm_cats = [x[0] for x in lnorm_cat_freqs if x[1] <=maxA]
        hnorm_wiki_df = lnorm_wiki_df.loc[lnorm_wiki_df['category'].isin(hnorm_cats)]
        print(f"Number of distinct categories that occur less or equal to {maxA} times in the dataset = {len(hnorm_cats)}")
        print(f"Size of the corresponding dataset = {len(hnorm_wiki_df)}")

        #Choose articles that have categories that appear more than 100 times in total and reduce the number of their appearances
        big_cats = [x[0] for x in freqs if x[1]>maxA]
        big_in_wiki_df = lnorm_wiki_df.loc[lnorm_wiki_df['category'].isin(big_cats)]
        big_wiki_df = pd.concat([pd.concat([lnorm_wiki_df.loc[lnorm_wiki_df['category'] == cat].head(maxA)]) for cat in big_cats])
        print(f"Number of distinct categories that occur more than {maxA} times in the dataset = {len(big_cats)}")
        print(f"Size of the corresponding dataset = {len(big_in_wiki_df)}")
        print(f"Size of the corresponding dataset after being reduced = {len(big_wiki_df)}")


        #Final combined dataset
        res_df = pd.concat([hnorm_wiki_df, big_wiki_df])
        print(f"Size of the final dataset = {len(res_df)}")
        with tf.Session() as session:
            session.run([tf.global_variables_initializer(), tf.tables_initializer()])
            self.wiki_features = session.run(embed(res_df['text'].tolist()))

        self.wiki_labels = res_df['category']

    def train():
        self.model = LogisticRegression(random_state=0)
        # model = ClassifierChain(LogisticRegression())
        self.model.fit(self.wiki_features, self.wiki_labels)

    def loadModel(self, filename):
        self.model = joblib.load(filename)
        print(f"[Classifier] Model loaded from {filename}")

    def saveModel(self, filename):
        joblib.dump(self.model, filename)
        print(f"[Classifier] Model saved to {filename}")

    def calcAccuracy(self):
        self.acc = cross_val_score(self.model, self.wiki_features, self.wiki_labels, scoring='accuracy', cv=5)
        print(self.acc.mean())
