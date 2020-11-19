import nltk
import statistics
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize

from .test_train_data import TestTrainData

class NaiveBayesAlgorithm:
    def algorithm(df, filename):
        print('Naïve Bayes')
        print('\nFitting pipeline ...')
        clf = Pipeline([
            ('vect', CountVectorizer(stop_words= "english")),
            ('tfidf', TfidfTransformer()),
            ('classifier', MultinomialNB()),
            ])

        df_1 = df.dropna()
        TestTrainData.test_train_data(df_1, clf)

class LogisticRegressionAlgorithm:
    def algorithm(df, filename):
        print('Logistic Regression')
        print('\nFitting pipeline ...')
        clf = Pipeline([
            ('vect', CountVectorizer(stop_words= "english")),
            ('tfidf', TfidfTransformer()),
            ('classifier', LogisticRegression()),
            ])

        df_1 = df.dropna()
        TestTrainData.test_train_data(df_1, clf)

class SentiWordNetAlgorithm:
    # df = pd.read_csv('reviews_0.csv')
    # title = df['Title']

    ps = PorterStemmer()
    lemmatizer = WordNetLemmatizer()    

    stop_words = set(stopwords.words('english'))

    filtered_sentence = []
    all_rating = []

    def algorithm(df, filename):
        print(filename)
        SentiWordNetAlgorithm.main_algo(filename)

    def pnn_to_wn(tag):
        if tag.startswith('J'):
            return wn.ADJ
        elif tag.startswith('N'):
            return wn.NOUN
        elif tag.startswith('R'):
            return wn.ADV
        elif tag.startswith('V'):
            return wn.VERB


    def get_sentiment(word, tag):    
        wn_tag = SentiWordNetAlgorithm.pnn_to_wn(tag)
        
        if wn_tag not in (wn.NOUN, wn.ADJ, wn.ADV):
            return [0, 0]
        lemma = SentiWordNetAlgorithm.lemmatizer.lemmatize(word, pos=wn_tag)
        if not lemma:
            return [0, 0]
        synsets = wn.synsets(word, pos=wn_tag)
        if not synsets:
            return [0, 0]
        synset = synsets[0]
        swn_synset = swn.senti_synset(synset.name())
        return [swn_synset.pos_score(),swn_synset.neg_score()]
    
    def main_algo(filename):
        df = pd.read_csv(filename)
        title = df['Title']
        for word in title:
            word_tokens = word_tokenize(word)
            for w in word_tokens:
                if w not in SentiWordNetAlgorithm.stop_words:
                    SentiWordNetAlgorithm.filtered_sentence.append(w)
            pos_val = nltk.pos_tag(SentiWordNetAlgorithm.filtered_sentence)
            senti_val = [SentiWordNetAlgorithm.get_sentiment(x, y) for (x, y) in pos_val]
            rate = 0
            average = 0
            rating_list = []
            for rating in senti_val:
                rate = rating[0]-rating[1]
                rating_list.append(rate)
            if len(rating_list) != 0:
                average = statistics.mean(rating_list)
                if average >= 0:
                    average = 5
                elif average < 0:
                    average = 1
            else:
                average = 3
            SentiWordNetAlgorithm.all_rating.append(average)
            SentiWordNetAlgorithm.filtered_sentence = []

        average_product_rating = statistics.mean(SentiWordNetAlgorithm.all_rating)

        from .machine_learning import ReviewSentimentalAnalyser

        review_sentimental_analyser = ReviewSentimentalAnalyser()
        review_sentimental_analyser.average_rating(average_product_rating)
        new_dataset = pd.read_csv(filename)
        review_sentimental_analyser.get_review_rate(SentiWordNetAlgorithm.all_rating, new_dataset)
        
