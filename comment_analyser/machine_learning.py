# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

# Visualization
import matplotlib.pyplot as plt

# sklearn for feature extraction & modeling
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from .algo import NaiveBayesAlgorithm, LogisticRegressionAlgorithm, SentiWordNetAlgorithm, RandomForestClassifierAlgorithm, KNeighborsClassifierAlgorithm
# from average_rating import AverageRating

class ReviewSentimentalAnalyser:
    filename = ''
    product_average_rating=1
    percision = 0
    recall = 0
    f1_score = 0
    positive = 0
    negative = 0
    neutral = 0

    def import_csvfile(self, choose):
        print('\nImporting Train set data csv file ...')
        df = pd.read_csv('testdata.csv')

        #Getting the head of data
        df.head()
        
        #Calling pipeline function
        self.choose_algorithm(choose, df)
    def factory_method_design(self, obj = ''):
        objs = dict(
            a=NaiveBayesAlgorithm(), 
            b=LogisticRegressionAlgorithm(), 
            c=SentiWordNetAlgorithm(), 
            d=RandomForestClassifierAlgorithm(),
            e=KNeighborsClassifierAlgorithm()
            )
        return objs[obj]

    def choose_algorithm(self, choose, df):
        filename = self.filename
        algorithm = self.factory_method_design(choose)
        algorithm.algorithm(df, filename)
        # PipelineClass.func_pipeline(df)
        
    def read_amazon_csv_file(self, clf, filename):
        print('\nImporting the Amzon web scraping csv file ...')
        print(filename)
        new_dataset = pd.read_csv(filename)
        new_X = new_dataset['Title']

        #example = ['Worst battery in expensive iphone']
        model = clf.predict(new_X)
        print(f'\nIndividual rating prediction :- {model}')

        self.get_review_rate(model, new_dataset)

        average = model.sum()/len(model)
        print(average)
        self.average_rating(average)
                
    def average_rating(self, average):
        print(f'\nAverage Rating :- {average}')
        ReviewSentimentalAnalyser.product_average_rating = average
        print(self.product_average_rating)
        # return average

    def get_review_rate(self, average, new_dataset):
        get_rating = new_dataset['Rating'].to_list()
        rating_list = []
        print(get_rating)
        for rating in range(0, len(get_rating)):
            print('@@@@@@@@@@@@@@@@@@@@@@@@@@@')
            print(get_rating[rating])
            try:
                rate = get_rating[rating].split(" ")
                rating_list.append(float(rate[0]))
            except Exception:
                rate = get_rating[rating]
                rating_list.append(float(rate))

        print('Original Rating')
        print(rating_list)
        print('Predictied Rating')
        print(average)

        true_positive = 0
        true_negative = 0
        false_positive = 0
        false_negative = 0
        positive = 0
        negative = 0
        neutral = 0

        for rate in range(0, len(rating_list)):
            if rating_list[rate] > 3:
                if average[rate] > 3:
                    true_positive += 1
                else:
                    false_positive += 1

            elif rating_list[rate] < 3:
                if average[rate] < 3:
                    true_negative += 1
                else:
                    false_negative += 1

            if average[rate] > 3:
                positive += 1
            elif average[rate] < 3:
                negative += 1
            else:
                neutral += 1

        
        print(f'Original Positive Rating :- {true_positive}, Original Negative Rating :- {true_negative}')
        print(f'Predicted Positive Rating :- {false_positive}, Predicted Negative Rating :- {false_negative}')

        percision = true_positive / (true_positive + false_positive)
        recall = true_positive / (true_positive + false_negative)
        f1_score = 2*(recall * percision) / (recall + percision)

        ReviewSentimentalAnalyser.percision = round(percision, 2)
        ReviewSentimentalAnalyser.recall = round(recall, 2)
        ReviewSentimentalAnalyser.f1_score = round(f1_score, 2)
        ReviewSentimentalAnalyser.positive = positive
        ReviewSentimentalAnalyser.negative = negative
        ReviewSentimentalAnalyser.neutral = neutral

        print(f'Precision :- {self.percision}, Recall :- {self.recall}, F1 Score :- {self.f1_score}')
        print(f'Precision :- {round(self.percision, 2)}, Recall :- {round(self.recall, 2)}, F1 Score :- {round(self.f1_score, 2)}')
        print(f'Positive :- {self.positive} Negative :- {self.negative} Positive :- {self.neutral}')