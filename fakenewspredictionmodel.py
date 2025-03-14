# -*- coding: utf-8 -*-
"""FakeNewsPredictionModel.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1p7-ryrcuIxbfU6FK5cMkl78gU74CGG7u

# FAKE NEWS PREDICTION MODEL
"""

import numpy as np
import re
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

news_df = pd.read_csv('train.csv')

news_df = pd.read_csv('train.csv', quoting=3)
# Tell pandas to ignore quotes

news_df = pd.read_csv('train.csv', quoting=3, on_bad_lines='skip')
# Use 'on_bad_lines' to skip bad lines

news_df.head()

"""## About the Dataset:

### id: unique id for a news article\
### title: the title of a news article\
### author: author of the news article\
### text: the text of the article; could be incomplete\
### label: a label that marks whether the news article is real or fake:\
### 1: Fake news\
### 0: real News

## Data Preprocessing
"""

news_df.isnull().sum()

news_df.shape

news_df = news_df.fillna(' ')

news_df.isnull().sum()

news_df['content'] = news_df['author']+' '+news_df['title']

news_df

"""## Separating the data & label"""

X = news_df.drop('label',axis=1)
y = news_df['label']

print(X)

"""## Stemming

## Steps:

### lower case
### splitting
### removing stopwords
### stemming
"""

ps = PorterStemmer()
def stemming(content):
    stemmed_content = re.sub('[^a-zA-Z]',' ',content)
    stemmed_content = stemmed_content.lower()
    stemmed_content = stemmed_content.split()
    stemmed_content = [ps.stem(word) for word in stemmed_content if not word in stopwords.words('english')]
    stemmed_content = ' '.join(stemmed_content)
    return stemmed_content

import nltk
nltk.download('stopwords')

news_df['content'] = news_df['content'].apply(stemming)

"""
## Separating the data and label
"""

X = news_df['content'].values
y = news_df['label'].values

"""## Converting the textual data to numerical data"""

vector = TfidfVectorizer()
vector.fit(X)
X = vector.transform(X)

print(X)

"""## Splitting the dataset to training & test data"""

X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size = 0.2, stratify=y, random_state=2)

# Check the distribution of your target variable 'y'
import pandas as pd
# Assuming 'y' is a pandas Series or a list
y_counts = pd.Series(y).value_counts()
print(y_counts)

# If a class has only one sample, consider the following:

# 1. Gather more data for the underrepresented class if possible.
# 2. If gathering more data is not feasible, you may have to:
#    - Combine the underrepresented class with another class if it makes sense in your context.
#    - Remove the sample belonging to the underrepresented class.
#    - Use a different splitting strategy that does not require stratification, such as simple random sampling.

# After addressing the class imbalance issue, retry the train_test_split:
# If you choose to use simple random sampling:
X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size = 0.2, random_state=2)
# Remove 'stratify=y' to perform simple random sampling.

X_train.shape

"""## Training the Model: Logistic Regression"""

model = LogisticRegression()
model.fit(X_train,Y_train)

# on training set
train_y_pred = model.predict(X_train)
print(accuracy_score(train_y_pred,Y_train))

# on testing set
testing_y_pred = model.predict(X_test)
print(accuracy_score(testing_y_pred,Y_test))



"""# Detection System"""

input_data = X_test[10]
prediction = model.predict(input_data)

if prediction[0] == 0:
    print('The News Is Real')
else:
    print('The News is Fake')

news_df['content'][2]

