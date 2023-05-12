import pickle
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import os

with open(os.path.dirname(os.path.realpath(__file__)) + '/per_hate_classifier.pkl', "rb") as f:
    loaded_clf = pickle.load(f)

with open(os.path.dirname(os.path.realpath(__file__)) + '/vectorizer.pk', "rb") as f:
    loaded_vct = pickle.load(f)

def prediction(text):
    text_v = loaded_vct.transform([text])

    return loaded_clf.predict(text_v)

