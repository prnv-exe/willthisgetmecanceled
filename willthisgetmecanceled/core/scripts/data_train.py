import numpy as np
import pandas as pd
import random
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import f1_score
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
import pickle
import os

class Messages:
    def __init__(self, tweet, hater):
        self.given_text = tweet
        self.label = hater
        self.is_hate = self.is_hater()

    def is_hater(self):
        if self.label == 'No':
            return False
        else:
            return True
        
class MessageContainer:
    def __init__(self, message):
        self.message = message
        
    def get_text(self):
        return [x.given_text for x in self.message]
    
    def get_sentiment(self):
        return [x.is_hate for x in self.message]
        
    def evenly_distribute(self):
        positive = list(filter(lambda x: x.is_hate == False, self.message))
        hate = list(filter(lambda x: x.is_hate == True, self.message))
        positive_shrunk = positive[:len(hate)]
        self.reviews = hate + positive_shrunk
        random.shuffle(self.reviews)
    
    def len(self):
        return len(self.message)
    

def SetCreator(arr, arr2, param):
    if param == 'text':
        for x in range(0, arr2.len()):
            buffer = arr2.get_text()[x]
            arr.append(buffer)
    elif param == 'hate':
        for x in range(0, arr2.len()):
            buffer = arr2.get_sentiment()[x]
            arr.append(buffer)

def Categoriser(df, type):
    for x in df.index:
        if type in df['text'][x]:
            print(df['text'][x])



def train_it(data):


    df = pd.DataFrame(data, columns=['text', 'label'])

    message_container = []

    for x in df.index:
        message = Messages(df['text'][x],df['label'][x])
        message_container.append(message)

    train_container = MessageContainer(message_container)
    

    train_container.evenly_distribute()

    train_x = []
    train_y = []

    SetCreator(train_x, train_container, param='text')
    SetCreator(train_y, train_container, param='hate')

    with open(os.path.dirname(os.path.realpath(__file__)) + '/per_hate_classifier.pkl', 'rb') as f:
        model = pickle.load(f)
    with open(os.path.dirname(os.path.realpath(__file__)) + '/vectorizer.pk', 'rb') as f:
        vectorizer = pickle.load(f)
    
    vectorizer.partial_fit(train_x)
    if not train_x:
        pass

    else:
        train_x_vectors = vectorizer.transform(train_x)


        model.partial_fit(train_x_vectors, train_y)

        with open(os.path.dirname(os.path.realpath(__file__)) + '/per_hate_classifier.pkl', 'wb') as f:
            pickle.dump(model, f)

        with open(os.path.dirname(os.path.realpath(__file__)) + '/vectorizer.pk', 'wb') as fin:
            pickle.dump(vectorizer, fin)