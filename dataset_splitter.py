import csv
import sys
import os

def load(dataset_path):
	dataset, features = [], []
	with open(dataset_path, 'r') as dataset_file:
		data_reader = csv.reader(dataset_file)
		data_lines = list(data_reader)
		features = data_lines.pop(0)
		dataset = data_lines
	return dataset, features

def split(dataset):
	dataset_1, dataset_2 = [], []
	for patient in dataset:
		null_count = 0
		for attribute in range(2, 28):
			attr = patient[attribute].strip().lower()
			if attr == 'null':
				null_count += 1
		if null_count > 20:
			dataset_1.append(patient)
		else:
			dataset_2.append(patient)
	return dataset_1, dataset_2

def write(dataset_1, dataset_2, features, current_path):
	new_file_1_path = current_path + 'DatasetWithoutAttributes.csv'
	new_file_2_path = current_path + 'DatasetWithAttributes.csv'
	dataset_1 = [features] + dataset_1
	dataset_2 = [features] + dataset_2
	with open(new_file_1_path, 'w', newline = '') as new_file_1, open(new_file_2_path, 'w', newline = '') as new_file_2:
		writer = csv.writer(new_file_1, delimiter=',')
		writer.writerows(dataset_1)
		writer = csv.writer(new_file_2, delimiter=',')
		writer.writerows(dataset_2)
	new_file_1.close()
	new_file_2.close()
	return

def main(dataset_name):
	current_path = os.path.dirname(os.path.abspath(__file__)) + '\\'
	dataset_path = current_path + dataset_name + '.csv'
	dataset, features = load(dataset_path)
	dataset_1, dataset_2 = split(dataset)
	write(dataset_1, dataset_2, features, current_path)

if __name__ == '__main__':
	main('FlattenedDataset')