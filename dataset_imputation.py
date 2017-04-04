import sys
import os
import csv
from pandas import read_csv
import numpy
import operator

def main(dataset_1_name, dataset_2_name):
	current_path = os.path.dirname(os.path.abspath(__file__)) + '\\'
	dataset_1_path = current_path + dataset_1_name + '.csv'
	dataset_2_path = current_path + dataset_2_name + '.csv'
	dataset_1 = read_csv(dataset_1_path, header = None)
	dataset_2 = read_csv(dataset_2_path, header = None)
	dataset_2[[0, 1, 2, 3, 4, 5, 6]] = dataset_2[[0, 1, 2, 3, 4, 5, 6]].replace('null', numpy.NaN)
	frequent_reason = getFrequentReason(dataset_2[6])
	dataset_2[6] = dataset_2[6].replace(numpy.NaN, frequent_reason)
	dataset_2.to_csv('FinalDatasetWithoutAttributes.csv', index=False)

def getFrequentReason(reason_column):
	reason_dict = {}
	for value in reason_column:
		if value in reason_dict:
			reason_dict[value] += 1
		else:
			reason_dict[value] = 1
	return max(reason_dict, key=reason_dict.get)

if __name__ == '__main__':
	main('CleanDatasetWithAttributes', 'CleanDatasetWithoutAttributes')