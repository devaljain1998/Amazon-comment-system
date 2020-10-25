from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix


class TestTrainData:
    def test_train_data(df_1, clf):
        print('\nSetting training and test data in model ...')
        X_train, X_test, y_train, y_test = train_test_split(df_1['TITLE'], df_1['RATING'], random_state=10 ,test_size = 0.01)

        print('\nFitting training data in model ...')
        model = clf.fit(X_train,y_train)

        # print("Accuracy of Classifier is {}".format(model.score(X_test,y_test)))

        y_predicted = model.predict(X_test)

        #Confusion Matrix
        # Compute confusion matrix
        cnf_matrix = confusion_matrix(y_test, y_predicted)
        
        from .machine_learning import ReviewSentimentalAnalyser

        #Calling read amazon cav file function
        review_sentimental_analyser = ReviewSentimentalAnalyser()
        filename = review_sentimental_analyser.filename
        print(f'FILEnAMNE ----------------------- {filename}')
        review_sentimental_analyser.read_amazon_csv_file(clf, filename)