
#!/Users/morozovgleb/anaconda/bin/python
# -*- coding: utf-8 -*-
import sys
import pandas as pd
# import numpy as np
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.linear_model import LogisticRegression
# from sklearn.multiclass import OneVsRestClassifier
from sklearn.externals import joblib
from pymystem3 import Mystem


# print 'Number of arguments:', len(sys.argv), 'arguments.'
# print 'Argument List:', str(sys.argv)


def tfidf_preproc(text):
    return filter(lambda x: not x.isdigit(), text)

clf = joblib.load('/Users/morozovgleb/Documents/alfa_project/models/logreg_10000_07.pkl')
vectorizer = joblib.load('/Users/morozovgleb/Documents/alfa_project/models/tfidf_vectorizer_all_data_10000.pkl')
category_names = ['autocredits',
                  'businesscredits',
                  'businessdeposits',
                  'corporate',
                  'creditcards',
                  'credits',
                  'debitcards',
                  'deposits',
                  'hypothec',
                  'leasing',
                  'remote',
                  'restructing']



stem = Mystem()


def predict_from_text(text, classifier, cat_names, vectorizer):
    text = pd.Series({'review': ''.join(stem.lemmatize(text))})
    text = vectorizer.transform(text)
    predict_cat = list(classifier.predict(text)[0])
    answer = [cat_names[i] for i in range(len(predict_cat)) if predict_cat[i] == 1]
    return answer

text = sys.argv[1]

response = predict_from_text(text, clf, category_names, vectorizer)
for category in response:
    print category
