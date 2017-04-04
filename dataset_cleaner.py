import os
import csv
import sys

def load(dataset_1_path, dataset_2_path):
	dataset_1, dataset_2, features = [], [], []
	with open(dataset_1_path, 'r') as dataset_1_file, open(dataset_2_path, 'r') as dataset_2_file:
		data_1_reader = csv.reader(dataset_1_file)
		data_1_lines = list(data_1_reader)
		features = data_1_lines.pop(0)
		dataset_1 = data_1_lines
		data_2_reader = csv.reader(dataset_2_file)
		data_2_lines = list(data_2_reader)
		data_2_lines.pop(0)
		dataset_2 = data_2_lines
	return dataset_1, dataset_2, features

def cleanDatasetWithAttributes(dataset_1, features):
	new_dataset = []
	new_features = ['ZIP Code', 'Albumin', 'Creatinine', 'Hemoglobin', 'ACR', 'Weight', 'Height', 'Urea', 'Primary Renal Disease', 
	'Other Primary Renal Disease', 'Angina?', 'Myocardial Infarct?', 'Coronary Artery Bypass Grafts/Angioplasty?', 'Pulmonary Edema',
	'Cerebrovascular', 'Peripheral Vas', 'Diabetes Type I', 'Diabetes Type II', 'Malignancy', 'Malignancy Site', 'Other Malignancy Site',
	'Chronic Obstructive Lung Disease?', 'Other Serious Illness', 'Specified Other Serious Illness', 'Current Smoker', 'Age', 'Sex', 
	'Dialysis Start Date', 'Treatment Duration', 'Number of Modality Changes', 'Final Modality', 'Reason Code']
	for patient in dataset_1:
		new_patient = []
		for attr in range(len(patient)):
			if (attr > 0 and attr < 8) or (attr > 9 and attr < 28) or attr == 30 or (attr > 34 and attr < 38) or attr == 39 or attr == 44:
				attribute = patient[attr].strip().lower()
				if attr == 35:
					attribute = attribute.split(' ')[0]
				new_patient.append(attribute)
			if attr == 29:
				new_patient.append(calcAge(int(patient[attr])))
		new_dataset.append(new_patient)
	return new_dataset, new_features

def cleanDatasetWithoutAttributes(dataset_2, features):
	new_dataset = []
	new_features = ['Age', 'Sex', 'Dialysis Start Date', 'Treatment Duration', 'Number of Modality Changes', 'Final Modality', 'Reason Code']
	for patient in dataset_2:
		new_patient = []
		for attr in range(len(patient)):
			if attr == 30 or (attr > 34 and attr < 38) or attr == 39 or attr == 44:
				attribute = patient[attr].strip().lower()
				if attr == 35:
					attribute = attribute.split(' ')[0]
				new_patient.append(attribute)
			if attr == 29:
				new_patient.append(calcAge(int(patient[attr])))
		new_dataset.append(new_patient)
	return new_dataset, new_features

def calcAge(year):
	return 2017 - year

def write(dataset_1, dataset_2, features_1, features_2, current_path):
	new_file_1_path = current_path + 'CleanDatasetWithAttributes.csv'
	new_file_2_path = current_path + 'CleanDatasetWithoutAttributes.csv'
	dataset_1 = [features_1] + dataset_1
	dataset_2 = [features_2] + dataset_2
	with open(new_file_1_path, 'w', newline = '') as new_file_1, open(new_file_2_path, 'w', newline = '') as new_file_2:
		writer = csv.writer(new_file_1, delimiter=',')
		writer.writerows(dataset_1)
		writer = csv.writer(new_file_2, delimiter=',')
		writer.writerows(dataset_2)
	new_file_1.close()
	new_file_2.close()
	return

def main(dataset_1_name, dataset_2_name):
	current_path = os.path.dirname(os.path.abspath(__file__)) + '\\'
	dataset_1_path = current_path + dataset_1_name + '.csv'
	dataset_2_path = current_path + dataset_2_name + '.csv'
	dataset_1, dataset_2, features = load(dataset_1_path, dataset_2_path)
	dataset_1, features_1 = cleanDatasetWithAttributes(dataset_1, features)
	dataset_2, features_2 = cleanDatasetWithoutAttributes(dataset_2, features)
	write(dataset_1, dataset_2, features_1, features_2, current_path)

if __name__ == '__main__':
	main("DatasetWithAttributes", "DatasetWithoutAttributes")