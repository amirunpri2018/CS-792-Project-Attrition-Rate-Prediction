import csv
import sys
import os

def load(dataset_path):
    dataset, features = [], []
    with open(dataset_path, 'r') as dataset_file:
        file = csv.reader(dataset_file)
        file_lines = list(file)
        features = file_lines.pop(0)
        dataset = file_lines
    dataset_file.close()
    return dataset, features

def flatten(dataset, features):

    withdrawed = False
    shouldSkipID = None

    start_date, duration, modality_changes, new_dataset = dataset[0][35], -1, {}, []
    modality_changes[dataset[0][46]] = 1
    withdrawed = False
    for patient_i in range(1, len(dataset)):
        if int(dataset[patient_i - 1][0]) == int(dataset[patient_i][0]):
            if withdrawed:
                continue

            modality_code = dataset[patient_i][44]
            if modality_code == "143":
                withdrawed = True
                continue
            else:
                new_modality = dataset[patient_i][46]
                if new_modality in modality_changes:
                    modality_changes[new_modality] += 1
                else:
                    modality_changes[new_modality] = 1
        else:
            end_date = dataset[patient_i - 1][35]
            if start_date != 'NULL' and end_date != 'NULL':
                duration = getDuration(start_date, end_date)
                if patient_i < 20:
                    print(start_date, end_date, duration)
            else:
                duration = 1
            new_patient = dataset[patient_i - 1][:35]
            new_patient.append(start_date)
            new_patient.append(duration)
            changes = 0
            for key in modality_changes:
                changes += modality_changes[key]
            new_patient.append(changes)
            new_patient.append(withdrawed)
            new_patient = new_patient + dataset[patient_i - 1][36:]
            new_dataset.append(new_patient)
            start_date = dataset[patient_i][35]
            new_modality = dataset[patient_i][46]
            modality_changes = {}
            modality_changes[new_modality] = 1
            withdrawed = False
    print(new_dataset[0])
    return new_dataset

def getDuration(start_date, end_date):
    start_date = start_date.split(" ")[0]
    end_date = end_date.split(" ")[0]
    start = start_date.split('-')
    end = end_date.split('-')
    start_month = int(start[1])
    start_year = int(start[0])
    end_month = int(end[1])
    end_year = int(end[0])
    duration = 0
    if end_year > start_year:
        duration += 12*(end_year - start_year - 1)
    if start_year == end_year:
        duration += end_month - start_month
    else:
        duration += end_month + (12 - start_month)
    if duration == 0:
        duration = 1
    return duration

def write(dataset, features, current_path):
    new_file_path = current_path + 'FlattenedDataset.csv'
    dataset = [features] + dataset
    with open(new_file_path, 'w') as new_file:
        writer = csv.writer(new_file, delimiter=',')
        writer.writerows(dataset)
    new_file.close()
    return

def main(dataset_name):
    current_path = os.path.dirname(os.path.abspath(__file__)) + '/'
    dataset_path = current_path + dataset_name + '.csv'
    dataset, features = load(dataset_path)
    features_1 = features[:36]
    features_2 = features[36:]
    features = features_1 + ['Duration'] + ['Number of Modality Changes'] + ["Withdrawed"] + features_2
    dataset = flatten(dataset, features)
    write(dataset, features, current_path)
    print(features)

if __name__ == '__main__':
    main('Templates')
