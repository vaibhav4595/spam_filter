from nltk.corpus import stopwords
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

class document:
    def __init__(self, path1, path2):
        files = os.walk(path1).next()[2]
        #cached_stop_words = stopwords.words("english")
        self.arr_train = []
        self.hams_train = len(files)
        for each in files:
            f = open(os.path.join(path1, each))
            doc = str.decode(f.read(), "UTF-8", "ignore")
            #doc = ' '.join([word for word in doc.split() if word not in cachedStopWords])
            self.arr_train.append(doc)

        files = os.walk(path2).next()[2]
        self.spams_train = len(files)
        for each in files:
            f = open(os.path.join(path2, each))
            doc = str.decode(f.read(), "UTF-8", "ignore")
            self.arr_train.append(doc)

        self.len_train = len(self.arr_train)

    def set_test_vectors(self, path1, path2):
        files = os.walk(path1).next()[2]
        #cached_stop_words = stopwords.words("english")
        self.arr_test = []
        self.hams_test = len(files)
        for each in files:
            f = open(os.path.join(path1, each))
            doc = str.decode(f.read(), "UTF-8", "ignore")
            #doc = ' '.join([word for word in doc.split() if word not in cachedStopWords])
            self.arr_test.append(doc)

        files = os.walk(path2).next()[2]
        self.spams_test = len(files)
        for each in files:
            f = open(os.path.join(path2, each))
            doc = str.decode(f.read(), "UTF-8", "ignore")
            self.arr_test.append(doc)

        self.len_test = len(self.arr_test)

    def get_vectors(self):
        self.new_arr = self.arr_test  + self.arr_train
        tfidf_vectorizer = TfidfVectorizer()
        self.vectors = tfidf_vectorizer.fit_transform(self.new_arr)
        return self.vectors
