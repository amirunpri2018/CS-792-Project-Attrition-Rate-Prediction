import sys
import os
import csv
from pandas import read_csv
import numpy
import operator
from sklearn import preprocessing

def main(dataset_name):
	current_path = os.path.dirname(os.path.abspath(__file__)) + '\\'
	dataset_path = current_path + dataset_name + '.csv'
	dataset = read_csv(dataset_path, header = None)
	dataset[2] = dataset[2].replace("f", 0).replace("m", 1)
	dataset[3] = dataset[3].replace('conventional (1to4 treatments)', 0).replace('hemodialysis acute', 1).replace('hemodialysis satellite', 2).replace('nocturnal (night treatments)', 3).replace('short daily (5,6,7 treatments)', 4).replace('home hemodialysis', 5).replace('capd', 6).replace('ccpd (apd)', 7).replace('pd/hemo combo', 8).replace('hemo/pd', 9).replace('withdrawl from treatment', 10).replace('deceased', 11).replace('transplanted', 12).replace('dc from  rrt (recovered)', 13)
	for i in range(len(dataset[3])):
		if type(dataset[3][i]) != int and i > 0:
			dataset[3][i] = 14
	dataset[13] = dataset[13].replace('false', 0).replace('true', 1)
	print(dataset[13])
	frequent_reason = getFrequentReason(dataset[14])
	dataset[14] = dataset[14].replace('null', frequent_reason)
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