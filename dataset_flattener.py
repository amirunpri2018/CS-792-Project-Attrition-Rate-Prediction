import csv
import sys
import os

modalityLessThanMonth = ['DC FROM RRT (Recovered)', 'DECEASED', 'TRANSPLANTED', 'WITHDRAWL FROM TREATMENT']
peritoneal = ['CAPD', 'CCPD (APD)']
inCenter = ['CONVENTIONAL (1to4 Treatments)', 'HEMODIALYSIS ACUTE', 'HEMODIALYSIS SATELLITE', 'NOCTURNAL (Night Treatments)', 'SHORT DAILY (5,6,7 Treatments)']
home = ['HOME HEMODIALYSIS']
combined = ['PD/Hemo Combo', 'HEMO/PD']

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

    withdrew = False 
    shouldSkipID = None

    start_date, start_treatment_modality, prev_modality_desc, duration, modality_changes, new_dataset = dataset[0][35], dataset[0][47], dataset[0][47], -1, {}, []
    code12, code23, code34, code45, code13, code14, code24, comorbidity = 0, 0, 0, 0, 0, 0, 0, 0
    modality_changes[dataset[0][46]] = 1
    for patient_i in range(1, len(dataset)):
        if int(dataset[patient_i - 1][0]) == int(dataset[patient_i][0]):
            if withdrew:
                continue
            modality_code = dataset[patient_i][44]
            reason = dataset[patient_i][49]
            if comorbidity == 0:
                for i in range(11, 27):
                    if dataset[patient_i][i] != 'NULL':
                        comorbidity = 1
            if reason in modalityLessThanMonth:
                curr_date = dataset[patient_i][35]
                duration = getDuration(start_date, curr_date)
                if duration == 0 or duration == 1:
                    continue
                else:
                    start_date = curr_date
            if modality_code == "143":
                withdrew = True
                continue
            else:
                new_modality_code = dataset[patient_i][46]
                modality_changes[new_modality_code] = 1
                new_modality_desc = dataset[patient_i][47]
                print('prev desc: ', prev_modality_desc, 'new desc: ', new_modality_desc)
                if (prev_modality_desc in peritoneal and new_modality_desc in inCenter) or (prev_modality_desc in inCenter and new_modality_desc in peritoneal):
                    code12 = 1
                elif (prev_modality_desc in inCenter and new_modality_desc in home) or (prev_modality_desc in home and new_modality_desc in inCenter):
                    code23 = 1
                elif (prev_modality_desc in home and new_modality_desc in combined) or (prev_modality_desc in combined and new_modality_desc in home) :
                    code34 = 1
                elif (prev_modality_desc in peritoneal and new_modality_desc in home) or (prev_modality_desc in home and new_modality_desc in peritoneal):
                    code13 = 1
                elif (prev_modality_desc in peritoneal and new_modality_desc in combined) or (prev_modality_desc in combined and new_modality_desc in peritoneal):
                    code14 = 1
                elif (prev_modality_desc in inCenter and new_modality_desc in combined) or (prev_modality_desc in combined and new_modality_desc in inCenter):
                    code24 = 1
                elif new_modality_desc not in peritoneal and new_modality_desc not in inCenter and new_modality_desc not in home and new_modality_desc not in combined:
                    code45 = 1
                prev_modality_desc = new_modality_desc
        else:
            end_date = dataset[patient_i - 1][35]
            if start_date != 'NULL' and end_date != 'NULL':
                duration = getDuration(start_date, end_date)
            else:
                duration = 1
            new_patient = dataset[patient_i - 1][:11]
            new_patient.append(comorbidity)
            new_patient = new_patient + dataset[patient_i][27:36]
            new_patient.append(start_treatment_modality)
            new_patient.append(duration)
            changes = 0
            for key in modality_changes:
                changes += modality_changes[key]
            new_patient.append(changes)
            new_patient.append(code12)
            new_patient.append(code13)
            new_patient.append(code14)
            new_patient.append(code23)
            new_patient.append(code24)
            new_patient.append(code34)
            new_patient.append(code45)
            new_patient.append(withdrew)
            new_patient = new_patient + dataset[patient_i - 1][36:]
            new_dataset.append(new_patient)
            start_date = dataset[patient_i][35]
            start_treatment_modality = dataset[patient_i][47]
            new_modality_code = dataset[patient_i][46]
            prev_modality_desc = dataset[patient_i][47]
            modality_changes = {}
            code12, code23, code34, code45, comorbidity = 0, 0, 0, 0, 0
            for i in range(11, 27):
                if dataset[patient_i][i] != 'NULL':
                    comorbidity = 1
            modality_changes[new_modality_code] = 1
            withdrew = False
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
    return duration

def write(dataset, features, current_path):
    new_file_path = current_path + 'FlattenedDataset.csv'
    dataset = [features] + dataset
    with open(new_file_path, 'w', newline='') as new_file:
        writer = csv.writer(new_file, delimiter=',')
        writer.writerows(dataset)
    new_file.close()
    return

def main(dataset_name):
    current_path = os.path.dirname(os.path.abspath(__file__)) + '/'
    dataset_path = current_path + dataset_name + '.csv'
    dataset, features = load(dataset_path)
    features_1 = features[:11]
    features_2 = features[27:36]
    features_3 = features[36:]
    features = features_1 + ['Comorbidity'] + features_2 + ['Start Treatment Modality'] + ['Duration'] + ['Number of Modality Changes'] + ['Code 12'] + ['Code 13'] + ['Code 14'] + ['Code 23'] + ['Code 24'] + ['Code 34'] + ['Code 45'] + ["Withdrew"] + features_3
    dataset = flatten(dataset, features)
    write(dataset, features, current_path)

if __name__ == '__main__':
    main('Templates')
