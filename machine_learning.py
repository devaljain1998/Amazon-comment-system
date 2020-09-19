# -*- coding: utf-8 -*-

import glob
import os
import numpy as np
import pandas as pd

# Visualization
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import seaborn as sns

# sklearn for feature extraction & modeling
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

class MachineLearning:

    sns.set(color_codes = True)

    def import_csvfile():
        print('\nImporting Train set data csv file ...')
        df = pd.read_csv('pdata.csv')

        #Getting the head of data
        df.head()
        
        #Caling pipeline function
        MachineLearning.func_pipeline(df)

    #Library for building wordcloud
    def word_cloud(df):
        heading_1 = df[df["RATING"]==1]["TITLE"] # Extract only Summary of reviews
        collapsed_heading_1 = heading_1.str.cat(sep=' ')

        heading_2 = df[df["RATING"]==2]["TITLE"] # Extract only Summary of reviews
        collapsed_heading_2 = heading_2.str.cat(sep=' ')

        heading_3 = df[df["RATING"]==3]["TITLE"] # Extract only Summary of reviews
        collapsed_heading_3 = heading_3.str.cat(sep=' ')

        heading_4 = df[df["RATING"]==4]["TITLE"] # Extract only Summary of reviews
        collapsed_heading_4 = heading_4.str.cat(sep=' ')

        heading_5 = df[df["RATING"]==5]["TITLE"] # Extract only Summary of reviews
        collapsed_heading_5 = heading_5.str.cat(sep=' ')

        # Create stopword list:
        # stopwords = set(STOPWORDS)
        #stopwords.update(["Subject","re","fw","fwd"])

        #Graphs
        '''
        print("Word Cloud for Rating 1")

        # Generate a word cloud image
        wordcloud = WordCloud(stopwords=stopwords, background_color="white",max_words=50).generate(collapsed_heading_1)

        # Display the generated image:
        # the matplotlib way:1
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()

        print("\nWord Cloud for Rating 2")

        # Generate a word cloud image
        wordcloud = WordCloud(stopwords=stopwords, background_color="white",max_words=50).generate(collapsed_heading_2)

        # Display the generated image:
        # the matplotlib way:1
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()

        print("\nWord Cloud for Rating 3")
        # Generate a word cloud image
        wordcloud = WordCloud(stopwords=stopwords, background_color="white",max_words=50).generate(collapsed_heading_3)

        # Display the generated image:
        # the matplotlib way:1
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()

        print("\nWord Cloud for Rating 4")

        # Generate a word cloud image
        wordcloud = WordCloud(stopwords=stopwords, background_color="white",max_words=50).generate(collapsed_heading_4)

        # Display the generated image:
        # the matplotlib way:1
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
            
        print("\nWord Cloud for Rating 5")
        # Generate a word cloud image
        wordcloud = WordCloud(stopwords=stopwords, background_color="white",max_words=50).generate(collapsed_heading_5)

        # Display the generated image:
        # the matplotlib way:1
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        '''
        
    def func_pipeline(df):
        # Building Pipeline for raw text transformation
        '''clf = Pipeline([
            ('vect', CountVectorizer(stop_words= "english")),
            ('tfidf', TfidfTransformer()),
            ('classifier', MultinomialNB()),
            ])'''
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

        #print("Accuracy of Classifier is {}".format(model.score(X_test,y_test)))

        y_predicted = model.predict(X_test)
        y_predicted[0:10]

        #Confusion Matrix
        # Compute confusion matrix
        cnf_matrix = confusion_matrix(y_test, y_predicted)
        np.set_printoptions(precision=2)
        #cnf_matrix

        #Calling read amazon cav file function
        MachineLearning.read_amazon_csv_file(clf)

    def read_amazon_csv_file(clf):
        print('\nImporting the Amzon web scraping csv file ...')
        new_dataset = pd.read_csv('reviews.csv')
        new_X = new_dataset['Title']

        #example = ['Worst battery in expensive iphone']
        model = clf.predict(new_X)
        print(f'\nIndividual rating prediction :- {model}')
            
        average = model.sum()/len(model)
        print(f'\nAverage Rating :- {average}')

#MachineLearning.import_csvfile()