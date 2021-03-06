# -*- coding: utf-8 -*-
"""featureEngineeringandModeling.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/112KFqEqYzyoZFey6n4j-E-5nBs1NfE_9
"""

from psutil import virtual_memory
ram_gb = virtual_memory().total / 1e9
print('Your runtime has {:.1f} gigabytes of available RAM\n'.format(ram_gb))

if ram_gb < 20:
  print('To enable a high-RAM runtime, select the Runtime > "Change runtime type"')
  print('menu, and then select High-RAM in the Runtime shape dropdown. Then, ')
  print('re-execute this cell.')
else:
  print('You are using a high-RAM runtime!')

pip install pandas-profiling

!pip install tweepy
!pip install wordcloud
!pip install textblob

import pandas_profiling
import tweepy                   
from google.colab import drive  
import json
import csv
from datetime import date
from datetime import datetime
import time
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sb
import re
import time
import string
import warnings

# for all NLP related operations on text
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import *
from wordcloud import WordCloud
import matplotlib.animation as animation
import operator
import plotly.express as px
from collections import Counter

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, confusion_matrix
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB


# To consume Twitter's API
import tweepy
from tweepy import OAuthHandler 

# To identify the sentiment of text
from textblob import TextBlob

# ignoring all the warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# downloading stopwords corpus
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('vader_lexicon')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
stopwords = set(stopwords.words("english"))

drive.mount('/content/gdrive')
path = './gdrive/MyDrive/WDPS_data'

df = pd.read_csv("/content/gdrive/MyDrive/WDPS_Data/cleanedElectiontweetsFinal")

df.head()

df = df.drop(['renderedContent'], axis = 1)
df = df.drop(['id'], axis = 1)
df = df.drop(['Count(#)'], axis = 1)

df.shape

dff = df.drop(['sentiment'], axis = 1)

dff.shape

from sklearn.model_selection import train_test_split
x_temp, x_test, y_temp, y_test = train_test_split(dff, list(df.sentiment), test_size=0.1)

x_test.shape

x_temp.shape

len(y_test)

type(y_temp)

x_temp['sentiment'] = y_temp

x_temp.head()

type(x_temp)

positive = x_temp[x_temp['sentiment'] == 'positive']

positive.head()

negative = x_temp[x_temp['sentiment'] == 'negative']

negative.head()

negative.shape[0]

positivesample = positive.sample(n = negative.shape[0])

positivesample.head()

positivesample.shape

ds = pd.concat([negative, positivesample], axis = 0)

ds.tail()

ds.shape

ds.to_csv("/content/gdrive/MyDrive/WDPS_Data/trainset.csv")

ds.head()

ds_temp = ds

test_df = x_test
test_df['sentiment'] = y_test

ds_temp.shape

test_df.shape

ds = pd.concat([ds_temp, test_df], axis = 0)

ds.head()

ds.shape

test_df.head()

list(test_df.index)

corpus = []
for i in range(ds.shape[0]):
    corpus.append(ds.iloc[i][0])

len(corpus)

from sklearn.feature_extraction.text import TfidfVectorizer

tfidf_vectors = TfidfVectorizer(max_df=0.90, min_df=2, max_features=9000, 
                                stop_words='english',
                                ngram_range=(1, 3))

tfidf_only_fit = tfidf_vectors.fit(corpus)

tfidf = tfidf_vectors.fit_transform(corpus)

df_vector = pd.DataFrame(tfidf.todense(),columns = tfidf_vectors.get_feature_names())

df_vector

tdf = df_vector
tdf['labelxyz'] = list(ds.sentiment)

tdf.tail()

tdf_negative = tdf[tdf.labelxyz == 'negative']

tdf_negative.shape

tdf_positive = tdf[tdf.labelxyz == 'positive']

tdf_positive.shape

x_train_negative = tdf_negative.sample(frac=0.9, random_state=0)

x_test_negative = tdf_negative.drop(x_train_negative.index)

x_train_positive =  tdf_positive.sample(frac=0.406, random_state=0)

x_test_positive = tdf_positive.drop(x_train_positive.index)

x_train_df = pd.concat([x_train_negative, x_train_positive], axis = 0)

x_train = x_train_df.drop(['labelxyz'], axis = 1)

y_train = list(x_train_df.labelxyz)

x_test_df = pd.concat([x_test_negative, x_test_positive], axis = 0)

x_test = x_test_df.drop(['labelxyz'], axis = 1)

y_test = list(x_test_df.labelxyz)

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB

from sklearn.model_selection import cross_val_score

LR = LogisticRegression()
LR_scores = cross_val_score(LR, x_train, y_train, cv=3)
LR_mean = LR_scores.mean()

NB = GaussianNB()
NB_scores = cross_val_score(NB, x_train, y_train, cv=3)
NB_mean = NB_scores.mean()

d = {'Classifiers': ['Logistic Reg.', 'Naives Bayes'], 
    'Crossval Mean Scores': [LR_mean, NB_mean]}
    
result_df = pd.DataFrame(data=d)

result_df

from sklearn.metrics import accuracy_score
NB = GaussianNB()
NB.fit(x_train, y_train)
predict_NB = NB.predict(x_test)
accuracy_score(y_test, predict_NB)

from sklearn.metrics import confusion_matrix
confusion_matrix(y_test, predict_NB)

predictedLabelsNB = predict_NB[np.newaxis].T
predictedLabelsNB

LR = LogisticRegression()
LR.fit(x_train, y_train)
predict_LR = LR.predict(x_test)
accuracy_score(y_test, predict_LR)

from sklearn.metrics import confusion_matrix
confusion_matrix(y_test, predict_LR)

predictedLabelsLog = predict_LR[np.newaxis].T
predictedLabelsLog

from sklearn.ensemble import RandomForestClassifier

RF = RandomForestClassifier()
RF.fit(x_train, y_train)
predict_RF = RF.predict(x_test)
accuracy_score(y_test, predict_RF)

confusion_matrix(y_test, predict_RF)

predictedLabelsRF = predict_RF[np.newaxis].T
predictedLabelsRF

from sklearn import tree
DT = tree.DecisionTreeClassifier()
DT.fit(x_train, y_train)
predict_DT = DT.predict(x_test)
accuracy_score(y_test, predict_DT)

confusion_matrix(y_test, predict_DT)

predictedLabelsDT = predict_DT[np.newaxis].T
predictedLabelsDT

from sklearn.ensemble import GradientBoostingClassifier
GB = GradientBoostingClassifier()
GB.fit(x_train, y_train)
predict_GB = GB.predict(x_test)
accuracy_score(y_test, predict_GB)

confusion_matrix(y_test, predict_GB)

predictedLabelsGB = predict_GB[np.newaxis].T
predictedLabelsGB

