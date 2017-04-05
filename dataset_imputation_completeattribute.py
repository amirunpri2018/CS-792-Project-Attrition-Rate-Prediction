import pandas as pd
import numpy as np

df = pd.read_csv("CleanDatasetWithAttributes.csv")
for name in df:
    df[name] = df[name].apply(lambda x : x.replace("}", "") if isinstance(x, str) else x)

def imputation_mean(df, name="Albumin"):
    df[name] = df[name].replace("null", np.NaN).astype(np.float64)
    df[name] = df[name].fillna(df[name].mean())
    df[name] = df[name].astype(int)
    return df[name]

def getFrequentReason(reason_column):
  reason_dict = {}
  for value in reason_column:
    if value in reason_dict:
      reason_dict[value] += 1
    else:
      reason_dict[value] = 1
  return max(reason_dict, key=reason_dict.get)

names = ["Albumin", "Creatinine", "Hemoglobin", "ACR", "Weight", "Height", "Urea"]

for name in names:
    print("convert {}".format(name))
    df[name] = imputation_mean(df, name)

booleanColumns = ['Angina?', 'Myocardial Infarct?',
       'Coronary Artery Bypass Grafts/Angioplasty?', 'Pulmonary Edema',
       'Cerebrovascular', 'Peripheral Vas', 'Diabetes Type I',
       'Diabetes Type II', "Malignancy", "Chronic Obstructive Lung Disease?", "Other Serious Illness", "Current Smoker"]

yesNoDF = df[booleanColumns].replace("n", 0).replace("y", 1).replace("null", np.NaN).replace("u", np.NaN).astype(float)

df[booleanColumns] = yesNoDF.fillna(yesNoDF.mean()).astype(int)

yesNoDF.fillna(yesNoDF.mean()).astype(int)

df[['Malignancy', 'Malignancy Site',
       'Chronic Obstructive Lung Disease?', 'Other Serious Illness',
       'Current Smoker', 'Age', 'Sex', 'Treatment Duration',
       'Number of Modality Changes', 'Withdrew', 'Reason Code']]

df["Primary Renal Disease"] = df["Primary Renal Disease"].replace("null", 0).astype(int)

df.Sex = df.Sex.replace("f", 0).replace("m", 1)

df["Malignancy Site"] = df["Malignancy Site"].replace("null", 0).astype(int)

frequent_reason = getFrequentReason(df['Reason Code'])
df['Reason Code'] = df['Reason Code'].replace('null', frequent_reason)

df.to_csv("FinalDatasetWithAttributes.csv")