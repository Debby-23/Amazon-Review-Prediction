# -*- coding: utf-8 -*-
"""amazon_product_review.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FXIPgyCrPTlGjAvCJDrYbc4lTHTV45eh
"""

!wget http://deepyeti.ucsd.edu/jianmo/amazon/categoryFilesSmall/Software_5.json.gz

# Commented out IPython magic to ensure Python compatibility.
import os
import json
import gzip
import pandas as pd
import matplotlib
# %matplotlib inline
import seaborn
from urllib.request import urlopen
import tensorflow
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np

data = []
with gzip.open('Software_5.json.gz') as f:
    for l in f:
        data.append(json.loads(l.strip()))

#print(len(data)) -->12805
train_data = data[:10244]
train_df = pd.DataFrame.from_dict(train_data)

#train_df.describe()

train_df.drop(columns = ['vote', 'image','verified','reviewerID','unixReviewTime','style','reviewerName','reviewText','reviewTime'],axis=1,inplace=True)
train_df['summary'] = train_df['summary'].astype(str)
train_df.head()

test_data = data[10244:]
test_df = pd.DataFrame.from_dict(test_data)

test_df.drop(columns=['vote', 'image','verified','reviewerID','unixReviewTime','style','reviewerName','reviewText','reviewTime'],axis=1,inplace=True)
test_df['summary'] = test_df['summary'].astype(str)
#test_df.head()

train = train_df[['summary', 'overall']] #train and test frequencies remain proportional still biased to 4 and 5 rating
train['overall'].hist()

#text pre-processing

from nltk.corpus import stopwords    
from textblob import Word

stoplist = set(stopwords.words('english'))

# For frequent words removal
freq = pd.Series(' '.join(train_df['summary']).split()).value_counts()[:10]
freq = list(freq.index)


# For rare words removal 
freq1 = pd.Series(' '.join(train_df['summary']).split()).value_counts()[-10:]
freq1=list(freq1.index)


def cleaning_text(df):
    df['summary'] = df['summary'].str.lower().str.replace('[^\w\s]','')                                                               # Punctuation Removal
    df['summary'] = df['summary'].apply( lambda x: ' '.join([w for w in str(x).split() if w not in stoplist]) )                       # Removing stopwords
    df['summary']= df['summary'].apply( lambda x:' '.join(x for x in x.split(" ") if not x.isdigit()) )                               # Numbers Removal
    df['summary'] = df['summary'].apply(lambda x: ' '.join(x for x in x.split(" ") if x not in freq))                                 # Frequent words removal
    df['summary'] = df['summary'].apply(lambda x: " ".join(x for x in x.split(" ") if x not in freq1))                                # Rare words removal
    df['summary'] = df['summary'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))                           # Lemmatization
    

cleaning_text(train_df)
cleaning_text(test_df)
train_df.head()
# Pre-processing of both the training and testing datasets is done .

wordcloud = WordCloud(background_color='white').generate(' '.join(train_df['summary']))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
X = train_df['summary']
y = train_df['overall']
cv = CountVectorizer()
X = cv.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.9)
mnb = KNeighborsClassifier()
mnb.fit(X_train, y_train)
y_test_pred = mnb.predict(X_test)
print(classification_report(y_test,y_test_pred))