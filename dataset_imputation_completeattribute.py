import pandas as pd
import numpy as np
from sklearn import preprocessing

df = pd.read_csv("CleanDatasetWithAttributes.csv")
for name in df:
    df[name] = df[name].apply(lambda x : x.replace("}", "") if isinstance(x, str) else x)

def imputation_mean(df, name="Albumin"):
    df[name] = df[name].replace("null", np.NaN).astype(np.float64)
    df[name] = df[name].fillna(df[name].mean())
    df[name] = df[name].astype(np.float64)
    return df[name]

def getFrequentReason(reason_column):
  reason_dict = {}
  for value in reason_column:
    if value in reason_dict:
      reason_dict[value] += 1
    else:
      reason_dict[value] = 1
  return max(reason_dict, key=reason_dict.get)

names = ["Albumin", "Creatinine", "Hemoglobin", "Weight", "Height", "Urea"]

for name in names:
    print("convert {}".format(name))
    df[name] = imputation_mean(df, name)

booleanColumns = ["Current Smoker"]

df[booleanColumns] = df[booleanColumns].replace("n", 0).replace("y", 1).replace("u", 2).astype(int)

df.Sex = df.Sex.replace("f", 0).replace("m", 1)
df[df.columns[10]] = df[df.columns[10]].replace('conventional (1to4 treatments)', 0).replace('hemodialysis acute', 1).replace('hemodialysis satellite', 2).replace('nocturnal (night treatments)', 3).replace('short daily (5,6,7 treatments)', 4).replace('home hemodialysis', 5).replace('capd', 6).replace('ccpd (apd)', 7).replace('pd/hemo combo', 8).replace('hemo/pd', 9).replace('withdrawl from treatment', 10).replace('deceased', 11).replace('transplanted', 12).replace('dc from  rrt (recovered)', 13)

#[df.columns[21]] = df[df.columns[21]].replace(FALSE, 0).replace("TRUE", 1)
df.Withdrew = df.Withdrew.astype(int)
frequent_reason = getFrequentReason(df['Reason Code'])
df['Reason Code'] = df['Reason Code'].replace('null', frequent_reason)

df.to_csv("FinalDatasetWithAttributes.csv")