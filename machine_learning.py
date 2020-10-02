# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

# Visualization
import matplotlib.pyplot as plt

# sklearn for feature extraction & modeling
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from algo import PipelineClass, PipelineNB, PipelineLR, PipelineSWN
# from average_rating import AverageRating

class ReviewSentimentalAnalyser:
    filename = ''
    product_average_rating=0

    def import_csvfile(choose):
        print('\nImporting Train set data csv file ...')
        df = pd.read_csv('testdata.csv')

        #Getting the head of data
        df.head()
        
        #Calling pipeline function
        ReviewSentimentalAnalyser.choose_algorithm(choose, df)
    def factory_method_design(obj = ''):
        objs = dict(a=PipelineNB, b=PipelineLR, c=PipelineSWN)
        return objs[obj]

    def choose_algorithm(choose, df):
        algorithm = ReviewSentimentalAnalyser.factory_method_design(choose)
        algorithm.func_pipeline(df)
        # PipelineClass.func_pipeline(df)
        
    def read_amazon_csv_file(clf, filename):
        print('\nImporting the Amzon web scraping csv file ...')
        print(filename)
        new_dataset = pd.read_csv(filename)
        new_X = new_dataset['Title']

        #example = ['Worst battery in expensive iphone']
        model = clf.predict(new_X)
        print(f'\nIndividual rating prediction :- {model}')
            
        average = model.sum()/len(model)
        print(average)
        ReviewSentimentalAnalyser.average_rating(average)
                
    def average_rating(average):
        print(f'\nAverage Rating :- {average}')
        ReviewSentimentalAnalyser.product_average_rating = average
        return average

