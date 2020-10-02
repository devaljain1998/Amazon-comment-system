from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from nltk.corpus import sentiwordnet
from test_train_data import TestTrainData

class PipelineClass:
    def func_pipeline(df):
        print('\nFitting pipeline ...')
        clf = Pipeline([
            ('vect', CountVectorizer(stop_words= "english")),
            ('tfidf', TfidfTransformer()),
            ('classifier', RandomForestClassifier(n_jobs= -1)),
            ])

        df_1 = df.dropna()
        TestTrainData.test_train_data(df_1, clf)

class PipelineNB:
    def func_pipeline(df):
        print('Naïve Bayes')
        print('\nFitting pipeline ...')
        clf = Pipeline([
            ('vect', CountVectorizer(stop_words= "english")),
            ('tfidf', TfidfTransformer()),
            ('classifier', MultinomialNB()),
            ])

        df_1 = df.dropna()
        TestTrainData.test_train_data(df_1, clf)

class PipelineLR:
    def func_pipeline(df):
        print('Logistic Regression')
        print('\nFitting pipeline ...')
        clf = Pipeline([
            ('vect', CountVectorizer(stop_words= "english")),
            ('tfidf', TfidfTransformer()),
            ('classifier', LogisticRegression()),
            ])

        df_1 = df.dropna()
        TestTrainData.test_train_data(df_1, clf)

class PipelineSWN:
    def func_pipeline(df):
        print('SentiWordNet')
        print('\nFitting pipeline ...')
        clf = Pipeline([
            ('vect', CountVectorizer(stop_words= "english")),
            ('tfidf', TfidfTransformer()),
            ('nltk', sentiwordnet()),
            ])

        df_1 = df.dropna()
        TestTrainData.test_train_data(df_1, clf)
