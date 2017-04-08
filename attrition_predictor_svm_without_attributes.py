import numpy as np
import pandas as pd

from sklearn.naive_bayes import GaussianNB
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import LeaveOneOut, KFold

df = pd.read_csv("FinalDatasetWithoutAttributes.csv")
df.Sex = df.Sex.replace("f", 0).replace("m", 1)
label = df.Withdrew.astype(int)
features = df.drop("Withdrew", axis=1).drop("Reason Code", axis=1)

feature_set = features.values
label_set = label.values

def LearnAndTest(feature_set, label_set):
    kf = KFold(n_splits = 10)
    correct = 0
    clf = svm.SVC()
    for train_indices, test_indices in kf.split(feature_set):
        X_train, y_train = getSets(feature_set, label_set, train_indices)
        X_test, y_test = getSets(feature_set, label_set, test_indices)
        clf.fit(X_train, y_train)
        prediction = clf.predict(X_test)
        print("Count of Correct:", correct)
        correct += checkPrediction(label_set, prediction, test_indices)
    accuracy = correct/len(feature_set)
    print("SVM accuracy with K Folds strategy: ", accuracy)

def LearnAndTest2(feature_set, label_set):
    kf = KFold(n_splits = 10)
    correct = 0
    clf = GaussianNB()
    for train_indices, test_indices in kf.split(feature_set):
        X_train, y_train = getSets(feature_set, label_set, train_indices)
        X_test, y_test = getSets(feature_set, label_set, test_indices)
        clf.fit(X_train, y_train)
        prediction = clf.predict(X_test)
        print("Count of Correct:", correct)
        correct += checkPrediction(label_set, prediction, test_indices)
    accuracy = correct/len(feature_set)
    print("Gaussian NB accuracy with K Folds strategy: ", accuracy)

def LogisticRegressionClassifier(feature_set, label_set):
    kf = KFold(n_splits = 10)
    correct = 0
    clf = LogisticRegression()
    for train_indices, test_indices in kf.split(feature_set):
        X_train, y_train = getSets(feature_set, label_set, train_indices)
        X_test, y_test = getSets(feature_set, label_set, test_indices)
        clf.fit(X_train, y_train)
        prediction = clf.predict(X_test)
        print("Count of Correct:", correct)
        correct += checkPrediction(label_set, prediction, test_indices)
    accuracy = correct/len(feature_set)
    print("Logistic Regression accuracy with K Folds strategy: ", accuracy)

def checkPrediction(label_set, prediction, indices):
    correct = 0
    predict_index = 0
    for index in indices:
        if label_set[index] == prediction[predict_index]:
            correct += 1
        predict_index += 1
    return correct

def getSets(feature_set, label_set, indices):
    X, y = [], []
    for index in indices:
        X.append(feature_set[index])
        y.append(label_set[index])
    return X, y

LearnAndTest(feature_set, label_set)
LearnAndTest2(feature_set, label_set)
LogisticRegressionClassifier(feature_set, label_set)
