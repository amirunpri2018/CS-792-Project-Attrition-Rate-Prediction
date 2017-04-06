import csv
import sys
import os
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import LeaveOneOut, KFold

def load(dataset_path):
	dataset = []
	with open(dataset_path, 'r') as dataset_file:
		dataset_reader = csv.reader(dataset_file)
		data_lines = list(dataset_reader)
		for line in data_lines:
			dataset.append(line)
	return dataset

def getFeatures(dataset):
	feature_set, label_set = [], []
	for data_point in dataset:
		label_set.append(data_point.pop(4))
		feature_set.append(data_point)
	return feature_set, label_set

def convertFeatures(feature_set):
	new_feature_set = []
	for features in feature_set:
		new_feature = []
		for feature_i in range(len(features)):
			if feature_i == 1:
				if features[feature_i] == 'm':
					new_feature.append(0)
				else:
					new_feature.append(1)
			else:
				new_feature.append(int(features[feature_i]))
		new_feature_set.append(new_feature)
	return new_feature_set

def convertLabels(label_set):
	new_label_set = []
	for label in label_set:
		if label == 'TRUE':
			new_label_set.append(1)
		else:
			new_label_set.append(0)
	return new_label_set

def getSets(feature_set, label_set, indices):
	X, y = [], []
	for index in indices:
		X.append(feature_set[index])
		y.append(label_set[index])
	return X, y

def checkPrediction(label_set, prediction, indices):
	correct = 0
	predict_index = 0
	for index in indices:
		if label_set[index] == prediction[predict_index]:
			correct += 1
		predict_index += 1
	return correct

def GNBKFolds(feature_set, label_set):
	kf = KFold(n_splits = 10)
	correct = 0
	for train_indices, test_indices in kf.split(feature_set):
		X_train, y_train = getSets(feature_set, label_set, train_indices)
		X_test, y_test = getSets(feature_set, label_set, test_indices)
		clf = GaussianNB()
		clf.fit(X_train, y_train)
		prediction = clf.predict(X_test)
		print("Count of Correct:", correct)
		correct += checkPrediction(label_set, prediction, test_indices)
	accuracy = correct/len(feature_set)
	print("Gaussian Naive Bayes' accuracy with K Folds strategy: ", accuracy)

def GNBLeaveOneOut(feature_set, label_set):
	loo = LeaveOneOut()
	correct = 0
	for train_indices, test_index in loo.split(feature_set):
		X_train, y_train = getSets(feature_set, label_set, train_indices)
		X_test = np.array(feature_set[test_index[0]])
		X_test = X_test.reshape(1, -1)
		clf = GaussianNB()
		clf.fit(X_train, y_train)
		prediction = clf.predict(X_test)
		print("Count of Correct:", correct)
		correct += checkPrediction(label_set[test_index[0]], prediction[0])
	accuracy = correct/len(feature_set)
	print("Gaussian Naive Bayes' accuracy with Leave One Out strategy: ", accuracy)

def main(dataset_name):
	current_path = os.path.dirname(os.path.abspath(__file__)) + '\\'
	dataset_path = current_path + dataset_name + '.csv'
	dataset = load(dataset_path)
	features = dataset.pop(0)
	feature_set, label_set = getFeatures(dataset)
	feature_set = convertFeatures(feature_set)
	label_set = convertLabels(label_set)
	#GNBLeaveOneOut(feature_set, label_set)
	GNBKFolds(feature_set, label_set)

if __name__ == '__main__':
	main('FinalDatasetWithoutAttributes')