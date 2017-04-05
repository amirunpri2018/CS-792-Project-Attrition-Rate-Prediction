import sys
import os
import csv
from pandas import read_csv
import numpy
import operator

def main(dataset_name):
	current_path = os.path.dirname(os.path.abspath(__file__)) + '\\'
	dataset_path = current_path + dataset_name + '.csv'
	dataset = read_csv(dataset_path, header = None)
	dataset[[0, 1, 2, 3, 4, 5]] = dataset[[0, 1, 2, 3, 4, 5]].replace('null', numpy.NaN)
	frequent_reason = getFrequentReason(dataset[5])
	dataset[5] = dataset[5].replace(numpy.NaN, frequent_reason)
	dataset.to_csv('FinalDatasetWithoutAttributes.csv', index=False)

def getFrequentReason(reason_column):
	reason_dict = {}
	for value in reason_column:
		if value in reason_dict:
			reason_dict[value] += 1
		else:
			reason_dict[value] = 1
	return max(reason_dict, key=reason_dict.get)

if __name__ == '__main__':
	main('CleanDatasetWithoutAttributes')