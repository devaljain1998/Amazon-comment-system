# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

# Visualization
import matplotlib.pyplot as plt
# from matplotlib.ticker import FuncFormatter
# import seaborn as sns

# sklearn for feature extraction & modeling
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
# from sklearn.model_selection import GridSearchCV

# from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

class MachineLearning:
    filename = ''
    product_average_rating=0
    # sns.set(color_codes = True)

    def import_csvfile():
        print('\nImporting Train set data csv file ...')
        df = pd.read_csv('testdata.csv')

        #Getting the head of data
        df.head()
        
        #Calling pipeline function
        MachineLearning.func_pipeline(df)

    def func_pipeline(df):
        print('\nFitting pipeline ...')
        clf = Pipeline([
            ('vect', CountVectorizer(stop_words= "english")),
            ('tfidf', TfidfTransformer()),
            ('classifier', RandomForestClassifier(n_jobs= -1)),
            ])
        
        # Remove records with blank values
        df_1 = df.dropna()
        df_1.shape , df.shape

        #Calling test train data function
        MachineLearning.test_train_data(df_1, clf)

    def test_train_data(df_1, clf):
        print('\nSetting training and test data in model ...')
        X_train, X_test, y_train, y_test = train_test_split(df_1['TITLE'], df_1['RATING'], random_state=10 ,test_size = 0.01)
        X_train.shape,X_test.shape,y_train.shape, y_test.shape

        print('\nFitting training data in model ...')
        model = clf.fit(X_train,y_train)

        print("Accuracy of Classifier is {}".format(model.score(X_test,y_test)))

        y_predicted = model.predict(X_test)
        # y_predicted[0:10]

        #Confusion Matrix
        # Compute confusion matrix
        cnf_matrix = confusion_matrix(y_test, y_predicted)
        np.set_printoptions(precision=2)
        #cnf_matrix

        #Calling read amazon cav file function
        filename = MachineLearning.filename
        MachineLearning.read_amazon_csv_file(clf, filename)

    def read_amazon_csv_file(clf, filename):
        print('\nImporting the Amzon web scraping csv file ...')
        new_dataset = pd.read_csv(filename)
        new_X = new_dataset['Title']

        #example = ['Worst battery in expensive iphone']
        model = clf.predict(new_X)
        print(f'\nIndividual rating prediction :- {model}')
            
        average = model.sum()/len(model)
        
        MachineLearning.average_rating(average)
                
    def average_rating(average):
        print(f'\nAverage Rating :- {average}')
        MachineLearning.product_average_rating = average
        return average

