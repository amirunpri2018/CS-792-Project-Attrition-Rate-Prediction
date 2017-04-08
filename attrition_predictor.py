import numpy as np
import pandas as pd

from sklearn.naive_bayes import GaussianNB
from sklearn import svm, tree
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import LeaveOneOut, KFold

def LearnAndTest(feature_set, label_set, clf, clf_name, dataset_name):
    kf = KFold(n_splits = 10)
    correct = 0
    for train_indices, test_indices in kf.split(feature_set):
        X_train, y_train = getSets(feature_set, label_set, train_indices)
        X_test, y_test = getSets(feature_set, label_set, test_indices)
        clf.fit(X_train, y_train)
        prediction = clf.predict(X_test)
        correct += checkPrediction(label_set, prediction, test_indices)
    accuracy = correct/len(feature_set)
    print(clf_name, "with K Folds strategy has an accuracy of", accuracy, 'for dataset', dataset_name)

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

def main(dataset_name):
    df = pd.read_csv(dataset_name)
    df.Sex = df.Sex.replace("f", 0).replace("m", 1)
    label = df.Withdrew.astype(int)
    features = df.drop("Withdrew", axis=1).drop("Reason Code", axis=1)

    feature_set = features.values
    label_set = label.values

    svm_clf = svm.SVC()
    LearnAndTest(feature_set, label_set, svm_clf, "Support Vector Machine", dataset_name)

    gnb_clf = GaussianNB()
    LearnAndTest(feature_set, label_set, gnb_clf, "Gaussian Naive Bayes", dataset_name)

    logistic_clf = LogisticRegression()
    LearnAndTest(feature_set, label_set, logistic_clf, 'Logistic Regression', dataset_name)

    neural_net_clf = MLPClassifier(hidden_layer_sizes=(100, 100))    
    LearnAndTest(feature_set, label_set, neural_net_clf, 'Neural Network', dataset_name)
    
    tree_clf = tree.DecisionTreeClassifier(max_features=3, max_depth=2)
    LearnAndTest(feature_set, label_set, tree_clf, 'Decision Tree', dataset_name)

if __name__ == '__main__':
    main("FinalDatasetWithAttributes.csv")
    main("FinalDatasetWithoutAttributes.csv")